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
import unittest

import create_client

from mock import Mock
from mock import patch
from oauth2client.client import GoogleCredentials


class CheckCreateClientTestCase(unittest.TestCase):
    """A test case for client creation."""

    def setUp(self):
        patcher1 = patch(
            'storage.storage_transfer.create_client.GoogleCredentials')
        patcher2 = patch(
            'storage.storage_transfer.create_client.discovery.build')
        self.mock_google_credentials = patcher1.start()
        self.mock_discovery = patcher2.start()
        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)

        self.mock_credentials = Mock(spec=GoogleCredentials)
        self.mock_google_credentials.get_application_default.return_value = \
            self.mock_credentials

    def test_create_client(self):
        create_client.create_transfer_client()
        self.mock_discovery.assert_called_with(
            'storagetransfer', 'v1',
            credentials=self.mock_credentials)
