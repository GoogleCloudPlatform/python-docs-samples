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


""" DialogFlow CX: webhook to to configure new session parameters."""

# [START dialogflow_v3beta1_webhook_configure_session_parameters]

# TODO (developer): change entry point to configure_session_params in Cloud Function


def configure_session_params(request):
    """Webhook to validate or configure new session parameters."""

    request_dict = request.get_json()
    tag = request_dict["fulfillmentInfo"]["tag"]

    new_session_parameter = "Hi, I am new!"
    text = f"{new_session_parameter}. I'm a session parameter configured by the webhook. The webhook's tag is {tag}."

    json_response = {
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
                "newSessionParameter": new_session_parameter,
            },
        },
    }

    return json_response


# [END dialogflow_v3beta1_webhook_configure_session_parameters]
