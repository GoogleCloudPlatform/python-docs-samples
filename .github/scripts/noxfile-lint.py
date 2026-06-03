# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import os
import sys
import nox

# Use a stable Python version for running the style utilities
LINTING_VERSION = "3.10"

# Error out if the runner is missing the target python interpreter
nox.options.error_on_missing_interpreters = True


def _determine_local_import_names(start_dir: str) -> list[str]:
    """Determines local import names to assist Flake8 with import order checks."""
    try:
        file_ext_pairs = [os.path.splitext(path) for path in os.listdir(start_dir)]
        return [
            basename
            for basename, extension in file_ext_pairs
            if extension == ".py"
            or (os.path.isdir(os.path.join(start_dir, basename)) and basename != "__pycache__")
        ]
    except Exception:
        return []


# Standardize style configuration parameters
FLAKE8_COMMON_ARGS = [
    "--show-source",
    "--builtin=gettext",
    "--max-complexity=20",
    "--import-order-style=google",
    "--exclude=.nox,.cache,env,lib,generated_pb2,*_pb2.py,*_pb2_grpc.py",
    "--ignore=ANN101,ANN102,E121,E123,E126,E203,E226,E24,E266,E501,E704,W503,W504,I202",
    "--max-line-length=88",
]


@nox.session(python=LINTING_VERSION)
def lint(session: nox.sessions.Session) -> None:
    """Runs flake8 linting checks. Honors incremental PR file arguments."""
    session.install("flake8", "flake8-import-order")

    local_names = _determine_local_import_names(".")
    args = FLAKE8_COMMON_ARGS + [
        "--application-import-names",
        ",".join(local_names),
    ]

    if session.posargs:
        args.extend(session.posargs)
    else:
        args.append(".")

    session.run("flake8", *args)


@nox.session(python=LINTING_VERSION)
def blacken(session: nox.sessions.Session) -> None:
    """Runs black code formatting checks. Honors incremental PR file arguments."""
    session.install("black")
    
    # If explicit target files are passed via posargs, target ONLY those files.
    if session.posargs:
        targets = session.posargs
    else:
        # Fallback to scanning immediate root Python files if run purely locally without args
        targets = [path for path in os.listdir(".") if path.endswith(".py")]

    if targets:
        session.run("black", *targets)
    else:
        session.log("No specific Python targets identified for formatting validations.")
