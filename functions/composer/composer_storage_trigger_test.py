# Copyright 2019 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import mock
import composer_storage_trigger

# handles error in JSON body
@mock.patch('composer_storage_trigger.make_iap_request',
            side_effect=Exception('Bad request: JSON body error'))
def test_json_body_error(make_iap_request_mock):
    # Pass None, an input that is not valid JSON
    trigger_event = None
    with pytest.raises(Exception):
        composer_storage_trigger.trigger_dag(trigger_event)

# handles error in IAP response
@mock.patch('composer_storage_trigger.make_iap_request',
            side_effect=Exception('Error in IAP response: unauthorized'))
def test_iap_response_error(make_iap_request_mock):
    trigger_event = {'file': 'some-gcs-file'}
    with pytest.raises(Exception):
        composer_storage_trigger.trigger_dag(trigger_event)
