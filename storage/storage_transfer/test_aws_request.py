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

from aws_request import main

from mock import Mock
from mock import patch


class AwsRequestTestCase(unittest.TestCase):
    """A test case for creating a TransferJob from AWS S3."""

    def setUp(self):
        patcher1 = patch(
            'storage.storage_transfer.aws_request.create_client')
        self.mock_create_client = patcher1.start()
        self.addCleanup(patcher1.stop)
        self.mock_client = Mock(spec=['transferJobs'])
        self.mock_create_client.create_transfer_client.return_value = \
            self.mock_client

    def test_create_aws_request(self):
        execute = self.mock_client.transferJobs.return_value.create.return_value \
            .execute
        execute.return_value = ""
        main()
        execute.assert_called_with()
