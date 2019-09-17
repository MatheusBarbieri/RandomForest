run:
	python src/main.py

setup:
	pip install -r requirements.txt -r

setup-dev:
	pip install -r requirements.txt -r requirements_dev.txt

lint:
	flake8
