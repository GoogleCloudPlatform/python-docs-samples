# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START dialogflow_list_test_case_results_sample]

from google.cloud.dialogflowcx_v3.services.test_cases.client import TestCasesClient
from google.cloud.dialogflowcx_v3.types.test_case import ListTestCaseResultsRequest


def list_test_case(project_id, agent_id, test_id, location):

    req = ListTestCaseResultsRequest()
    req.parent = f"projects/{project_id}/locations/{location}/agents/{agent_id}/testCases/{test_id}"
    req.filter = "environment=draft"
    client = TestCasesClient(
        client_options={"api_endpoint": f"{location}-dialogflow.googleapis.com"}
    )
    # Makes a call to list all test case results that match filter
    result = client.list_test_case_results(request=req)
    print(result)
    return result


# [END dialogflow_list_test_case_results_sample]
