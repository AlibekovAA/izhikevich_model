.PHONY: install run clean lint format type-check

install:
	py -m pip install -r requirements.txt

run:
	py main.py

clean:
	py clean_project.py

lint:
	py -m ruff check .

format:
	py -m ruff format .

type-check:
	py -m mypy .

all: install run
