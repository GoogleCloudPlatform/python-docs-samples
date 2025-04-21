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

from http import HTTPStatus
import os
from typing import Union

from flask import Flask, request

from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

app = Flask(__name__)

from urllib.request import Request, urlopen

SERVICE_NAME = os.getenv("K_SERVICE")
# E.g. 'receive-python'

# https://cloud.google.com/run/docs/container-contract#metadata-server
# https://cloud.google.com/compute/docs/access/authenticate-workloads#applications

req = Request("http://metadata.google.internal/computeMetadata/v1/project/project-id")
req.add_header("Metadata-Flavor", "Google")
PROJECT_ID = urlopen(req).read().decode("utf-8")
# E.g. 'samples-xwf-01'

req = Request("http://metadata.google.internal/computeMetadata/v1/instance/region")
req.add_header("Metadata-Flavor", "Google")
# Returns "projects/PROJECT-NUMBER/regions/REGION"
# E.g. "projects/764067474825/regions/us-central1"

response: str = urlopen(req).read().decode("utf-8")
project_region_list = response.split('/')

PROJECT_NUMBER = project_region_list[1]
REGION = project_region_list[3]

req = Request("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token")
req.add_header("Metadata-Flavor", "Google")
# Returns "projects/PROJECT-NUMBER/regions/REGION"
# E.g. "projects/764067474825/regions/us-central1"

TOKEN_JSON_RESPONSE: str = urlopen(req).read().decode("utf-8")

# https://cloud.google.com/run/docs/triggering/https-request#deterministic
SERVICE_URL = f"https://{SERVICE_NAME}-{PROJECT_NUMBER}.{REGION}.run.app"


def receive_request_and_parse_auth_header(auth_header: str) -> Union[str, bool]:
    """Parse the authorization header, validate the Bearer token
    and decode the token to get its information.

    Args:
        auth_header: Raw HTTP header with a Bearer token.

    Returns:
        A string with the email from the token.
        False if the token is invalid.
    """

    # TODO: Update this function based on:
    # https://github.com/googleapis/google-auth-library-python/blob/main/samples/cloud-client/snippets/verify_google_idtoken.py

    # Split the auth type and value from the header.
    auth_type, creds = auth_header.split(" ", 1)

    # TODO: https://cloud.google.com/run/docs/authenticating/service-to-service#acquire-token
    # Set the audience claim (aud) to the URL of the receiving service
    # Note: Use the base domain, avoid a trailing slash.
    audience = SERVICE_URL

    if auth_type.lower() == "bearer":
        # Find more information about `verify_oauth2_token` function here:
        # https://googleapis.dev/python/google-auth/latest/reference/google.oauth2.id_token.html#google.oauth2.id_token.verify_oauth2_token
        # TODO: Check clock_skew_in_seconds (int)
        # The clock skew used for `iat` and `exp`` validation,
        # as other samples show it's usage.

        # If `audience` is None then the audience is not verified.
        try:
            decoded_token = id_token.verify_oauth2_token(
                id_token=creds,
                request=requests.Request(),
                audience=audience,
            )

            # TODO: Perhaps show other fields from the token.
            # TODO: Indicate that the Oauth2 Token is a JWT.
            # https://cloud.google.com/docs/authentication/token-types#id

            # Verify that the token contains subject and email claims.

            # Get the User id.
            if not decoded_token["sub"] is None:
                print(f"User id: {decoded_token['sub']}")

            # Optionally, if "INCLUDE_EMAIL" was set in the token options,
            # check if the email was verified.
            if decoded_token['email_verified'] == "True":
                print(f"Email verified {decoded_token['email']}")

            return decoded_token['email']
        except GoogleAuthError as e:
            print(f"Invalid token: {e}")
            return False
    else:
        print(f"Unhandled header format ({auth_type}).")

    return False


@app.route("/")
def main() -> str:
    """Example route for receiving authorized requests."""
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header:
            email = receive_request_and_parse_auth_header(auth_header)

            if email:
                return f"Hello, {email}.\n", HTTPStatus.OK

        # Indicate that the request must be authenticated
        # and that Bearer auth is the permitted authentication scheme.
        headers = {"WWW-Authenticate": "Bearer"}

        return (
            "Unauthorized request. Please supply a bearer token.",
            HTTPStatus.UNAUTHORIZED,
            headers,
        )
    except Exception as e:
        return f"Error verifying ID token: {e}", HTTPStatus.UNAUTHORIZED


@app.route("/info")
def info() -> str:
    """Show instance information for debugging."""

    target_audience = SERVICE_URL
    auth_req = requests.Request()

    token_client_library = id_token.fetch_id_token(auth_req, target_audience)

    response = f"{SERVICE_NAME=}<br>\n{PROJECT_ID=}<br>\n" \
        + f"{PROJECT_NUMBER=}<br>\n{REGION=}<br>\n" \
        + f"{SERVICE_URL=}<br>\n{TOKEN_JSON_RESPONSE=}<br>\n" \
        + f"{token_client_library}<br>\n"

    return response, HTTPStatus.OK


if __name__ == "__main__":
    app.run(host="localhost", port=int(os.environ.get("PORT", 8080)), debug=True)
