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

# [START dialogflow_set_agent_sample]

from google.cloud.dialogflow_v2 import Agent, AgentsClient


def set_agent(project_id, display_name):

    agents_client = AgentsClient()

    parent = agents_client.common_project_path(project_id)

    agent = Agent(
        parent=parent,
        display_name=display_name,
        default_language_code="en",
        time_zone="America/Los_Angeles",
    )

    response = agents_client.set_agent(request={"agent": agent})

    return response


# [END dialogflow_set_agent_sample]
