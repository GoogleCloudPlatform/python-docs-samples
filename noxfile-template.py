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

from __future__ import print_function

import fnmatch
import os
from pathlib import Path
import tempfile

import nox

# Get root of this repository. Assume we don't have directories nested deeper than 10 items.
p = Path(os.getcwd())
for i in range(10):
    if p is None:
        raise Exception("Unable to detect repository root.")
    if Path(p / ".git").exists():
        REPO_ROOT = str(p)
        break
    p = p.parent

#
# Helpers and utility functions
#


def _list_files(folder, pattern):
    """Lists all files below the given folder that match the pattern."""
    for root, folders, files in os.walk(folder):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                yield os.path.join(root, filename)


def _collect_dirs(
    start_dir,
    blacklist=set(["conftest.py", "noxfile.py", "lib", "third_party"]),
    suffix="requirements.txt",
    recurse_further=False,
):
    """Recursively collects a list of dirs that contain a file matching the
    given suffix.

    This works by listing the contents of directories and finding
    directories that have `"requirements.text` files.
    """
    # Collect all the directories that have tests in them.
    for parent, subdirs, files in os.walk(start_dir):
        if "./." in parent:
            continue  # Skip top-level dotfiles
        elif any(f for f in files if f.endswith(suffix) and f not in blacklist):
            # Don't recurse further for tests, since py.test will do that.
            if not recurse_further:
                del subdirs[:]
            # This dir has desired files in it. yield it.
            yield parent
        else:
            # Filter out dirs we don't want to recurse into
            subdirs[:] = [s for s in subdirs if s[0].isalpha() and s not in blacklist]


def _determine_local_import_names(start_dir):
    """Determines all import names that should be considered "local".

    This is used when running the linter to insure that import order is
    properly checked.
    """
    file_ext_pairs = [os.path.splitext(path) for path in os.listdir(start_dir)]
    return [
        basename
        for basename, extension in file_ext_pairs
        if extension == ".py"
        or os.path.isdir(os.path.join(start_dir, basename))
        and basename not in ("__pycache__")
    ]


#
# App Engine specific helpers
#


_GAE_ROOT = os.environ.get("GAE_ROOT")
if _GAE_ROOT is None:
    _GAE_ROOT = tempfile.mkdtemp()


def _setup_appengine_sdk(session):
    """Installs the App Engine SDK, if needed."""
    session.env["GAE_SDK_PATH"] = os.path.join(_GAE_ROOT, "google_appengine")
    session.run("gcp-devrel-py-tools", "download-appengine-sdk", _GAE_ROOT)


#
# Test sessions
#


PYTEST_COMMON_ARGS = ["--junitxml=sponge_log.xml"]

# Ignore I202 "Additional newline in a section of imports." to accommodate
# region tags in import blocks. Since we specify an explicit ignore, we also
# have to explicitly ignore the list of default ignores:
# `E121,E123,E126,E226,E24,E704,W503,W504` as shown by `flake8 --help`.
FLAKE8_COMMON_ARGS = [
    "--show-source",
    "--builtin",
    "gettext",
    "--max-complexity",
    "20",
    "--import-order-style",
    "google",
    "--exclude",
    ".nox,.cache,env,lib,generated_pb2,*_pb2.py,*_pb2_grpc.py",
    "--ignore=E121,E123,E126,E203, E226,E24,E266,E501,E704,W503,W504,I100,I201,I202",
]


# Collect sample directories.
ALL_TESTED_SAMPLES = sorted(list(_collect_dirs(".")))

GAE_STANDARD_SAMPLES = [
    sample
    for sample in ALL_TESTED_SAMPLES
    if str(Path(sample).absolute().relative_to(REPO_ROOT)).startswith(
        "appengine/standard/"
    )
]
PY3_ONLY_SAMPLES = [
    sample
    for sample in ALL_TESTED_SAMPLES
    if (
        str(Path(sample).absolute().relative_to(REPO_ROOT)).startswith(
            "appengine/standard_python37"
        )
        or str(Path(sample).absolute().relative_to(REPO_ROOT)).startswith("functions/")
        or str(Path(sample).absolute().relative_to(REPO_ROOT)).startswith(
            "bigquery/pandas-gbq-migration"
        )
    )
]
NON_GAE_STANDARD_SAMPLES_PY2 = sorted(
    list((set(ALL_TESTED_SAMPLES) - set(GAE_STANDARD_SAMPLES)) - set(PY3_ONLY_SAMPLES))
)
NON_GAE_STANDARD_SAMPLES_PY3 = sorted(
    list(set(ALL_TESTED_SAMPLES) - set(GAE_STANDARD_SAMPLES))
)


def _session_tests(session, sample, post_install=None):
    """Runs py.test for a particular sample."""
    session.install("-r", REPO_ROOT + "/testing/requirements.txt")

    session.chdir(sample)

    if os.path.exists("requirements.txt"):
        session.install("-r", "requirements.txt")

    if post_install:
        post_install(session)

    session.run(
        "pytest",
        *(PYTEST_COMMON_ARGS + session.posargs),
        # Pytest will return 5 when no tests are collected. This can happen
        # on travis where slow and flaky tests are excluded.
        # See http://doc.pytest.org/en/latest/_modules/_pytest/main.html
        success_codes=[0, 5]
    )


@nox.session(python="2.7")
@nox.parametrize("sample", GAE_STANDARD_SAMPLES)
def gae(session, sample):
    """Runs py.test for an App Engine standard sample."""

    # Create a lib directory if needed, otherwise the App Engine vendor library
    # will complain.
    if not os.path.isdir(os.path.join(sample, "lib")):
        os.mkdir(os.path.join(sample, "lib"))

    _session_tests(session, sample, _setup_appengine_sdk)


@nox.session(python="2.7")
@nox.parametrize("sample", NON_GAE_STANDARD_SAMPLES_PY2)
def py2(session, sample):
    """Runs py.test for a sample using Python 2.7"""
    _session_tests(session, sample)


@nox.session(python=["3.5", "3.6", "3.7"])
@nox.parametrize("sample", NON_GAE_STANDARD_SAMPLES_PY3)
def py3(session, sample):
    """Runs py.test for a sample using Python 3.x"""
    _session_tests(session, sample)


BLACK_VERSION = "black==19.3b0"


@nox.session(python="3.6")
def lint(session):
    """Checks if blacken would result in any changes in the sample."""
    session.install("flake8", "flake8-import-order", BLACK_VERSION)

    session.run("black", "--check", ".")

    local_names = _determine_local_import_names(".")
    args = FLAKE8_COMMON_ARGS + [
        "--application-import-names",
        ",".join(local_names),
        ".",
    ]
    session.run("flake8", *args)


@nox.session(python="3.6")
def blacken(session):
    """Run black.
    Format code to uniform standard.
    """
    session.install(BLACK_VERSION)
    session.run("black", ".")


SAMPLES_WITH_GENERATED_READMES = sorted(list(_collect_dirs(".", suffix=".rst.in")))


@nox.session
@nox.parametrize("sample", SAMPLES_WITH_GENERATED_READMES)
def readmegen(session, sample):
    """(Re-)generates the readme for a sample."""
    session.install("jinja2", "pyyaml")

    if os.path.exists(os.path.join(sample, "requirements.txt")):
        session.install("-r", os.path.join(sample, "requirements.txt"))

    in_file = os.path.join(sample, "README.rst.in")
    session.run("python", REPO_ROOT + "/scripts/readme-gen/readme_gen.py", in_file)
