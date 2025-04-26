# Variables
PYTHON=python3

# Targets
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) Main.py

clean:
	rm -rf data/*.parquet
	rm -f data/execution_report.json

all: install run
