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

"""Demonstrates how to receive authenticated service-to-service requests.

For example for Cloud Run or Cloud Functions.
"""

# This sample will be migrated to app.py

# [START auth_validate_and_decode_bearer_token_on_flask]
# [START cloudrun_service_to_service_receive]
from flask import Request

from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token


def receive_request_and_parse_auth_header(request: Request) -> str:
    """Parse the authorization header, validate the Bearer token
    and decode the token to get its information.

    Args:
        request: Flask request object.

    Returns:
        One of the following:
        a) The email from the request's Authorization header.
        b) A welcome message for anonymous users.
        c) An error description.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header:
        # Split the auth type and value from the header.
        auth_type, creds = auth_header.split(" ", 1)

        if auth_type.lower() == "bearer":
            # Find more information about `verify_token` function here:
            # https://google-auth.readthedocs.io/en/master/reference/google.oauth2.id_token.html#google.oauth2.id_token.verify_token
            try:
                decoded_token = id_token.verify_token(creds, requests.Request())
                return f"Hello, {decoded_token['email']}!\n"
            except GoogleAuthError as e:
                return f"Invalid token: {e}\n"
        else:
            return f"Unhandled header format ({auth_type}).\n"

    return "Hello, anonymous user.\n"
# [END cloudrun_service_to_service_receive]
# [END auth_validate_and_decode_bearer_token_on_flask]
