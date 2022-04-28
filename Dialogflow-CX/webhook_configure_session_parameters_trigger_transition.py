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


""" DialogFlow CX: Configure new session parameters with trigger transition."""

# [START dialogflow_v3beta1_webhook_configure_session_parameters_trigger_transition]

# TODO (developer): change entry point to trigger_transition in Cloud Function


def trigger_transition(request):
    """Webhook to validate or configure new session parameters."""

    request_dict = request.get_json()
    session_parameter = request_dict["sessionInfo"]["parameters"].get("value", 25)

    if session_parameter > 15:
        text = f"You said {session_parameter}. Let me redirect you to our higher number department"
        target_page = (
            "projects/<Project ID>/locations/<Location ID>/"
            "agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>"
        )
    else:
        text = f"{session_parameter} is a number I can help you with!"
        target_page = (
            "projects/<Project ID>/locations/<Location ID>/"
            "agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>"
        )

    json_response = {
        "target_page": target_page,
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
    }

    return json_response


# [END dialogflow_v3beta1_webhook_configure_session_parameters_trigger_transition]
