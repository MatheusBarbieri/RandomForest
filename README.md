# Random Forest

> This is a random forest classifier developed for the course: INF01017 - Aprendizado de Máquina (2019/2).

### Installation
This application requires Python version 3.6 or newer

There is a Makefile in the project folder which has set up rules for installing and running this application. Make sure you are on a python 3.6+ enviroment and call `make setup`.

### Usage
```
main.py [-h] -d DATASET -a ATTRIBUTES [-s SEED] [-m M] [-n NTREE] [-k KFOLDS] [-p] [-v]

Random Forest Classifier

mandatory arguments:
  -d DATASET, --dataset DATASET
                        Path to csv dataset for training or classification.
  -a ATTRIBUTES, --attributes ATTRIBUTES
                        Path to json object containing attributes wich will be
                        used and its kind information.

optional arguments:
  -h, --help            show this help message and exit
  -s SEED, --seed SEED  Seed to random numbers and sampling.
  -m M                  Number of sample attributes used on each division on
                        tree [if not present, all attributes are used].
  -n NTREE, --ntree NTREE
                        Number of trees generated on ensamble [default: 5].
  -k KFOLDS, --kfolds KFOLDS
                        Number of k-folds generated for cross-validation
                        [default: 5].
  -p, --parallelize     Parallelize with 2x number of cpu cores processes on
                        tree generation. WARNING: seed values wont work if -p
                        activated.
  -v, --verbose
  ```
