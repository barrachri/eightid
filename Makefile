##@ Subcommands
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[\/0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation
deps/pre: ## Install base setup tools
	python -m pip install -U pip poetry wheel

deps/install:: deps/pre ## Install the dependencies needed for a production installation
	poetry install --no-dev

deps/install-ci:: deps/pre ## Install the dependencies necessary for CI

deps/install-ci::
	poetry install

deps/install-dev:: deps/install-ci ## Install development dependencies

deps/install-dev::
	python -m pip install pre-commit
	pre-commit install

##@ Clean up
clean/temp: clean/build clean/pyc ## Delete all intermediate files

clean/all: clean/temp clean/caches ## Delete all intermediate files and caches

clean/build: ## Delete the Python build files and folders
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.spec

clean/pyc: ## Delete the Python intermediate execution files
	find . -name '*~' -exec rm -f {} +
	find . -name '*.log*' -delete
	find . -name '*_cache' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean/caches: ## Delete the pre-commit and test caches
	pre-commit clean
	rm -rf .coverage
	rm -rf .pytest_cache

##@ Code checks and formatting
format/isort: ## Format your code with isort
	poetry run isort src

format/black: ## Format your code with black
	poetry run black src

format: format/isort format/black ## Format your code with isort and black

lint/pre-commit: ## Run pre-commit against all your files
	pre-commit run --all-files

lint/mypy: ## Run mypy check
	poetry run mypy src

lint/black: ## Run black style check
	poetry run black --check src

lint/isort: ## Run isort import style check
	poetry run isort -c src

lint/flake8: ## Run flake8 check
	poetry run flake8 src

lint: lint/mypy lint/flake8 lint/black lint/isort ## Run all code checks

##@ Tests
test: ## Run tests with coverage
	poetry run python -m pytest -v --cov src tests/

test/debug: ## Run tests in debug mode
	poetry run pytest --pdb --ff
