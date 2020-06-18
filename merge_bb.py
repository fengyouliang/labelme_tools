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
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_string(string):
    return f"{bcolors.HEADER}{string}{bcolors.ENDC}"


def timeit(func):
    def wrapper(*arg, **kw):
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        func_name = color_string(func.__name__)
        ts = f"\033[1;31m {t2 - t1:.3f}s\033[0m"
        print(f'timeit: {ts} in {func_name}')
        return res
    return wrapper


class double_blind():
    def __init__(self):
        super(double_blind, self).__init__()


@timeit
def glob_all_jsons(root_path='E:/project/huatian/labelme_json/', sub_path='yyq'):
    path = f"{root_path}/{sub_path}"
    json_list = glob.glob(f'{path}/*/*/*.json', recursive=True)
    json_list = [item.replace('\\', '/') for item in json_list]
    return json_list


def check2dir(a_json_file_path, b_json_file_path, save_dir='E:/project/huatian/labelme_DBcheck_json/'):
    os.makedirs(save_dir, exist_ok=True)
    name = a_json_file_path.split('/')[-4]
    move_path = f'{save_dir}/{name}'
    os.makedirs(move_path, exist_ok=True)
    shutil.move(a_json_file_path, f'{move_path}/{osp.basename(a_json_file_path)}')
    os.remove(b_json_file_path)


def check(a_file_path, b_file_path):
    a_json = json.load(open(a_file_path, 'r'))
    b_json = json.load(open(b_file_path, 'r'))
    a_label = a_json['shapes'][0]['label']
    b_label = b_json['shapes'][0]['label']

    if a_label == b_label:
        check2dir(a_file_path, b_file_path)


def main():
    jlo = glob_all_jsons('E:/project/huatian/labelme_json/original_json', 'demo')
    jlm = glob_all_jsons('E:/project/huatian/labelme_json/modify_json', 'demo')

    bar = tqdm(zip(jlo, jlm), total=len(jlo))
    for x, y in bar:
        assert osp.basename(x) == osp.basename(y)
        bar.set_description(osp.basename(x))
        check(x, y)


if __name__ == '__main__':
    main()
