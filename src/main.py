import time
import random

import pandas as pd

from util import load_data, load_attributes, get_args
from sampling import generate_k_folds
from tree import Tree


if __name__ == "__main__":
    args = get_args()
    data = load_data(args.dataset)
    attributes = load_attributes(args.attributes)
    seed = args.seed

    random.seed()
    k_folds = generate_k_folds(data, 10, seed=seed)
    training = pd.concat(k_folds[:-1])
    test = k_folds[-1]

    start = time.time()
    tree = Tree.generate(training, attributes)
    end = time.time()
    print("Total generation time: ", end-start)

    results = tree.predict_df(test)
    total = len(results)
    correct = 0
    for result in results:
        if result[0] == result[1]:
            correct = correct + 1

    print(f"Total: {total}, Correct: {correct}")
