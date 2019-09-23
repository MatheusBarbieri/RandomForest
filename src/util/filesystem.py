import os
import json
from time import time
import pandas as pd
import numpy as np


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
            file_header = '"total","correct","accuracy","true_positives","true_negatives","false_positives","false_negatives","classes","per_class_recall","per_class_precision","per_class_specificity","macro_recall","macro_precision","macro_specificity","macro_f_measure_2","macro_f_measure_1","macro_f_measure_0.5","k_folds","ntree","m","execution_time","timestamp","seed"\r\n' # noqa
            f.write(file_header)

        seed = seed if seed and not parallel else 0
        classes = str(np.unique(cm._results.values[:, 0]))

        total = cm._total
        correct = cm._correct
        accuracy = cm.accuracy()

        true_positives = f'"{str(cm.true_positives().to_list())}"'
        true_negatives = f'"{str(cm.true_negatives().to_list())}"'
        false_positives = f'"{str(cm.false_positives().to_list())}"'
        false_negatives = f'"{str(cm.false_negatives().to_list())}"'
        per_class_recall = f'"{str(cm.recalls().to_list())}"'
        per_class_precision = f'"{str(cm.precisions().to_list())}"'
        per_class_specificity = f'"{str(cm.specificities().to_list())}"'

        macro_recall = cm.macro_recall()
        macro_precision = cm.macro_precision()
        macro_specificity = cm.macro_specificity()
        macro_f_measure_2 = cm.macro_f_measure(2)
        macro_f_measure_1 = cm.macro_f_measure(1)
        macro_f_measure_05 = cm.macro_f_measure(0.5)
        timestamp = int(time())

        results = f'{total},{correct},{accuracy},{true_positives},{true_negatives},{false_positives},{false_negatives},{classes},{per_class_recall},{per_class_precision},{per_class_specificity},{macro_recall},{macro_precision},{macro_specificity},{macro_f_measure_2},{macro_f_measure_1},{macro_f_measure_05},{k_folds},{ntree},{m},{exec_time},{timestamp},{seed}\r\n' # noqa

        f.write(results)
