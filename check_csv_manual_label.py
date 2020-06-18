import pandas as pd
import os
import glob
import json
import numpy as np


def main():
    df = pd.read_csv(r'E:\project\Denso\results\efficient_results.csv')
    v = df.values
    names, labels = zip(*v)
    d = {x.split('/')[-1]: y for x, y in zip(names, labels)}
    json_dir = r'E:\project\Denso\original_data\GIC\test'
    json_list = glob.glob(f"{json_dir}/*.json")
    # json_list = [item.split('\\')[-1] for item in json_list]

    results = []
    confuse_matrixs = np.zeros([8, 8])
    label2index = ['NG1', 'NG2', 'NG3', 'NG4', 'NG5', 'NG6', 'NG7', 'OK']

    for js in json_list:
        j = json.load(open(js, 'r'))
        label = None
        count = 0
        for k, v in j['flags'].items():
            if v:
                count += 1
                label = k
        if count != 1:
            raise ValueError

        name = js.split('\\')[-1].replace('json', 'jpg')
        if name in d:
            pred = d[name]
        else:
            pred = None
        target = label

        confuse_matrixs[label2index.index(target), label2index.index(pred)] += 1

        if target != pred:
            # print(name, '\ttarget:', f"{target:3s}", '\tpred:', pred, '\t', target == pred)
            results.append(f"{name} \ttarget:{target:3s}\tpred:{pred:3s}\t{target == pred}")
    return results, confuse_matrixs


if __name__ == '__main__':
    ret, cm = main()
    for _ in ret:
        print(_)
    print(len(ret))
    print(cm)
    for i in range(len(cm)):
        for j in range(len(cm)):
            print(int(cm[i, j]), end='\t')
        print()

