import argparse


def get_args(arguments=None):
    parser = argparse.ArgumentParser(description='Random Forest Classificator')

    parser.add_argument(
        '-d',
        '--dataset',
        required=True,
        type=str,
        help="Path to csv dataset for training or classification.")

    parser.add_argument(
        '-a',
        '--attributes',
        required=True,
        type=str,
        help="Path to json object containing attributes wich will be used and its kind information.")

    parser.add_argument(
        '-s',
        '--seed',
        default=42,
        type=int,
        help="Seed to random numbers and sampling.")

    parser.add_argument(
        '-m',
        type=int,
        help="Number of sample attributes used on each division on tree [if not present, all attributes are used].")

    parser.add_argument(
        '-n',
        '--ntree',
        default=5,
        type=int,
        help="Number of trees generated on ensamble [default: %(default)s].")

    parser.add_argument(
        '-k',
        '--kfolds',
        default=5,
        type=int,
        help="Number of k-folds generated for cross-validation [default: %(default)s].")

    args = parser.parse_args(arguments)
    return args
