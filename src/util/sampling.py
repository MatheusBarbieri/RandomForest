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


def _random_k_folds(df, k, add_remaining, seed):
    fold_size = len(df) // k
    if not fold_size:
        raise Exception("Fold size should be smaller than dataset rows")

    folds = []
    for i in range(k):
        sample = df.sample(n=fold_size, random_state=seed)
        df = df.drop(sample.index, errors='ignore')
        folds.append(sample)

    # add remaining elements to folds
    if add_remaining:
        for i in range(len(df)):
            folds[i] = pd.concat([folds[i], df.iloc[i:i+1]])

    return folds


def _stratified_k_folds(df, k, add_remaining, seed):
    groups = df.groupby('class')
    a = [_random_k_folds(g, k, add_remaining, seed) for c, g in groups]
    folds = [pd.concat(a[y][i] for y in range(len(a))) for i in range(k)]
    return folds


def generate_k_folds(df, k, sampling='stratified', add_remaining=True, seed=42):
    if sampling == 'random':
        return _random_k_folds(df, k, add_remaining, seed)
    elif sampling == 'stratified':
        return _stratified_k_folds(df, k, add_remaining, seed)
    else:
        raise Exception("Sampling parameter must be one of [stratified, random]")
