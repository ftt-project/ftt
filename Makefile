.ONESHELL:
SHELL=/bin/bash
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate
CONDA_CURRENT_ENV=source $$(conda info --base)/etc/profile.d/conda.sh; conda env list | grep '*'

FTT_ENV_NAME := ftt
PYTHON_VERSION := 3.10
FTT_ENV_CHECK := $(shell conda env list | grep ftt)
CONDA := $(shell command -v conda 2>/dev/null)
CONDA_LOCK := $(shell command -v conda-lock 2>/dev/null)
POETRY := $(shell command -v poetry 2>/dev/null)

prepare-environment:
	@echo "Preparing environment..."

ifndef CONDA
	@echo "miniconda is not installed. Installing..."
	brew install miniconda
	conda init fish
	conda init bash
endif

ifndef CONDA_LOCK
	@echo "CONDA_LOCK: False. Running 'conda install conda-lock...''"
	pip3 install conda-lock
	conda install -y -c conda-forge conda-lock
else
	@echo "CONDA_LOCK: True"
endif

ifndef FTT_ENV_CHECK
	@echo "FTT_ENV_CHECK: False. Running 'conda create ...''"
	conda create -y -n $(FTT_ENV_NAME) python=$(PYTHON_VERSION)
	@echo "FTT_ENV_CHECK: running 'conda-lock -f environment.yml ...'"
	conda-lock -f environment.yml
else
	@echo "FTT_ENV_CHECK: True"
endif


install: prepare-environment
	$(CONDA_ACTIVATE) $(FTT_ENV_NAME) \
		&& conda-lock install --name $(FTT_ENV_NAME) conda-lock.yml \
		&& poetry env use system \
		&& poetry install


remove:
	$(CONDA_ACTIVATE) base && \
		conda remove -y -n $(FTT_ENV_NAME) --all


update: install conda-activate
	$(CONDA_ACTIVATE) $(FTT_ENV_NAME) && \
		conda env update -n $(FTT_ENV_NAME) && \
		poetry update