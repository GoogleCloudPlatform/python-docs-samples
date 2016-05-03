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

import fnmatch
import os
import tempfile

import nox

REPO_TOOLS_REQ =\
    'git+https://github.com/GoogleCloudPlatform/python-repo-tools.git'

COMMON_PYTEST_ARGS = [
    '-x', '--no-success-flaky-report', '--cov', '--cov-config',
    '.coveragerc', '--cov-append', '--cov-report=']

# Speech is temporarily disabled.
SESSION_TESTS_BLACKLIST = set(('appengine', 'testing', 'speech'))


def session_lint(session):
    session.install('flake8', 'flake8-import-order')
    session.run(
        'flake8', '--builtin=gettext', '--max-complexity=10',
        '--import-order-style=google',
        '--exclude',
        'container_engine/django_tutorial/polls/migrations/*,.nox,.cache,env',
        *(session.posargs or ['.']))


def list_files(folder, pattern):
    for root, folders, files in os.walk(folder):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                yield os.path.join(root, filename)


def session_reqcheck(session):
    session.install(REPO_TOOLS_REQ)

    if 'update' in session.posargs:
        command = 'update-requirements'
    else:
        command = 'check-requirements'

    for reqfile in list_files('.', 'requirements*.txt'):
        session.run('gcprepotools', command, reqfile)


def collect_sample_dirs(start_dir, blacklist=set()):
    """Recursively collects a list of dirs that contain tests."""
    # Collect all the directories that have tests in them.
    for parent, subdirs, files in os.walk(start_dir):
        if any(f for f in files if f[-8:] == '_test.py'):
            # Don't recurse further, since py.test will do that.
            del subdirs[:]
            # This dir has tests in it. yield it.
            yield parent
        else:
            # Filter out dirs we don't want to recurse into
            subdirs[:] = [s for s in subdirs
                          if s[0].isalpha() and s not in blacklist]


@nox.parametrize('interpreter', ['python2.7', 'python3.4'])
def session_tests(session, interpreter, extra_pytest_args=None):
    session.interpreter = interpreter
    session.install(REPO_TOOLS_REQ)
    session.install('-r', 'requirements-{}-dev.txt'.format(interpreter))

    # extra_pytest_args can be send by another session calling this session,
    # see session_travis.
    pytest_args = COMMON_PYTEST_ARGS + (extra_pytest_args or [])

    # session.posargs is any leftover arguments from the command line, which
    # allows users to run a particular test instead of all of them.
    for sample in (session.posargs or
                   collect_sample_dirs('.', SESSION_TESTS_BLACKLIST)):

        # Install additional dependencies if they exist
        dirname = sample if os.path.isdir(sample) else os.path.dirname(sample)
        for reqfile in list_files(dirname, 'requirements*.txt'):
            session.install('-r', reqfile)

        session.run(
            'py.test', sample,
            *pytest_args,
            success_codes=[0, 5])  # Treat no test collected as success.


def session_gae(session, extra_pytest_args=None):
    session.interpreter = 'python2.7'
    session.install(REPO_TOOLS_REQ)
    session.install('-r', 'requirements-python2.7-dev.txt')

    # Install the app engine sdk and setup import paths.
    gae_root = os.environ.get('GAE_ROOT', tempfile.gettempdir())
    session.env['PYTHONPATH'] = os.path.join(gae_root, 'google_appengine')
    session.run('gcprepotools', 'download-appengine-sdk', gae_root)

    # Create a lib directory to prevent the GAE vendor library from
    # complaining.
    if not os.path.exists('lib'):
        os.makedirs('lib')

    pytest_args = COMMON_PYTEST_ARGS + (extra_pytest_args or [])

    for sample in (session.posargs or collect_sample_dirs('appengine')):

        # Install additional dependencies if they exist
        dirname = sample if os.path.isdir(sample) else os.path.dirname(sample)
        for reqfile in list_files(dirname, 'requirements*.txt'):
            session.install('-r', reqfile)

        session.run(
            'py.test', sample,
            *pytest_args,
            success_codes=[0, 5])  # Treat no test collected as success.


@nox.parametrize('subsession', ['gae', 'tests'])
def session_travis(session, subsession):
    """On travis, just run with python3.4 and don't run slow or flaky tests."""
    if subsession == 'tests':
        session_tests(
            session,
            'python3.4',
            extra_pytest_args=['-m not slow and not flaky'])
    else:
        session_gae(
            session,
            extra_pytest_args=['-m not slow and not flaky'])
