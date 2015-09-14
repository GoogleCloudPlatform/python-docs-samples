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
Common testing utilities between samples
"""

import contextlib
import json
import os
import sys
import tempfile
import unittest

from mock import patch
from nose.plugins.skip import SkipTest
from six.moves import cStringIO

try:
    APPENGINE_AVAILABLE = True
    from google.appengine.datastore import datastore_stub_util
    from google.appengine.ext import testbed
except ImportError:
    APPENGINE_AVAILABLE = False

BUCKET_NAME_ENV = 'TEST_BUCKET_NAME'
PROJECT_ID_ENV = 'TEST_PROJECT_ID'
RESOURCE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'resources')


# TODO: This can be written as a much simpler context manager.
class mock_input_answers(object):

    def __init__(self, list_, target):
        self.i = 0
        self.list_ = list_
        self.target = target

    def get_next_value(self, question):
        ret = self.list_[self.i]
        self.i += 1
        print('Responding to {} with {}'.format(question, ret))
        return u"{}".format(ret)

    def __enter__(self):
        self.patch = patch(self.target, self.get_next_value)
        self.patch.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.patch.__exit__(exc_type, exc_value, traceback)


class CloudBaseTest(unittest.TestCase):

    def setUp(self):
        self.resource_path = RESOURCE_PATH

        # A hack to prevent get_application_default from going GAE route.
        self._server_software_org = os.environ.get('SERVER_SOFTWARE')
        os.environ['SERVER_SOFTWARE'] = ''

        # Constants from environment
        test_bucket_name = os.environ.get(BUCKET_NAME_ENV, '')
        test_project_id = os.environ.get(PROJECT_ID_ENV, '')
        if not test_project_id or not test_bucket_name:
            raise Exception('You need to define an env var "%s" and "%s" to '
                            'run the test.'
                            % (PROJECT_ID_ENV, BUCKET_NAME_ENV))

        # Constants from resources/constants.json
        with open(
                os.path.join(RESOURCE_PATH, 'constants.json'),
                'r') as constants_file:

            self.constants = json.load(constants_file)
        self.constants['projectId'] = test_project_id
        self.constants['bucketName'] = test_bucket_name
        self.constants['cloudStorageInputURI'] = (
            self.constants['cloudStorageInputURI'] % test_bucket_name)
        self.constants['cloudStorageOutputURI'] = (
            self.constants['cloudStorageOutputURI'] % test_bucket_name)

    def tearDown(self):
        if self._server_software_org:
            os.environ['SERVER_SOFTWARE'] = self._server_software_org


class AppEngineTestbedCase(CloudBaseTest):
    """A base test case for common setup/teardown tasks for test."""
    def setUp(self):
        super(AppEngineTestbedCase, self).setUp()

        if not APPENGINE_AVAILABLE:
            raise SkipTest()

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
        self.testbed.init_user_stub()
        self.testbed.init_taskqueue_stub()

    def tearDown(self):
        super(AppEngineTestbedCase, self).tearDown()
        self.testbed.deactivate()

    def loginUser(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)


@contextlib.contextmanager
def capture_stdout():
    """Capture stdout."""
    fake_stdout = cStringIO()
    old_stdout = sys.stdout

    try:
        sys.stdout = fake_stdout
        yield fake_stdout
    finally:
        sys.stdout = old_stdout
