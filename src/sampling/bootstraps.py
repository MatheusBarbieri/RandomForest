from numpy.random import randint


def generate_bootstraps(df, n, seed=randint(10000)):
    bootstraps = []
    for i in range(n):
        sample = df.sample(frac=1, replace=True, random_state=seed+i)
        bootstraps.append(sample)

    return bootstraps
