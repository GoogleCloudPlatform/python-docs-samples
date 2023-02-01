# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" DialogFlow CX long running operation code snippet """

## [START dialogflow_cx_long_running_snippet]
from google.cloud.dialogflowcx_v3.services.agents.client import AgentsClient
from google.cloud.dialogflowcx_v3.types.agent import ExportAgentRequest


def export_long_running_agent(project_id, agent_id, location):

    api_endpoint = f"{location}-dialogflow.googleapis.com:443"
    client_options = {"api_endpoint": api_endpoint}

    agents_client = AgentsClient(client_options=client_options)

    export_request = ExportAgentRequest()

    export_request.name = (
        f"projects/{project_id}/locations/{location}/agents/{agent_id}"
    )

    # export_agent returns a long running operation
    operation = agents_client.export_agent(request=export_request)

    # Returns the result of the operation when the operation is done
    return operation.result()


## [END dialogflow_cx_long_running_snippet]
