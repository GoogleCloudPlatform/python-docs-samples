# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib

import nox

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

# https://github.com/psf/black/issues/2964, pin click version to 8.0.4 to
# avoid incompatiblity with black.
CLICK_VERSION = "click==8.0.4"
BLACK_VERSION = "black==19.3b0"
BLACK_PATHS = [
    "google",
    "tests",
    "tests_async",
    "noxfile.py",
    "setup.py",
    "docs/conf.py",
]


# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

#
# Style Checks
#


# Linting with flake8.
#
# We ignore the following rules:
#   E203: whitespace before ‘:’
#   E266: too many leading ‘#’ for block comment
#   E501: line too long
#   I202: Additional newline in a section of imports
#
# We also need to specify the rules which are ignored by default:
# ['E226', 'W504', 'E126', 'E123', 'W503', 'E24', 'E704', 'E121']
FLAKE8_COMMON_ARGS = [
    "--show-source",
    "--builtin=gettext",
    "--max-complexity=20",
    "--exclude=.nox,.cache,env,lib,generated_pb2,*_pb2.py,*_pb2_grpc.py",
    "--ignore=E121,E123,E126,E203,E226,E24,E266,E501,E704,W503,W504,I202",
    "--max-line-length=88",
]


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
def unit(session):
    # constraints_path = str(
    #     CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    # )
    session.install("-r", "requirements.txt")
    # session.install("-e", ".")
    session.run(
        "pytest",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "snippets_test.py",
        # "tests_async",
    )


@nox.session
def lint(session: nox.sessions.Session) -> None:
    session.install("flake8")

    args = FLAKE8_COMMON_ARGS + [
        ".",
    ]
    session.run("flake8", *args)
