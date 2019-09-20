def generate_bootstraps(df, n, seed=42):
    bootstraps = []
    for i in range(n):
        sample = df.sample(frac=1, replace=True, random_state=seed+i)
        bootstraps.append(sample)

    return bootstraps
