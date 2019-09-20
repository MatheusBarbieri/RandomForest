import time
import random

from util import load_data, load_attributes, get_args
from sampling import generate_k_folds, generate_splits
from forest import Forest


if __name__ == "__main__":
    args = get_args()
    data = load_data(args.dataset)
    attributes = load_attributes(args.attributes)
    seed = args.seed

    random.seed(seed)

    k_folds = generate_k_folds(data, args.kfolds, seed=seed)
    splits = generate_splits(k_folds)

    for i, split in enumerate(splits):
        train, test = split

        start = time.time()
        forest = Forest.generate(train, attributes, args.ntree)
        end = time.time()
        print("Forest {} generation time: {}s".format(i+1, "{0:.4f}".format(end-start)))

        results = forest.predict_df(test)

        total = len(results)
        correct = len(results[results['predicted'] == results['class']])
        print(f"Total: {total}, classified correctly: {correct}")
