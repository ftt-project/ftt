.ONESHELL:

FTT_ENV_NAME := ftt
FTT_ENV_CHECK := $(shell conda env list | grep ftt)
CONDA := $(shell command -v conda 2>/dev/null)
CONDA_LOCK := $(shell command -v conda-lock 2>/dev/null)
POETRY := $(shell command -v poetry 2>/dev/null)
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

run:
	poetry run python3 -m $(FTT_ENV_NAME)

ui:
	poetry run python3 -m $(FTT_ENV_NAME).ui

prepare-environment:
ifndef CONDA
	@echo "miniconda is not installed. Installing..."
	brew install miniconda
	conda init fish
endif

ifndef POETRY
	@echo "Poetry is not installed. Installing..."
	brew install poetry
endif

ifndef CONDA_LOCK
	@echo "conda-lock is not installed. Installing..."
	pip3 install conda-lock
	conda install -y -c conda-forge conda-lock
endif

ifndef FTT_ENV_CHECK
	conda create -y -n $(FTT_ENV_NAME)
endif

	python3 -m pip install --upgrade pip

conda-activate:
	$(CONDA_ACTIVATE) $(FTT_ENV_NAME)
	
install: prepare-environment conda-activate
	conda-lock install --name $(FTT_ENV_NAME) conda-lock.yml
	poetry install

update: install conda-activate
	conda env update -n $(FTT_ENV_NAME)
	poetry update

lock: prepare-environment
	conda-lock -f environment.yml -p osx-64 -p linux-64
	poetry lock --no-update

clean:
	rm -rf dist build .mypy_cache .pytest_cache
	find . -regex ".*/__pycache__" -exec rm -rf {} +
	find . -regex ".*\.egg-info" -exec rm -rf {} +
	find . -regex ".*/.coverage" -exec rm -rf {} +
	find . -regex ".*/.pytest_cache" -exec rm -rf {} +

remove:
	$(CONDA_ACTIVATE) base
	conda remove -y -n $(FTT_ENV_NAME) --all

test:
	poetry run pytest -s tests

lint:
	poetry run black ftt tests
	poetry run flake8 ftt
	poetry run mypy ftt

build: clean
	poetry build

package: clean
	pyinstaller --onefile \
	--hidden-import="sklearn.utils._typedefs" \
	--hidden-import="numpy" --copy-metadata=numpy \
	--copy-metadata=property_cached \
	--hidden-import=property_cached \
	--collect-all=property_cached \
	--collect-all=ftt \
	--name ftt \
	ftt/__main__.py