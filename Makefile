# Makefile for running typical developer workflow actions.
# To run actions in a subdirectory of the repo:
#   make lint build dir=translate/snippets
#
# Python version may also be specified in the command as 'py=3.10'


# Default values for make variables:
# dir will use repo root as working directory if not specified.
dir ?= $(shell pwd)
# python version: defaults to 3.11
py ?= "3.11"

INTERFACE_ACTIONS="build test lint"
repo_root = $(shell pwd)
.ONESHELL: #ease subdirectory work by using the same subshell for all commands
.-PHONY: *

# Export env vars used to determine cloud project.
export GOOGLE_CLOUD_PROJECT ?= ${GOOGLE_SAMPLE_PROJECT}
export BUILD_SPECIFIC_GCLOUD_PROJECT ?= ${GOOGLE_SAMPLE_PROJECT}

build:
	pip install nox
	cd ${dir}
	pip install -r requirements.txt

test: check-env build noxfile.py
	cd ${dir}
	nox $(NOXFLAGS) -s py-$(py)

lint: noxfile.py
	pip install nox black
	cd ${dir}
	nox $(NOXFLAGS) -s blacken
	nox $(NOXFLAGS) -s lint

# if no noxfile is present, we create one from the toplevel noxfile-template.py
noxfile.py:
	cd ${dir}
	cp ${repo_root}/noxfile-template.py noxfile.py

check-env:
ifndef GOOGLE_SAMPLE_PROJECT
	$(error GOOGLE_SAMPLE_PROJECT must be set to the name of a GCP project to use.)
endif
ifndef VIRTUAL_ENV
	$(error Use of a Python Virtual Environment is recommended. See README.md for details.)
endif

list-actions:
	@ echo ${INTERFACE_ACTIONS}

