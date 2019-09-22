import os
import json
from time import time
import pandas as pd


def load_data(path):
    if os.path.exists(path):
        df = pd.read_csv(path)
        if 'Class' in df.columns:
            df = df.rename(columns={'Class': 'class'})
        elif 'CLASS' in df.columns:
            df = df.rename(columns={'CLASS': 'class'})

        if 'class' not in df.columns:
            raise Exception("Dataset does not contains \"Class\" column.")

        return df
    else:
        raise Exception("File does not exists.")


def load_attributes(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        raise Exception("Missing attribute category info.")


def save_results(cm, data_path, k_folds, ntree, m, exec_time, seed, parallel, path='results'):
    data_name = os.path.basename(data_path)
    file_path = path + '/' + data_name

    if not os.path.exists(path):
        os.mkdir(path)

    file_exists = os.path.exists(file_path)
    with open(file_path, 'a+') as f:
        if not file_exists:
            file_header = '"total","correct","accuracy","macro_recall","macro_precision","macro_specificity","macro-f-measure-2","macro-f-measure-1","macro-f-measure-0.5","k_folds","ntree","m","execution_time","timestamp","seed"\r\n' # noqa
            f.write(file_header)

        seed = seed if seed and not parallel else 0

        results = f'{cm._total},{cm._correct},{cm.accuracy()},{cm.macro_recall()},{cm.macro_precision()},{cm.macro_specificity()},{cm.macro_f_measure(2)},{cm.macro_f_measure(1)},{cm.macro_f_measure(0.5)},{k_folds},{ntree},{m},{exec_time},{int(time())},{seed}\r\n' # noqa

        f.write(results)
