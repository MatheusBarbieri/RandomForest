from collections import Counter
from numpy.random import randint

from sampling import generate_bootstraps
from tree import Tree, predict as tree_predict


class Forest:
    def __init__(self, trees):
        self.trees = trees

    @classmethod
    def generate(cls, train_set, attributes, ntree, m=None, pool=None, seed=None):
        if not seed:
            seed = randint(10000)
        bootstraps = generate_bootstraps(train_set, ntree, seed=seed)
        wraped_bootstraps = [(b, attributes, m) for b in bootstraps]
        if pool:
            trees = pool.starmap(Tree.generate, wraped_bootstraps)
        else:
            trees = [Tree.generate(b, attributes, m) for b in bootstraps]

        return Forest(trees)

    def predict(self, instance, pool=None):
        wraped_trees = [(tree, instance) for tree in self.trees]
        if pool:
            results = pool.starmap(tree_predict, wraped_trees)
        else:
            results = [tree_predict(tree, instance) for tree in self.trees]

        data = Counter(results)
        result = max(results, key=data.get)
        return result

    def predict_df(self, instances):
        instances['predicted'] = instances.apply(lambda x: self.predict(x), axis=1)
        return instances[['class', 'predicted']]
