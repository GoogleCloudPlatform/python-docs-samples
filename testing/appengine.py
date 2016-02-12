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
#

"""
Common testing tools for Google App Engine tests.
"""

import os
import tempfile

from nose.plugins.skip import SkipTest

try:
    APPENGINE_AVAILABLE = True
    from google.appengine.datastore import datastore_stub_util
    from google.appengine.ext import testbed
    from google.appengine.api import namespace_manager
except ImportError:
    APPENGINE_AVAILABLE = False


from .cloud import CloudTest


class AppEngineTest(CloudTest):
    """A base test case for common setup/teardown tasks for test."""
    def setUp(self):
        super(AppEngineTest, self).setUp()

        if not APPENGINE_AVAILABLE:
            raise SkipTest()

        # A hack to prevent get_application_default from going GAE route.
        self._server_software_org = os.environ.get('SERVER_SOFTWARE')
        os.environ['SERVER_SOFTWARE'] = ''

        # Setup the datastore and memcache stub.
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for
        # use.
        self.testbed.activate()
        # Create a consistency policy that will simulate the High
        # Replication consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub(
            datastore_file=tempfile.mkstemp()[1],
            consistency_policy=self.policy)
        self.testbed.init_memcache_stub()

        # Setup remaining stubs.
        self.testbed.init_app_identity_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_user_stub()
        self.testbed.init_taskqueue_stub(root_path='tests/resources')
        self.taskqueue_stub = self.testbed.get_stub(
            testbed.TASKQUEUE_SERVICE_NAME)
        self.testbed.init_logservice_stub()

    def tearDown(self):
        super(AppEngineTest, self).tearDown()

        if self._server_software_org:
            os.environ['SERVER_SOFTWARE'] = self._server_software_org

        self.testbed.deactivate()

    def login_user(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)

    def run_tasks(self):
        tasks = self.taskqueue_stub.get_filtered_tasks()
        for task in tasks:
            namespace = task.headers.get('X-AppEngine-Current-Namespace', '')
            previous_namespace = namespace_manager.get_namespace()
            try:
                namespace_manager.set_namespace(namespace)
                self.app.post(
                    task.url,
                    task.extract_params(),
                    headers={
                        k: v for k, v in task.headers.iteritems()
                        if k.startswith('X-AppEngine')})
            finally:
                namespace_manager.set_namespace(previous_namespace)
