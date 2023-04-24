# Copyright 2016 Google Inc. All Rights Reserved.
#
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


import os
from unittest import mock

import access_token

PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']


@mock.patch('access_token.requests')
def test_main(requests_mock):
    metadata_response = mock.Mock()
    metadata_response.status_code = 200
    metadata_response.json.return_value = {
        'access_token': '123'
    }
    bucket_response = mock.Mock()
    bucket_response.status_code = 200
    bucket_response.json.return_value = [{'bucket': 'name'}]

    requests_mock.get.side_effect = [
        metadata_response, bucket_response]

    access_token.main(PROJECT)

    assert requests_mock.get.call_count == 2
