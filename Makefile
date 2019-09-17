run-credit-g:
	python src/main.py -d "data/dataset_31_credit-g.csv" -k "data/dataset_31_credit-g.json" -m "train"

setup:
	pip install -r requirements.txt -r

setup-dev:
	pip install -r requirements.txt -r requirements_dev.txt

lint:
	flake8
