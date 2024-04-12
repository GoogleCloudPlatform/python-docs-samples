# Makefile for running typical developer workflow actions.
# To run actions in a subdirectory of the repo:
#   make lint build dir=translate/snippets
#
# Python version may also be specified in the command as 'py=3.10'


# Default values for make variables:
# dir will use repo root as working directory if not specified.
dir ?= $(shell pwd)
# python version: defaults to 3.11
py ?= 3.11

INTERFACE_ACTIONS="build test lint"
repo_root = $(shell pwd)
.ONESHELL: #ease subdirectory work by using the same subshell for all commands
.-PHONY: *

# GOOGLE_SAMPLES_PROJECT takes precedence over GOOGLE_CLOUD_PROJECT
PROJECT_ID = ${GOOGLE_SAMPLES_PROJECT}
ifeq (${PROJECT_ID},)
PROJECT_ID = ${GOOGLE_CLOUD_PROJECT}
endif
# export our project ID as GOOGLE_CLOUD_PROJECT in the action environment
override GOOGLE_CLOUD_PROJECT := ${PROJECT_ID}
export GOOGLE_CLOUD_PROJECT
export BUILD_SPECIFIC_GCLOUD_PROJECT ?= ${PROJECT_ID}

build: check-env
	pip install nox
	cd ${dir}

test: check-env build noxfile.py
# kokoro uses $RUN_TESTS_SESSION to indicate which session to run.
# for local use, use a suitable default.
ifndef RUN_TESTS_SESSION
	cd ${dir}
	nox -s py-$(py)
else
	cd ${dir}
	nox -s ${RUN_TESTS_SESSION}
endif

lint: check-env noxfile.py
	pip install nox black
	cd ${dir}
	nox -s blacken
	nox -s lint

# if no noxfile is present, we create one from the toplevel noxfile-template.py
noxfile.py:
	cd ${dir}
	cp -n ${repo_root}/noxfile-template.py noxfile.py

check-env:
ifndef PROJECT_ID
	$(error At least one of the following env vars must be set: GOOGLE_SAMPLES_PROJECT, GOOGLE_CLOUD_PROJECT.)
endif
ifndef VIRTUAL_ENV
	$(warning Use of a Python Virtual Environment is recommended. See README.md for details.)
endif

list-actions:
	@ echo ${INTERFACE_ACTIONS}

