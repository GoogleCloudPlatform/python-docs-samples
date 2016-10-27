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

"""
Noxfile used with nox-automation to run tests across all samples.

Use nox -l to see all possible sessions.

In general, you'll want to run:

    nox -s lint
    # or
    nox -s list -- /path/to/sample/dir

And:

    nox -s tests -- /path/to/sample/dir

"""

import fnmatch
import os
import subprocess
import tempfile

import nox

# Location of our common testing utilities. This isn't published to PyPI.
REPO_TOOLS_REQ =\
    'git+https://github.com/GoogleCloudPlatform/python-repo-tools.git'

# Arguments used for every invocation of py.test.
COMMON_PYTEST_ARGS = [
    '-x', '--no-success-flaky-report', '--cov', '--cov-config',
    '.coveragerc', '--cov-append', '--cov-report=']


# Libraries that only work on Python 2.7
PY27_ONLY_LIBRARIES = ['mysql-python']

# Whether we're running on Travis CI
ON_TRAVIS = os.environ.get('TRAVIS', False)


def list_files(folder, pattern):
    """Lists all files below the given folder that match the pattern."""
    for root, folders, files in os.walk(folder):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                yield os.path.join(root, filename)


def collect_sample_dirs(start_dir, blacklist=set(), suffix='_test.py'):
    """Recursively collects a list of dirs that contain tests.

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
            subdirs[:] = [s for s in subdirs
                          if s[0].isalpha() and
                          os.path.join(parent, s) not in blacklist]


def get_changed_files():
    """Uses travis environment variables to determine which files
    have changed for this pull request / push."""
    # Debug info
    print('TRAVIS_PULL_REQUEST: {}'.format(
        os.environ.get('TRAVIS_PULL_REQUEST')))
    print('TRAVIS_COMMIT: {}'.format(os.environ.get('TRAVIS_COMMIT')))
    print('TRAVIS_BRANCH: {}'.format(os.environ.get('TRAVIS_BRANCH')))

    pr = os.environ.get('TRAVIS_PULL_REQUEST')
    if pr == 'false':
        # This is not a pull request.
        changed = subprocess.check_output(
            ['git', 'show', '--pretty=format:', '--name-only',
                os.environ.get('TRAVIS_COMMIT')])

    elif pr is not None:
        try:
            changed = subprocess.check_output(
                ['git', 'diff', '--name-only',
                    os.environ.get('TRAVIS_COMMIT'),
                    os.environ.get('TRAVIS_BRANCH')])

        except subprocess.CalledProcessError:
            # Fallback to git head.
            git_head = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD']).strip()

            print('Falling back to HEAD: {}'.format(git_head))

            changed = subprocess.check_output(
                ['git', 'diff', '--name-only',
                    git_head,
                    os.environ.get('TRAVIS_BRANCH')])
    else:
        changed = ''
        print('Uh... where are we?')
    return set([x for x in changed.split('\n') if x])


def filter_samples(sample_dirs, changed_files):
    """Filers the list of sample directories to only include directories that
    contain changed files."""
    result = []
    for sample_dir in sample_dirs:
        if sample_dir.startswith('./'):
            sample_dir = sample_dir[2:]
        for changed_file in changed_files:
            if changed_file.startswith(sample_dir):
                result.append(sample_dir)

    return list(set(result))


def setup_appengine(session):
    """Installs the App Engine SDK."""
    # Install the app engine sdk and setup import paths.
    if session.interpreter.startswith('python3'):
        return

    gae_root = os.environ.get('GAE_ROOT', tempfile.gettempdir())
    session.env['GAE_SDK_PATH'] = os.path.join(gae_root, 'google_appengine')
    session.run('gcprepotools', 'download-appengine-sdk', gae_root)

    # Create a lib directory to prevent the GAE vendor library from
    # complaining.
    if not os.path.exists('lib'):
        os.makedirs('lib')


def run_tests_in_sesssion(
        session, interpreter, sample_directories, use_appengine=True,
        skip_flaky=False):
    """This is the main function for executing tests.

    It:
    1. Install the common testing utilities.
    2. Installs the test requirements.
    3. Determines which pytest arguments to use. skip_flaky causes extra
       arguments to be passed that will skip tests marked flaky.
    7. For each sample directory, it runs py.test.
    """
    session.interpreter = interpreter
    session.install(REPO_TOOLS_REQ)
    session.install('-r', 'testing/requirements-dev.txt')

    if use_appengine:
        setup_appengine(session)

    pytest_args = COMMON_PYTEST_ARGS[:]

    if skip_flaky:
        pytest_args.append('-m not slow and not flaky')

    for sample in sample_directories:
        # Ignore lib and env directories
        ignore_args = [
            '--ignore', os.path.join(sample, 'lib'),
            '--ignore', os.path.join(sample, 'env')]

        # output junit report.
        junit_args = ['--junitxml', os.path.join(sample, 'junit.xml')]

        session.run(
            'py.test', sample,
            *(pytest_args + ignore_args + junit_args),
            success_codes=[0, 5])  # Treat no test collected as success.


@nox.parametrize('interpreter', ['python2.7', 'python3.5'])
def session_tests(session, interpreter):
    """Runs tests for all non-gae standard samples."""
    # session.posargs is any leftover arguments from the command line,
    # which allows users to run a particular test instead of all of them.
    sample_directories = session.posargs
    if not sample_directories:
        sample_directories = collect_sample_dirs('.')

    run_tests_in_sesssion(
        session, interpreter, sample_directories)


def session_gae(session):
    """Runs test for GAE Standard samples."""
    sample_directories = collect_sample_dirs('appengine/standard')
    run_tests_in_sesssion(
        session, 'python2.7', sample_directories, use_appengine=True)


@nox.parametrize('subsession', ['gae', 'tests'])
def session_travis(session, subsession):
    """On travis, just run with python3.5 and don't run slow or flaky tests."""
    if subsession == 'tests':
        interpreter = 'python3.5'
        sample_directories = collect_sample_dirs(
            '.', set('./appengine/standard'))
    elif subsession == 'gae':
        interpreter = 'python2.7'
        sample_directories = collect_sample_dirs('appengine/standard')

    changed_files = get_changed_files()
    sample_directories = filter_samples(
        sample_directories, changed_files)

    if not sample_directories:
        print('No samples changed.')
        return

    print('Running tests on a subset of samples: ')
    print('\n'.join(sample_directories))

    run_tests_in_sesssion(
        session, interpreter, sample_directories, skip_flaky=True)


def session_lint(session):
    """Lints each sample."""
    sample_directories = session.posargs
    if not sample_directories:
        # The top-level dir isn't a sample dir - only its subdirs.
        _, subdirs, _ = next(os.walk('.'))
        sample_directories = (
            sample_dir for subdir in subdirs if not subdir.startswith('.')
            for sample_dir in collect_sample_dirs(
                    subdir, suffix='.py', blacklist='conftest.py'))

    # On travis, only lint changed samples.
    if ON_TRAVIS:
        changed_files = get_changed_files()
        sample_directories = filter_samples(
            sample_directories, changed_files)

    session.install('flake8', 'flake8-import-order')

    for sample_directory in sample_directories:
        # Determine local import names
        local_names = [
            basename
            for basename, extension
            in [os.path.splitext(path) for path
                in os.listdir(sample_directory)]
            if extension == '.py' or os.path.isdir(
                os.path.join(sample_directory, basename))]

        session.run(
            'flake8',
            '--show-source',
            '--builtin', 'gettext',
            '--max-complexity', '15',
            '--import-order-style', 'google',
            '--exclude', '.nox,.cache,env,lib',
            '--application-import-names', ','.join(local_names),
            sample_directory)


def session_reqcheck(session):
    """Checks for out of date requirements."""
    session.install(REPO_TOOLS_REQ)

    if 'update' in session.posargs:
        command = 'update-requirements'
    else:
        command = 'check-requirements'

    reqfiles = list(list_files('.', 'requirements*.txt'))
    reqfiles.append('requirements-dev.in')

    for reqfile in reqfiles:
        session.run('gcprepotools', command, reqfile)


def session_reqrollup(session):
    """Rolls up all requirements files into requirements-dev.txt.

    This does not test for uniqueness. pip itself will validate that.
    """
    requirements = set()
    requirements_files = list(list_files('.', 'requirements*.txt'))
    requirements_files.append('./testing/requirements-dev.in')

    for filename in requirements_files:
        if filename == './testing/requirements-dev.txt':
            continue

        with open(filename, 'r') as f:
            lines = f.readlines()
        requirements.update(lines)

    def mark_if_necessary(requirement):
        """Adds environment markers to Python 2.7-only libraries."""
        for library in PY27_ONLY_LIBRARIES:
            if requirement.startswith(library):
                return '{}; python_version == \'2.7\'\n'.format(
                    requirement.strip())
        return requirement

    requirements = [
        mark_if_necessary(requirement) for requirement in requirements]

    with open('testing/requirements-dev.txt', 'w') as f:
        f.write('# This file is generated by nox -s reqrollup. Do not edit.\n')
        for requirement in sorted(requirements, key=lambda s: s.lower()):
            if not requirement.startswith('#'):
                f.write(requirement)


def session_readmegen(session):
    session.install('-r', 'testing/requirements-dev.txt')

    in_files = list(list_files('.', 'README.rst.in'))

    for in_file in in_files:
        session.run('python', 'scripts/readme-gen/readme_gen.py', in_file)
