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


"""DialogFlow API Create Agent Sample"""

## [START dialogflow_cx_create_agent_sample]
from google.cloud.dialogflowcx_v3.services.agents.client import AgentsClient
from google.cloud.dialogflowcx_v3.types.agent import Agent


def create_agent(project_id, display_name):

    parent = "projects/" + project_id + "/locations/global"

    agents_client = AgentsClient()

    agent = Agent(
        display_name=display_name,
        default_language_code="en",
        time_zone="America/Los_Angeles",
    )

    response = agents_client.create_agent(request={"agent": agent, "parent": parent})

    return response


## [END dialogflow_cx_create_agent_sample]
