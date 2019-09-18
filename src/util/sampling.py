import pandas as pd


def generate_bootstraps(df, n, seed=42):
    bootstraps = []
    for i in range(n):
        sample = df.sample(frac=1, replace=True, random_state=seed+i)
        bootstraps.append(sample)

    non_used = df
    for b in bootstraps:
        non_used = non_used.drop(b.index, errors='ignore')

    return bootstraps, non_used


def generate_k_folds(df, k, seed=42):
    fold_size = len(df) // k
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
