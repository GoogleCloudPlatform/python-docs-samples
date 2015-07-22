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

from mock import Mock

from transfer_check import check_operation


class CheckTransferTestCase(unittest.TestCase):
    """A test case for querying transfer job completion."""

    def test_check_operation(self):
        mock_client = Mock(spec=['transferOperations'])
        execute = mock_client.transferOperations.return_value.list.return_value \
            .execute
        project_id = ""
        job_name = ""
        check_operation(mock_client, project_id, job_name)
        execute.assert_called_with()
