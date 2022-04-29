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


""" DialogFlow CX: webhook to configure optional or required form parameters."""

# [START dialogflow_v3beta1_webhook_configure_optional_or_required_form_params]

# TODO (developer): change entry point to configure_optional_form_param in Cloud Function


def configure_optional_form_param(request):
    """Webhook to configure optional or required form parameters."""

    request_dict = request.get_json()
    form_parameter = request_dict["pageInfo"]["formInfo"]["parameterInfo"][0]["value"]
    is_param_required = True
    param_state = "VALID"

    if form_parameter <= 15:
        text = f"{form_parameter} is a number I can work with!"

    if form_parameter > 15 and form_parameter < 20:
        text = f"{form_parameter} is too many, but it's okay. Let's move on."
        is_param_required = False
    else:
        text = f"{form_parameter} isn't going to work for me. Please try again!"
        param_state = "INVALID"
        form_parameter = None

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
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [
                    {
                        "displayName": form_parameter,
                        # if required: false, the agent will not reprompt for
                        # this parameter, even if the state is 'INVALID'
                        "required": is_param_required,
                        "state": param_state,
                    },
                ],
            },
        },
        "sessionInfo": {
            "parameterInfo": {
                # Set session parameter to null if you want to reprompt
                # the user to enter a required parameter
                "formParameter": form_parameter,
            },
        },
    }
    return json_response


# [END dialogflow_v3beta1_webhook_configure_optional_or_required_form_params]
