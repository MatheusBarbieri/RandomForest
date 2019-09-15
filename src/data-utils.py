import os
import pandas as pd


def read_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        raise Exception("File does not exists.")


def get_attributes_names(df):
    return df.columns.to_list()


def generate_k_folds(df, k, seed=42):
    fold_size = df // k
    if not fold_size:
        raise Exception("Fold size should be smaller than dataset rows")

    folds = []
    for i in range(k):
        sample = df.sample(n=fold_size, random_state=seed)
        df = df.drop(sample.index)
        folds.append(sample)

    # add remaining elements to first fold
    folds[0] = pd.concat([folds[0], df])

    return folds
