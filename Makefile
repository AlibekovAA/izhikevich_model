.PHONY: install run clean lint format type-check

install:
	py -m pip install -r requirements.txt

run:
	py main.py

clean:
	if exist __pycache__ rmdir /s /q __pycache__
	if exist models\__pycache__ rmdir /s /q models\__pycache__
	if exist simulation\__pycache__ rmdir /s /q simulation\__pycache__
	if exist ui\__pycache__ rmdir /s /q ui\__pycache__
	if exist .mypy_cache rmdir /s /q .mypy_cache
	if exist .ruff_cache rmdir /s /q .ruff_cache
	del /s /q *.pyc 2>nul
	del /s /q *.pyo 2>nul

lint:
	py -m ruff check .

format:
	py -m ruff format .

type-check:
	py -m mypy .

all: install run
