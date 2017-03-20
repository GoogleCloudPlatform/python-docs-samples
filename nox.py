# Copyright 2016 Google Inc. All Rights Reserved.
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
import tempfile

import nox

try:
    import ci_diff_helper
except ImportError:
    ci_diff_helper = None


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
        blacklist=set(['conftest.py', 'nox.py']),
        suffix='_test.py'):
    """Recursively collects a list of dirs that contain a file matching the
    given suffix.

    This works by listing the contents of directories and finding
    directories that have `*_test.py` files.
    """
    # Collect all the directories that have tests in them.
    for parent, subdirs, files in os.walk(start_dir):
        if any(f for f in files if f.endswith(suffix) and f not in blacklist):
            # Don't recurse further, since py.test will do that.
            del subdirs[:]
            # This dir has tests in it. yield it.
            yield parent
        else:
            # Filter out dirs we don't want to recurse into
            subdirs[:] = [
                s for s in subdirs
                if s[0].isalpha() and
                os.path.join(parent, s) not in blacklist]


def _get_changed_files():
    """Returns a list of files changed for this pull request / push.

    If running on a public CI like Travis or Circle this is used to only
    run tests/lint for changed files.
    """
    if not ci_diff_helper:
        return None

    try:
        config = ci_diff_helper.get_config()
    except OSError:  # Not on CI.
        return None

    changed_files = ci_diff_helper.get_changed_files('HEAD', config.base)

    changed_files = set([
        './{}'.format(filename) for filename in changed_files])

    return changed_files


def _filter_samples(sample_dirs, changed_files):
    """Filers the list of sample directories to only include directories that
    contain files in the list of changed files."""
    result = []
    for sample_dir in sample_dirs:
        for changed_file in changed_files:
            if changed_file.startswith(sample_dir):
                result.append(sample_dir)

    return list(set(result))


def _determine_local_import_names(start_dir):
    """Determines all import names that should be considered "local".

    This is used when running the linter to insure that import order is
    properly checked.
    """
    file_ext_pairs = [os.path.splitext(path) for path in os.listdir(start_dir)]
    return [
        basename
        for basename, extension
        in file_ext_pairs
        if extension == '.py' or os.path.isdir(
            os.path.join(start_dir, basename))
        and basename not in ('__pycache__')]

#
# App Engine specific helpers
#

_GAE_ROOT = os.environ.get('GAE_ROOT')
if _GAE_ROOT is None:
    _GAE_ROOT = tempfile.mkdtemp()


def _setup_appengine_sdk(session):
    """Installs the App Engine SDK, if needed."""
    session.env['GAE_SDK_PATH'] = os.path.join(_GAE_ROOT, 'google_appengine')
    session.run('gcprepotools', 'download-appengine-sdk', _GAE_ROOT)


#
# Test sessions
#


PYTEST_COMMON_ARGS = [
    '--cov',
    '--cov-config', os.path.abspath('.coveragerc'),
    '--cov-report', 'term']

FLAKE8_COMMON_ARGS = [
    '--show-source', '--builtin', 'gettext', '--max-complexity', '20',
    '--import-order-style', 'google',
    '--exclude', '.nox,.cache,env,lib,generated_pb2,*_pb2.py,*_pb2_grpc.py',
]

# Location of our common testing utilities. This isn't published to PyPI.
GCP_REPO_TOOLS_REQ =\
    'git+https://github.com/GoogleCloudPlatform/python-repo-tools.git'


# Collect sample directories.
ALL_TESTED_SAMPLES = sorted(list(_collect_dirs('.')))
ALL_SAMPLE_DIRECTORIES = sorted(list(_collect_dirs('.', suffix='.py')))
GAE_STANDARD_SAMPLES = [
    sample for sample in ALL_TESTED_SAMPLES
    if sample.startswith('./appengine/standard')]
NON_GAE_STANDARD_SAMPLES = sorted(
    list(set(ALL_TESTED_SAMPLES) - set(GAE_STANDARD_SAMPLES)))


# Filter sample directories if on a CI like Travis or Circle to only run tests
# for changed samples.
CHANGED_FILES = _get_changed_files()

if CHANGED_FILES is not None:
    print('Filtering based on changed files.')
    ALL_TESTED_SAMPLES = _filter_samples(
        ALL_TESTED_SAMPLES, CHANGED_FILES)
    ALL_SAMPLE_DIRECTORIES = _filter_samples(
        ALL_SAMPLE_DIRECTORIES, CHANGED_FILES)
    GAE_STANDARD_SAMPLES = _filter_samples(
        GAE_STANDARD_SAMPLES, CHANGED_FILES)
    NON_GAE_STANDARD_SAMPLES = _filter_samples(
        NON_GAE_STANDARD_SAMPLES, CHANGED_FILES)


def _session_tests(session, sample):
    """Runs py.test for a particular sample."""
    session.install('-r', 'testing/requirements.txt')
    session.install(GCP_REPO_TOOLS_REQ)

    session.chdir(sample)

    if os.path.exists(os.path.join(sample, 'requirements.txt')):
        session.install('-r', 'requirements.txt')

    session.run(
        'pytest',
        *(PYTEST_COMMON_ARGS + session.posargs),
        # Pytest will return 5 when no tests are collected. This can happen
        # on travis where slow and flaky tests are excluded.
        # See http://doc.pytest.org/en/latest/_modules/_pytest/main.html
        success_codes=[0, 5])


@nox.parametrize('sample', GAE_STANDARD_SAMPLES)
def session_gae(session, sample):
    """Runs py.test for an App Engine standard sample."""
    session.interpreter = 'python2.7'
    session.install(GCP_REPO_TOOLS_REQ)
    _setup_appengine_sdk(session)

    # Create a lib directory if needed, otherwise the App Engine vendor library
    # will complain.
    if not os.path.isdir(os.path.join(sample, 'lib')):
        os.mkdir(os.path.join(sample, 'lib'))

    _session_tests(session, sample)


@nox.parametrize('sample', NON_GAE_STANDARD_SAMPLES)
def session_py27(session, sample):
    """Runs py.test for a sample using Python 2.7"""
    session.interpreter = 'python2.7'
    _session_tests(session, sample)


@nox.parametrize('sample', NON_GAE_STANDARD_SAMPLES)
def session_py35(session, sample):
    """Runs py.test for a sample using Python 3.5"""
    session.interpreter = 'python3.5'
    _session_tests(session, sample)


@nox.parametrize('sample', ALL_SAMPLE_DIRECTORIES)
def session_lint(session, sample):
    """Runs flake8 on the sample."""
    session.install('flake8', 'flake8-import-order')

    local_names = _determine_local_import_names(sample)
    args = FLAKE8_COMMON_ARGS + [
        '--application-import-names', ','.join(local_names),
        '.']

    session.chdir(sample)
    session.run('flake8', *args)


#
# Utility sessions
#


def session_missing_tests(session):
    """Lists all sample directories that do not have tests."""
    session.virtualenv = False
    print('The following samples do not have tests:')
    for sample in set(ALL_SAMPLE_DIRECTORIES) - set(ALL_TESTED_SAMPLES):
        print('* {}'.format(sample))


SAMPLES_WITH_GENERATED_READMES = sorted(
    list(_collect_dirs('.', suffix='.rst.in')))


@nox.parametrize('sample', SAMPLES_WITH_GENERATED_READMES)
def session_readmegen(session, sample):
    """(Re-)generates the readme for a sample."""
    session.install('jinja2', 'pyyaml')

    if os.path.exists(os.path.join(sample, 'requirements.txt')):
        session.install('-r', os.path.join(sample, 'requirements.txt'))

    in_file = os.path.join(sample, 'README.rst.in')
    session.run('python', 'scripts/readme-gen/readme_gen.py', in_file)


def session_check_requirements(session):
    """Checks for out of date requirements and optionally updates them.

    This is intentionally not parametric, as it's desired to never have two
    samples with differing versions of dependencies.
    """
    session.install(GCP_REPO_TOOLS_REQ)

    if 'update' in session.posargs:
        command = 'update-requirements'
    else:
        command = 'check-requirements'

    reqfiles = list(_list_files('.', 'requirements*.txt'))

    for reqfile in reqfiles:
        session.run('gcprepotools', command, reqfile)
