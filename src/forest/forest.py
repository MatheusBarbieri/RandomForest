from multiprocessing import Pool
import os
from collections import Counter

from sampling import generate_bootstraps
from tree import Tree


class Forest:
    def __init__(self, trees):
        self.trees = trees

    @classmethod
    def generate(cls, train_set, attributes, ntree, m=None):
        bootstraps = generate_bootstraps(train_set, ntree)
        wraped_bootstraps = [(b, attributes, m) for b in bootstraps]
        with Pool(os.cpu_count()*2 - 1) as p:
            trees = p.starmap(Tree.generate, wraped_bootstraps)

        return Forest(trees)

    def predict(self, instance):
        results = [tree.predict(instance) for tree in self.trees]
        data = Counter(results)
        result = max(results, key=data.get)
        return result

    def predict_df(self, instances):
        instances['predicted'] = instances.apply(lambda x: self.predict(x), axis=1)
        return instances[['class', 'predicted']]
