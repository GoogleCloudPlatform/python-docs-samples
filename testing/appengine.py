# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Common testing tools for Google App Engine tests.
"""

import sys
import tempfile

try:
    APPENGINE_AVAILABLE = True
    from google.appengine.datastore import datastore_stub_util
    from google.appengine.ext import testbed
    from google.appengine.api import namespace_manager
except ImportError:
    APPENGINE_AVAILABLE = False


def setup_sdk_imports():
    """Sets up appengine SDK third-party imports."""
    if 'google' in sys.modules:
        # Some packages, such as protobuf, clobber the google
        # namespace package. This prevents that.
        reload(sys.modules['google'])

    # This sets up google-provided libraries.
    import dev_appserver
    dev_appserver.fix_sys_path()

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
    # Setup the datastore and memcache stub.
    # First, create an instance of the Testbed class.
    tb = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for
    # use.
    tb.activate()
    # Create a consistency policy that will simulate the High
    # Replication consistency model.
    policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
        probability=0)
    # Initialize the datastore stub with this policy.
    tb.init_datastore_v3_stub(
        datastore_file=tempfile.mkstemp()[1],
        consistency_policy=policy)
    tb.init_memcache_stub()

    # Setup remaining stubs.
    tb.init_app_identity_stub()
    tb.init_blobstore_stub()
    tb.init_user_stub()
    tb.init_logservice_stub()
    # tb.init_taskqueue_stub(root_path='tests/resources')
    tb.init_taskqueue_stub()
    tb.taskqueue_stub = tb.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    return tb


def run_tasks(testbed, app):
    tasks = testbed.taskqueue_stub.get_filtered_tasks()
    for task in tasks:
        namespace = task.headers.get('X-AppEngine-Current-Namespace', '')
        previous_namespace = namespace_manager.get_namespace()
        try:
            namespace_manager.set_namespace(namespace)
            app.post(
                task.url,
                task.extract_params(),
                headers={
                    k: v for k, v in task.headers.iteritems()
                    if k.startswith('X-AppEngine')})
        finally:
            namespace_manager.set_namespace(previous_namespace)
