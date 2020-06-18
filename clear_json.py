import os
import os.path as osp
from tqdm import tqdm
import json


def func(root_path):
    bar = os.listdir(root_path)
    bar = tqdm(bar)
    for file in bar:
        file_path = f'{root_path}/{file}'
        j_json = json.load(open(file_path, 'r'))
        flags = j_json['flags']
        if flags == {}:
            j_json['shapes'][0]['label'] = 'OK'
        else:
            label = None
            for k, v in flags.items():
                if v:
                    label = k
            if label is None:
                label = 'OK'

            j_json['shapes'][0]['label'] = label

        with open(file_path, 'w') as fid:
            json.dump(j_json, fid, indent=4)


if __name__ == '__main__':
    root_dirs = [f'E:/project/huatian/labelme_json/annonate_json/NG/{i}' for i in [1, 2, 3, 4]]
    # root_dirs = [f'E:/project/huatian/labelme_json/modify_json/NG/{i}' for i in [1, 2, 3, 4]]
    for root_dir in root_dirs:
        func(root_dir)
