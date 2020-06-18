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


def get_all_jsons(root_path='E:/project/huatian/labelme_json/original_json', sub_path='fyl'):
    path = f"{root_path}/{sub_path}"
    json_list = []
    for dirname, _, filenames in os.walk(path):
        clear_list = [f'{dirname}/{filename}'.replace('\\', '/') for filename in filenames]
        json_list.extend(clear_list)
    return json_list


def glob_all_jsons(root_path='E:/project/huatian/labelme_json/original_json', sub_path='yyq'):
    path = f"{root_path}/{sub_path}"
    json_list = glob.glob(f'{path}/*/*/*.json', recursive=True)
    return json_list


def check_single_json(ori_json_file, ann_json_file, mod_json_file):
    ori_json = json.load(open(ori_json_file, 'r'))
    ann_json = json.load(open(ann_json_file, 'r'))
    mod_json = json.load(open(mod_json_file, 'r'))


def check_annonation(root_path='E:/project/huatian/labelme_json'):
    original_dir = f'{root_path}/original_json'
    annonate_dir = f'{root_path}/annonate_json'
    modify_dir = f'{root_path}/modify_json'

    root_paths = [f'{root_path}/original_json', f'{root_path}/annonate_json', f'{root_path}/modify_json']
    person_paths = os.listdir(original_dir)

    for person in person_paths:

        ori_json_list = get_all_jsons(original_dir, person)
        ann_json_list = get_all_jsons(annonate_dir, person)
        mod_json_list = get_all_jsons(modify_dir, person)
        assert len(ori_json_list) == len(ann_json_list) == len(mod_json_list)

        for ori_json, ann_json, mod_json in zip(ori_json_list, ann_json_list, mod_json_list):
            check_single_json(ori_json, ann_json, mod_json)


def main():
    ret = get_all_jsons()
    for _ in ret:
        print(_)


if __name__ == '__main__':
    # main()
    glob_all_jsons()
