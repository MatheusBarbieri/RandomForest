run-credit-g:
	python src/main.py -d "data/dataset_31_credit-g.csv" -k "data/dataset_31_credit-g.json" -m "train"

run-spam-base:
	python src/main.py -d "data/dataset_44_spambase.csv" -k "data/dataset_44_spambase.json" -m "train"

run-wine:
	python src/main.py -d "data/dataset_191_wine.csv" -k "data/dataset_191_wine.json" -m "train"

run-vertebral-column:
	python src/main.py -d "data/phpOkU53r.csv" -k "data/phpOkU53r.json" -m "train"

setup:
	pip install -r requirements.txt -r

setup-dev:
	pip install -r requirements.txt -r requirements_dev.txt

lint:
	flake8
