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
""" DialogFlow CX: webhook to log session ID for each request."""

# [START dialogflow_cx_v3_webhook_log_session_id]

import re


def log_session_id_for_troubleshooting(request):
    """Webhook will log session id corresponding to request."""

    req = request.get_json()
    # You can read more about SessionInfo at https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/SessionInfo
    # Use a regex pattern to get the session ID
    session_id_regex = r".+\/sessions\/(.+)"
    session = req["sessionInfo"]["session"]
    regex_match = re.search(session_id_regex, session)
    session_id = regex_match.group(1)

    # Instead of printing, use the logging tools available to you
    print(f"Debug Node: session ID = {session_id}")

    # Return a generic response
    res = {
        "fulfillment_response": {
            "messages": [{"text": {"text": [f"Request Session ID: {session_id}"]}}]
        }
    }

    # Returns json
    return res


# [END dialogflow_cx_v3_webhook_log_session_id]
