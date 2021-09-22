# Copyright 2021, Google LLC
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


import google.auth

from list_testcase_results import list_test_case

LOCATION = "global"

_, PROJECT_ID = google.auth.default()
AGENT_ID = "143dee60-56fe-4191-a8d8-095f569f6cd8"
TEST_ID = "3c48d39e-71c0-4cb0-b974-3d5c596d347e"


def test_list_testcase_results():
    result = list_test_case(PROJECT_ID, AGENT_ID, TEST_ID, LOCATION)

    assert "Hello! How can I help you?" in str(result)
