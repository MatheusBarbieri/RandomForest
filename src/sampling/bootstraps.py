def generate_bootstraps(df, n, seed=42):
    bootstraps = []
    for i in range(n):
        sample = df.sample(frac=1, replace=True, random_state=seed+i)
        bootstraps.append(sample)

    non_used = df
    for b in bootstraps:
        non_used = non_used.drop(b.index, errors='ignore')

    return bootstraps, non_used
