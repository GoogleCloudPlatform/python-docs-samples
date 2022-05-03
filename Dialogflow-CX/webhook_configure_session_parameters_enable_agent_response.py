# Copyright 2022, Google LLC
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


""" DialogFlow CX: Configures a webhook to enable an agent response."""

# [START dialogflow_cx_v3_webhook_configure_session_parameters_enable_agent_response]

# TODO (developer): change entry point to enable_agent_response in Cloud Function


def enable_agent_response(request):
    """A webhook to enable an agent response."""

    request_dict = request.get_json()
    tag = request_dict["fulfillmentInfo"]["tag"]

    # The value of the parameter used to enable agent response:
    session_parameter = request_dict["sessionInfo"]["parameters"]["number"]

    if tag == "increase number":
        session_parameter += 100
        text = f"The new increased value of the number parameter is {session_parameter}"
    elif tag == "decrease number":
        session_parameter -= 50
        text = f"The new decreased value of the number parameter is {session_parameter}"

    return {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            # fulfillment text response to be sent to the agent
                            text
                        ],
                    },
                },
            ],
        },
        "sessionInfo": {
            "parameters": {
                "number": session_parameter,
            },
        },
    }


# [END dialogflow_cx_v3_webhook_configure_session_parameters_enable_agent_response]
