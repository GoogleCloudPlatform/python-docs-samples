# Copyright 2023 Google LLC
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


""" DialogFlow CX: webhook to validate or invalidate form parameters snippet."""


# [START dialogflow_cx_v3_webhook_validate_form_parameter]


def validate_parameter(request):
    """Webhook will validate or invalidate parameter based on logic configured by the user."""
    return {
        "page_info": {
            "form_info": {
                "parameter_info": [
                    {
                        "displayName": "orderNumber",
                        "required": True,
                        "state": "INVALID",
                        "value": 123,
                    },
                ],
            },
        },
        "sessionInfo": {
            "parameters": {
                # Set session parameter to None if the form parameter is 'INVALID' and your agent needs to reprompt the user
                "orderNumber": None,
            },
        },
    }


# [END dialogflow_cx_v3_webhook_validate_form_parameter]
