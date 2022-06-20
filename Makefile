.ONESHELL:

CONDA := $(shell command -v conda 2>/dev/null)
CONDA_LOCK := $(shell command -v conda-lock 2>/dev/null)
POETRY := $(shell command -v poetry 2>/dev/null)
FTT_ENV := $(shell conda env list | grep ftt)
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

run:
	poetry run python -m ftt

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
	conda install -y -c conda-forge conda-lock
endif

ifndef FTT_ENV
	conda create -y -n ftt
endif

	python -m pip install --upgrade pip

conda-activate:
	$(CONDA_ACTIVATE) ftt
	
install: prepare-environment conda-activate
	conda-lock install --name ftt conda-lock.yml
	poetry install

update: install conda-activate
	conda env update -n ftt
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
	conda remove -y -n ftt --all

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