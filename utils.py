import json
import os
import os.path as osp
import shutil
from random import shuffle
import yaml
from tqdm import tqdm
import numpy as np
import pandas as pd


def load(yaml_name='config'):
    config_file = osp.join('./configs', f'{yaml_name}.yaml')
    with open(config_file) as f:
        config = yaml.safe_load(f)
    return config


def split_json(huatian_dir, ok_ng_split=True, chunk_size=1000):
    """
    :param huatian_dir: 该路径包含一个labelme文件夹，文件夹中为待切分的json文件
    :param ok_ng_split: 是否按OK/NG来切分
    :param chunk_size: 分块大小
    :return:
    """

    def split2dir(jsons, extra_fold_name):
        fold_index = 0
        bar = tqdm(enumerate(jsons), total=len(jsons))
        for idx, json_file in bar:
            if (idx + 1) % chunk_size == 0:
                fold_index += 1
            if extra_fold_name is not None:
                output_dir = f'{huatian_dir}/labelme_split/{extra_fold_name}/{fold_index}/'
            else:
                output_dir = f'{huatian_dir}/labelme_split/{fold_index}/'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            shutil.copy(f'{json_dir}/{json_file}', f'{output_dir}/{json_file}')

    def split_ok_ng(jsons):
        ok_list = []
        ng_list = []

        split_ok_ng_bar = tqdm(jsons)
        for _json in split_ok_ng_bar:
            split_ok_ng_bar.set_description('splitting OK NG')
            j = json.load(open(f'{json_dir}/{_json}', 'r'))
            label = j['shapes'][0]['label']
            if label == 'OK':
                ok_list.append(_json)
            elif label == 'NG':
                ng_list.append(_json)
            else:
                raise ValueError

        return ok_list, ng_list

    json_dir = f'{huatian_dir}/labelme'
    json_list = os.listdir(json_dir)
    shuffle(json_list)

    if ok_ng_split:
        ok_json_list, ng_json_list = split_ok_ng(json_list)
        split2dir(ok_json_list, 'OK')
        split2dir(ng_json_list, 'NG')
    else:
        split2dir(json_list, None)


def clear_dir(path):
    shutil.rmtree(path)
    os.makedirs(path)


def check_single_json(json):
    config = load()


def check_json(json_dir):
    for file in os.listdir(json_dir):
        json_file = json.load(open(osp.join(json_dir, file), 'r'))

        # imageData = json_file['imageData']
        # shapes = json_file['shapes']
        # assert imageData is None
        # assert len(shapes) == 1


def check_single_fold(ori_path, mod_path):
    orgin_files = os.listdir(ori_path)
    modify_files = os.listdir(mod_path)
    assert orgin_files == modify_files

    diff_list = []
    table_size = 3
    diff_table = [[0] * table_size for _ in range(table_size)]
    table_dict = {
        'OK': 0,
        'NG': 1,
        'Difficult': 2
    }
    for file in orgin_files:
        ori_json_file = osp.join(ori_path, file)
        mod_json_file = osp.join(mod_path, file)
        ori_json = json.load(open(ori_json_file, 'r'))
        mod_json = json.load(open(mod_json_file, 'r'))
        ori_label = ori_json['shapes'][0]['label']
        mod_label = mod_json['shapes'][0]['label']

        if ori_label != mod_label:
            diff_list.append(file)

            x = table_dict[ori_label]
            y = table_dict[mod_label]
            diff_table[x][y] = diff_table[x][y] + 1

    return diff_list, diff_table


def check_annonation(root_path, sub_fold_name, save_flag='both'):
    """
    :param root_path: sub fold with original_json and modify_json
    :param sub_fold_name:
    :param save_flag: 'ori', 'mod', 'both'
    """
    assert save_flag in ['ori', 'mod', 'both']

    original_dir = f'{root_path}/original_json/{sub_fold_name}'
    annonate_dir = f'{root_path}/annonate_json/{sub_fold_name}'
    modify_dir = f'{root_path}/modify_json/{sub_fold_name}'

    orgin_folds = os.listdir(original_dir)
    annonate_folds = os.listdir(annonate_dir)
    modify_folds = os.listdir(modify_dir)
    assert orgin_folds == modify_folds and orgin_folds == annonate_folds
    statistics_info = dict()
    bar = tqdm(orgin_folds)
    for fold in bar:  # fold = index 0, 1, 2, ...
        ori_path = osp.join(original_dir, fold)
        annonate_path = osp.join(annonate_dir, fold)
        mod_path = osp.join(modify_dir, fold)
        ori_ann_diff_list, ori_ann_diff_table = check_single_fold(ori_path, annonate_path)
        ann_check_diff_list, ann_check_diff_table = check_single_fold(annonate_path, mod_path)

        statistics_info[fold] = dict()
        statistics_info[fold]['original_annonate'] = ori_ann_diff_table
        statistics_info[fold]['annonate_check'] = ann_check_diff_table

        if save_flag in ['ori', 'both']:
            ori_save_path = f'{root_path}/diff_json/original_json/{sub_fold_name}/{fold}'
            if not osp.exists(ori_save_path):
                os.makedirs(ori_save_path)
        if save_flag in ['mod', 'both']:
            mod_save_path = f'{root_path}/diff_json/modify_json/{sub_fold_name}/{fold}'
            if not osp.exists(mod_save_path):
                os.makedirs(mod_save_path)
        if save_flag in ['mod', 'both']:
            mod_save_path = f'{root_path}/diff_json/annonate_json/{sub_fold_name}/{fold}'
            if not osp.exists(mod_save_path):
                os.makedirs(mod_save_path)

        for diff_item in ann_check_diff_list:
            if save_flag in ['ori', 'both']:
                shutil.copy(f'{ori_path}/{diff_item}', f'{ori_save_path}/{diff_item}')
            if save_flag in ['mod', 'both']:
                shutil.copy(f'{ori_path}/{diff_item}', f'{mod_save_path}/{diff_item}')
            # if save_flag in ['mod', 'both']:
            #     shutil.copy(f'{ori_path}/{diff_item}', f'{mod_save_path}/{diff_item}')
        # break

    return statistics_info


def run_check_annonation():
    root = r'E:/project/huatian/labelme_json'
    sub_folds = ['OK', 'NG']
    for sub_fold in sub_folds:
        statistics_info = check_annonation(root, sub_fold, save_flag='both')
        for k, v in statistics_info.items():
            print(f"{root}/{sub_fold}/{k}")
            print(pd.DataFrame(v))


def main():

    split_json(r'E:\project\huatian', ok_ng_split=True, chunk_size=500)
    # clear_dir(r'E:\project\huatian\labelme')

    # run_check_annonation()
    # config = load('config')
    # print(config)


if __name__ == '__main__':
    main()
