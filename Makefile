# Makefile
.DEFAULT_TARGET: help
.EXPORT_ALL_VARIABLES:
SHELL = bash

# Store the current date
DATE := $(shell date +%Y%m%d-%H%M%S)

# Add .local/bin to PATH
PATH := $(shell printenv PATH):${HOME}/.local/bin/

# Python Variables
VENV=.venv
PYTHON=${VENV}/bin/python3
SYSTEM_PYTHON=$(or $(shell which python3), $(shell which python))

# Application info, gets name and version from setup.cfg
PKG_NAME := $(shell grep -Poi 'name\s*=\s*\K([^\s]+)' setup.cfg)
PKG_VERSION := $(shell grep -Poi '^version\s*=\s*\K([^\s]+)' setup.cfg)

# MAKE FILE FORMAT
# TARGET: PREREQUISITE(S)
# <TAB> recipie

all: clean test


$(VENV):
	@mkdir -p .build
	@test -d $(VENV) || ${SYSTEM_PYTHON} -m venv $(VENV)
	@source ${VENV}/bin/activate
	@${VENV}/bin/pip install --upgrade setuptools wheel pip virtualenv
	@${VENV}/bin/python3 -m pip install -r requirements.txt

.PHONY: test
test: $(VENV)
	@${PYTHON} -m unittest discover -v tests

.PHONY: lint
lint: $(VENV)
	@${VENV}/bin/pylint --recursive=y ${PKG_NAME}/*.py

.PHONY: package
package: $(VENV)
	# Creates artifact and stores locally under dist
	@${PYTHON} setup.py sdist

.PHONY: run
run:
	@${PYTHON} -m ${PKG_NAME}/${PKG_NAME}.py

.PHONY: upgrade_pip
upgrade_pip:
	@${VENV}/bin/pip install --upgrade setuptools wheel pip virtualenv

.PHONY: publish
publish: $(VENV)
	@${VENV}/bin/twine upload --repository pypi dist/${PKG_NAME}-${PKG_VERSION}.tar.gz --verbose

.PHONY: clean
clean:
	@rm -fr $(VENV)
	@rm -fr venv
	@rm -fr .eggs
	@rm -fr .build
	@rm -fr dist
	@rm -fr */__pycache__

.PHONY: help
help:
	@echo 'Makefile for building application [${PKG_NAME}/${PKG_VERSION}]'
	@echo ''
	@echo 'Usage:'
	@echo '   make                    runs rules specified under all'
	@echo '   make all                cleans, inits venv, and test project'
	@echo "   make lint               runs lint on package source files"
	@echo "   make test               runs pylint on package source files"
	@echo "   make upgrade_pip        upgrades setuptools, wheel, pip, virtualenv"
	@echo "   make package            creates dist artifact"
	@echo "   make publish            publishes artifact to repo"
	@echo "   make deploy             uploads dist artifact to nexus"
	@echo '   make clean              removes venv and build related files'
	@echo '   make help               prints this message'
	@echo ''
