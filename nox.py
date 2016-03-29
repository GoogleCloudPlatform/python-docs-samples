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

SAMPLES = [
    'bigquery/api',
    'blog/introduction_to_data_models_in_cloud_datastore',
    'cloud_logging/api',
    'compute/api',
    'compute/autoscaler/demo',
    'datastore/api',
    'managed_vms/cloudsql',
    'managed_vms/datastore',
    'managed_vms/disk',
    'managed_vms/extending_runtime',
    'managed_vms/hello_world',
    'managed_vms/hello_world_compat',
    'managed_vms/memcache',
    'managed_vms/pubsub',
    'managed_vms/static_files',
    'managed_vms/storage',
    'monitoring/api',
    'storage/api',
]

GAE_SAMPLES = [
    'appengine/app_identity/signing',
    'appengine/bigquery',
    'appengine/blobstore',
    'appengine/cloudsql',
    'appengine/images',
    'appengine/localtesting',
    'appengine/logging/reading_logs',
    'appengine/logging/writing_logs',
    'appengine/mailgun',
    'appengine/memcache/guestbook',
    'appengine/multitenancy',
    'appengine/ndb/modeling',
    'appengine/ndb/overview',
    'appengine/ndb/transactions',
    'appengine/storage',
]


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
    for sample in (session.posargs or SAMPLES):
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

    for sample in (session.posargs or GAE_SAMPLES):
        session.run(
            'py.test', sample,
            *pytest_args,
            success_codes=[0, 5])  # Treat no test collected as success.


def session_travis(session):
    """On travis, just run with python3.4 and don't run slow or flaky tests."""
    session_tests(
        session, 'python3.4', extra_pytest_args=['-m not slow and not flaky'])
    session_gae(
        session, extra_pytest_args=['-m not slow and not flaky'])
