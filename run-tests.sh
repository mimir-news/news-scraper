rm -rf .pytest_cache
mypy --ignore-missing-imports main.py
pytest --cache-clear
