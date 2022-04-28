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


""" DialogFlow CX: webhook to validate or invalidate form parameters snippet."""

# [START dialogflow_v3beta1_webhook_validate_form_parameter]

# TODO (developer): change entry point to validate_parameter in Cloud Function


def validate_parameter(request):
    """# Webhook to validate or invalidate parameter based on conditions configured by the user."""

    request_dict = request.get_json()
    param_to_validate = request_dict["pageInfo"]["formInfo"]["parameterInfo"][0][
        "value"
    ]

    if param_to_validate > 15:
        text = "That is too many! Please pick another number."
        param_state = "INVALID"
    else:
        text = "That is a number I can work with!"
        param_state = "VALID"

    json_response = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            text
                        ],  # fulfillment text response to be sent to the agent
                    },
                },
            ],
        },
        "page_info": {
            "form_info": {
                "parameter_info": [
                    {
                        "displayName": "paramToValidate",
                        "required": True,
                        "state": param_state,
                    },
                ],
            },
        },
        "sessionInfo": {
            "parameters": {
                # Set session parameter to null if your agent needs to reprompt the user
                "paramToValidate": None
            },
        },
    }

    return json_response


# [END dialogflow_v3beta1_webhook_validate_form_parameter]
