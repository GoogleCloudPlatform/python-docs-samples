# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START auth_validate_and_decode_bearer_token_on_flask]
# [START cloudrun_service_to_service_receive]
"""Demonstrates how to receive authenticated service-to-service requests
on a Cloud Run Service.
"""

from http import HTTPStatus
import os
from typing import Optional

from flask import Flask, request

from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

app = Flask(__name__)


def parse_auth_header(auth_header: str) -> Optional[str]:
    """Parse the authorization header, validate and decode the Bearer token.

    Args:
        auth_header: Raw HTTP header with a Bearer token.

    Returns:
        A string containing the email from the token.
        None if the token is invalid or the email can't be retrieved.
    """

    # Split the auth type and value from the header.
    try:
        auth_type, creds = auth_header.split(" ", 1)
    except ValueError:
        print("Malformed Authorization header.")
        return None

    # Get the service URL from the environment variable
    # set at the time of deployment.
    service_url = os.environ["SERVICE_URL"]

    # Define the expected audience as the Service Base URL.
    audience = service_url

    # Validate and decode the ID token in the header.
    if auth_type.lower() == "bearer":
        try:
            # Find more information about `verify_oauth2_token` function:
            # https://googleapis.dev/python/google-auth/latest/reference/google.oauth2.id_token.html#google.oauth2.id_token.verify_oauth2_token
            decoded_token = id_token.verify_oauth2_token(
                id_token=creds,
                request=requests.Request(),
                audience=audience,
            )

            # More info about the structure for the decoded ID Token here:
            # https://cloud.google.com/docs/authentication/token-types#id

            # Verify that the token contains the email claim.
            if decoded_token['email_verified']:
                print(f"Email verified: {decoded_token['email']}")

                return decoded_token['email']

            print("Invalid token. Email wasn't verified.")
        except GoogleAuthError as e:
            print(f"Invalid token: {e}")
    else:
        print(f"Unhandled header format ({auth_type}).")

    return None


@app.route("/")
def main() -> str:
    """Example route for receiving authorized requests only."""
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header:
            email = parse_auth_header(auth_header)

            if email:
                return f"Hello, {email}.\n", HTTPStatus.OK

        # Indicate that the request must be authenticated
        # and that Bearer auth is the permitted authentication scheme.
        headers = {"WWW-Authenticate": "Bearer"}

        return (
            "Unauthorized request. Please supply a valid bearer token.",
            HTTPStatus.UNAUTHORIZED,
            headers,
        )
    except Exception as e:
        return f"Error verifying ID token: {e}", HTTPStatus.UNAUTHORIZED


if __name__ == "__main__":
    app.run(host="localhost", port=int(os.environ.get("PORT", 8080)), debug=True)
# [END cloudrun_service_to_service_receive]
# [END auth_validate_and_decode_bearer_token_on_flask]
