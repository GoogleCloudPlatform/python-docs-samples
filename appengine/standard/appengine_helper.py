# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Common testing tools for Google App Engine tests.
"""

import os
import sys
import tempfile

import pytest
import six


def setup_sdk_imports():
    """Sets up appengine SDK third-party imports."""
    if six.PY3:
        return

    sdk_path = os.environ.get('GAE_SDK_PATH')

    if not sdk_path:
        return

    if os.path.exists(os.path.join(sdk_path, 'google_appengine')):
        sdk_path = os.path.join(sdk_path, 'google_appengine')

    if 'google' in sys.modules:
        sys.modules['google'].__path__.append(
            os.path.join(sdk_path, 'google'))

    # This sets up libraries packaged with the SDK, but puts them last in
    # sys.path to prevent clobbering newer versions
    sys.path.append(sdk_path)
    import dev_appserver
    sys.path.extend(dev_appserver.EXTRA_PATHS)

    # Fixes timezone and other os-level items.
    import google.appengine.tools.os_compat
    (google.appengine.tools.os_compat)


def import_appengine_config():
    """Imports an application appengine_config.py. This is used to
    mimic the behavior of the runtime."""
    try:
        import appengine_config
        (appengine_config)
    except ImportError:
        pass


def setup_testbed():
    """Sets up the GAE testbed and enables common stubs."""
    from google.appengine.datastore import datastore_stub_util
    from google.appengine.ext import testbed as gaetestbed

    # Setup the datastore and memcache stub.
    # First, create an instance of the Testbed class.
    tb = gaetestbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for
    # use.
    tb.activate()
    # Create a consistency policy that will simulate the High
    # Replication consistency model.
    policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
        probability=1.0)
    # Initialize the datastore stub with this policy.
    tb.init_datastore_v3_stub(
        datastore_file=tempfile.mkstemp()[1],
        consistency_policy=policy)
    tb.init_memcache_stub()

    # Setup remaining stubs.
    tb.init_urlfetch_stub()
    tb.init_app_identity_stub()
    tb.init_blobstore_stub()
    tb.init_user_stub()
    tb.init_logservice_stub()
    # tb.init_taskqueue_stub(root_path='tests/resources')
    tb.init_taskqueue_stub()
    tb.taskqueue_stub = tb.get_stub(gaetestbed.TASKQUEUE_SERVICE_NAME)

    return tb


def run_taskqueue_tasks(testbed, app):
    """Runs tasks that are queued in the GAE taskqueue."""
    from google.appengine.api import namespace_manager

    tasks = testbed.taskqueue_stub.get_filtered_tasks()
    for task in tasks:
        namespace = task.headers.get('X-AppEngine-Current-Namespace', '')
        previous_namespace = namespace_manager.get_namespace()
        try:
            namespace_manager.set_namespace(namespace)
            app.post(
                task.url,
                task.extract_params(),
                headers=dict([
                    (k, v) for k, v in task.headers.iteritems()
                    if k.startswith('X-AppEngine')]))
        finally:
            namespace_manager.set_namespace(previous_namespace)


# py.test helpers

@pytest.fixture
def testbed():
    """py.test fixture for the GAE testbed."""
    testbed = setup_testbed()
    yield testbed
    testbed.deactivate()


@pytest.fixture
def login(testbed):
    """py.test fixture for logging in GAE users."""
    def _login(email='user@example.com', id='123', is_admin=False):
        testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)
    return _login


@pytest.fixture
def run_tasks(testbed):
    """py.test fixture for running GAE tasks."""
    def _run_tasks(app):
        run_taskqueue_tasks(testbed, app)
    return _run_tasks


def pytest_configure():
    """conftest.py hook function for setting up SDK imports."""
    setup_sdk_imports()


def pytest_runtest_call(item):
    """conftest.py hook for setting up appengine configuration."""
    import_appengine_config()
