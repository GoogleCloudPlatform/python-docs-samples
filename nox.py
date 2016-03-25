import fnmatch
import os

import nox

REPO_TOOLS_REQ =\
    'git+https://github.com/GoogleCloudPlatform/python-repo-tools.git'


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


@nox.parametrize('interpreter', ['python2.7', 'python3.4'])
def session_tests(session, interpreter, extra_pytest_args=None):
    session.interpreter = interpreter
    session.install(REPO_TOOLS_REQ)
    session.install('-r', 'requirements-{}-dev.txt'.format(interpreter))

    pytest_args = COMMON_PYTEST_ARGS + (extra_pytest_args or [])

    for sample in (session.posargs or SAMPLES):
        session.run(
            'py.test', sample,
            *pytest_args,
            success_codes=[0, 5])  # Treat no test collected as success.


def session_travis(session):
    """On travis, just run with python3.4 and don't run slow or flaky tests."""
    session_tests(
        session, 'python3.4', extra_pytest_args=['-m not slow and not flaky'])
