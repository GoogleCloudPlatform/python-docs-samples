# Copyright 2022 Google LLC
#
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

"""
Demonstrates how to receive authenticated service-to-service requests, eg
for Cloud Run or Cloud Functions
"""

# [START cloudrun_service_to_service_receive]

from google.auth import jwt


def receive_authorized_get_request(request):
    """
    receive_authorized_get_request takes the "Authorization" header from a
    request, decodes it using the google-auth client library, and returns
    back the email from the header to the caller.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header:

        # split the auth type and value from the header.
        auth_type, creds = auth_header.split(" ", 1)

        if auth_type.lower() == "bearer":
            claims = jwt.decode(creds, verify=False)
            return f"Hello, {claims['email']}!\n"

        else:
            return f"Unhandled header format ({auth_type}).\n"
    return "Hello, anonymous user.\n"


# [END cloudrun_service_to_service_receive]
