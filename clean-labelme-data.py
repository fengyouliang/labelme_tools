import json
import os
import os.path as osp
from pathlib import Path

from tqdm import tqdm


def scan_folder(data_dir, extension='json'):
    assert os.path.exists(data_dir), data_dir + " does not exist"
    extension = extension.strip('.')
    files = Path(data_dir).glob('**/*.{}'.format(extension))
    files = [str(x) for x in files]
    return files


def load_json(json_file):
    with open(json_file, encoding='GBK') as fid:
        return json.load(fid)


def clean_path(path):
    path = path.replace('\\', '/')
    key = 'ADC0515/'
    assert key in path, path
    relative_path = key + path.split(key)[1]
    return relative_path


def remove_image_data(json_file):
    obj = load_json(json_file)
    obj['imageData'] = None

    # clean path
    obj['imagePath'] = clean_path(obj['imagePath'])

    # clean flags
    obj['flags'] = {}

    # save json to the file
    with open(json_file, 'w') as fid:
        json.dump(obj, fid, indent=4)


def run_remove(tar_dir):
    json_files = scan_folder(tar_dir)
    for json_file in tqdm(json_files):
        remove_image_data(json_file)


def clear_original():
    tar_dir = r'E:\project\huatian\labelme_json'
    for fold in os.listdir(tar_dir):
        run_remove(osp.join(tar_dir, fold))


if __name__ == '__main__':
    # set gpu
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--target_dir', dest='tar_dir',
    #                     help='Json directory',
    #                     default=r'E:\project\huatian\json\fengyouliang',
    #                     type=str)
    # args = parser.parse_args()
    #
    # run_remove(args.tar_dir)
    # clear_original()
    pass
