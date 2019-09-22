from multiprocessing import Pool
import pandas as pd
import numpy as np
import os
import random
import time

from metrics import ConfusionMatrix
from util import load_data, load_attributes, get_args
from sampling import generate_k_folds, generate_splits
from forest import Forest


if __name__ == "__main__":
    args = get_args()
    data_path = args.dataset
    data = load_data(data_path)
    attributes = load_attributes(args.attributes)

    seed = args.seed
    k_folds_number = args.kfolds
    trees_number = args.ntree
    verbose = args.verbose or 0
    attributes_in_division = args.m if args.m else max(int(np.sqrt(len(attributes))), 3)

    if seed:
        print(f"Using seed: {seed}")
        random.seed(seed)

    k_folds = generate_k_folds(data, k_folds_number, seed=seed)
    splits = generate_splits(k_folds)

    with Pool(os.cpu_count()*2 - 1) as pool:
        total_results = []
        total_start = time.time()
        for i, split in enumerate(splits):
            train, test = split

            start = time.time()
            forest = Forest.generate(train, attributes, trees_number, m=attributes_in_division, pool=pool)
            end = time.time()

            if verbose > 1:
                print("="*50)
                print("Forest {} generation time: {}s".format(i+1, "{0:.3f}".format(end-start)))

            results = forest.predict_df(test)
            total_results.append(results)

            if verbose > 1:
                confusion_matrix = ConfusionMatrix(results)
                confusion_matrix.show(verbose=(verbose > 2))

        final_confusion_matrix = ConfusionMatrix(pd.concat(total_results))
        if verbose > 1:
            print("="*50)
        print(f"Results for {data_path.replace('.csv', '')}:")
        print(f"Params: k_folds: {k_folds_number}; ntree: {trees_number}; m: {attributes_in_division}; seed: {seed}")
        final_confusion_matrix.show(verbose=(verbose > 0))
        total_end = time.time()
        print(f"Total processing time: {total_end-total_start:0.3f}s")
