# Copyright 2023 Google LLC
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

"""Entrypoint for the Live Stream key publisher."""

import json
import os

from typing import Union
import clients.fake_client
from flask import current_app
import functions_framework
import google.api_core.exceptions
from google.cloud import secretmanager

PROVIDERS = {
    "FakeProvider": clients.fake_client.FakeClient,
}


def http_response(msg: str, status: Union[int, str]) -> str:
    """Prepares HTTP response to the client calling the function.

    Args:
        msg (string): String response message.
        status (string or int): A string or integer HTTP Status code.

    Returns:
        A string containing the JSON response, status, and headers, to be used
        by the Flask server.
    """
    return (
        json.dumps({"message": msg, "status": status}),
        status,
        {"Content-Type": "application/json"},
    )


def write_secret(secret_id: str, payload: str) -> str:
    """Writes a secret to Secret Manager.

    If the secret does not exist, it will be created and an initial version
    added. If the secret does exist, a new version will be created.

    Args:
        secret_id (string): ID of the secret.
        payload (string): Secret payload.

    Returns:
        A string containing the name of the new secret version.
    """
    client = secretmanager.SecretManagerServiceClient()
    project_name = "projects/{}".format(os.environ.get("PROJECT"))
    try:
        secret = client.create_secret(
            request={
                "parent": project_name,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        secret_name = secret.name
    except google.api_core.exceptions.AlreadyExists:
        secret_name = "{}/secrets/{}".format(project_name, secret_id)
    version = client.add_secret_version(
        request={"parent": secret_name, "payload": {"data": str.encode(payload)}}
    )
    return version.name


def validate_environment(cpix_client):
    required_vars = ["PROJECT"]
    required_vars.extend(cpix_client.required_env_vars())
    for required_var in required_vars:
        if required_var not in os.environ:
            return http_response(
                'environment variable "{}" must be set'.format(required_var), 400
            )


@functions_framework.http
def keys(request):
    """Fetches encryption keys and uploads key information to Secret Manager.

    Entrypoint of the Cloud Function.

    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>

    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    if request.method != "POST":
        return http_response("Only POST requests are supported", 400)

    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return http_response("no request body was provided", 400)

        media_id = request_json.get("mediaId")
        if not media_id:
            return http_response('"mediaId" field must be specified', 400)
        provider_key = request_json.get("provider")
        if not provider_key:
            return http_response(
                '"provider" field must be specified. supported providers: {}'.format(
                    ", ".join(PROVIDERS.keys())
                ),
                400,
            )
        if provider_key not in PROVIDERS:
            return http_response(
                '"{}" is not a valid provider. supported providers: {}'.format(
                    provider_key, ", ".join(PROVIDERS.keys())
                ),
                400,
            )
        key_ids = request_json.get("keyIds")
        if not key_ids:
            return http_response(
                'at least one key ID must be specified via the "keyIds" field', 400
            )

        cpix_client = PROVIDERS[provider_key]()
        env_error = validate_environment(cpix_client)
        if env_error:
            return env_error

        key_info = cpix_client.fetch_keys(media_id, key_ids)
        version_name = write_secret(media_id, json.dumps(key_info, indent=2))
        current_app.logger.info("wrote encryption key secret to %s", version_name)
        return version_name

    # pylint: disable=broad-except
    except Exception as ex:
        current_app.logger.exception(ex)
        return http_response(str(ex), 500)
