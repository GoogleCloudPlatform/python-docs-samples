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


""" DialogFlow CX: webhook to configure new session parameters."""

# [START dialogflow_cx_v3_webhook_configure_session_parameters]

# TODO (developer): change entry point to configure_session_params in Cloud Function


def configure_session_params(request):
    """Webhook to validate or configure new session parameters."""

    order_number = 123

    json_response = {
        "sessionInfo": {
            "parameters": {
                "orderNumber": order_number,
            },
        },
    }

    return json_response


# [END dialogflow_cx_v3_webhook_configure_session_parameters]
