import json
import os
import os.path as osp
import shutil
from random import shuffle
import yaml
from tqdm import tqdm
import numpy as np
import pandas as pd
import glob
import numpy as np
from configs import config
import collections


def split_ok_ng(jsons):
    ok_list = []
    ng_list = []

    split_ok_ng_bar = tqdm(jsons)
    for _json in split_ok_ng_bar:
        split_ok_ng_bar.set_description('splitting OK NG')
        j = json.load(open(_json, 'r'))
        label = j['shapes'][0]['label']
        if label == 'OK':
            ok_list.append(_json)
        elif label == 'NG':
            ng_list.append(_json)
        else:
            raise ValueError

    return ok_list, ng_list


def chunk_by_name(llist, names=config.names):
    num_chunk = len(names)
    ret_dict = {name: [] for name in names}
    for idx, item in enumerate(llist):
        person_id = (idx + 1) % num_chunk
        name = names[person_id]
        ret_dict[name].append(item)
    return ret_dict


def db_chunk_by_name(llist, names=config.names):
    names = np.array(names)
    np.random.shuffle(names)
    names = names.reshape(-1, 2)
    num_chunk = names.shape[0]
    ret_dict = collections.OrderedDict()
    # ret_dict = dict()
    for idx, item in enumerate(llist):
        person_id = (idx + 1) % num_chunk
        name = names[person_id, 0]
        cur_list = ret_dict.get(f'{person_id}_{name}', [])
        # ret_dict[f'{idx}_{name}'].append(item)
        cur_list.append(item)
        ret_dict[f'{person_id}_{name}'] = cur_list

    for idx, name in enumerate(names[:, 1]):
        cp_name = names[idx, 0]
        ret_dict[f'{idx}_{name}'] = ret_dict[f'{idx}_{cp_name}']
    return ret_dict


def _copy(a_list, name, copy=True):
    save_path = 'E:/project/huatian/labelme_split'
    for fold_idx, fold_item in enumerate(a_list):
        fold_item = fold_item.replace('\\', '/')
        bn = osp.basename(fold_item)
        dst = f'{save_path}/{name}'
        os.makedirs(dst, exist_ok=True)
        if copy:
            shutil.copy(fold_item, f'{dst}/{bn}')
        else:
            shutil.move(fold_item, f'{dst}/{bn}')


def to_dir(ret_dict, type_name=None, size=config.max_single_size):
    bar = tqdm(ret_dict.items())
    for name, llist in bar:
        # bar.set_description(name)
        llen = len(llist) // size
        for idx in range(llen + 1):
            a = llist[size * idx: size * (idx + 1)]
            dir_name = f'{name}/{idx}' if type_name is None else f'{name}/{type_name}/{idx}'
            bar.set_description(dir_name)
            _copy(a, dir_name)


def split_json(huatian_dir='E:/project/huatian', split_ok_ng_flag=False):
    json_list = glob.glob(f'{huatian_dir}/labelme/*.json')
    shuffle(json_list)

    if split_ok_ng_flag:
        ok_json_list, ng_json_list = split_ok_ng(json_list)

        ok_ret_dict = chunk_by_name(ok_json_list)
        to_dir(ok_ret_dict, type_name='OK')

        ng_ret_dict = chunk_by_name(ng_json_list)
        to_dir(ng_ret_dict, type_name='NG')
    else:
        ret_dict = chunk_by_name(json_list)
        to_dir(ret_dict)


def split(chunk_func=db_chunk_by_name, huatian_dir='E:/project/huatian', split_ok_ng_flag=False):
    json_list = glob.glob(f'{huatian_dir}/labelme/*.json')
    shuffle(json_list)

    if split_ok_ng_flag:
        ok_json_list, ng_json_list = split_ok_ng(json_list)

        ok_ret_dict = chunk_func(ok_json_list)
        to_dir(ok_ret_dict, type_name='OK')

        ng_ret_dict = chunk_func(ng_json_list)
        to_dir(ng_ret_dict, type_name='NG')
    else:
        ret_dict = chunk_func(json_list)
        to_dir(ret_dict)


def main():
    split()


if __name__ == '__main__':
    main()
