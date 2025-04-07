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

# This test deploys a secure application running on Cloud Run
# to test that the authentication sample works properly.

import os
import subprocess
from urllib import error, request
import uuid

import pytest
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

HTTP_STATUS_OK = 200
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500
HTTP_STATUS_BAD_GATEWAY = 502
HTTP_STATUS_SERVICE_UNAVAILABLE = 503
HTTP_STATUS_GATEWAY_TIMEOUT = 504

STATUS_FORCELIST = [
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_UNAUTHORIZED,
    HTTP_STATUS_FORBIDDEN,
    HTTP_STATUS_NOT_FOUND,
    HTTP_STATUS_INTERNAL_SERVER_ERROR,
    HTTP_STATUS_BAD_GATEWAY,
    HTTP_STATUS_SERVICE_UNAVAILABLE,
    HTTP_STATUS_GATEWAY_TIMEOUT,
],


@pytest.fixture(scope="module")
def service() -> tuple[str, str]:
    """Deploys a Cloud Run service and returns its URL and a valid token."""
    # Add a unique suffix to create distinct service names.
    service_name = f"receive-{uuid.uuid4()}"

    # Deploy the Cloud Run Service.
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--project",
            PROJECT_ID,
            "--source",
            ".",
            "--region=us-central1",
            "--allow-unauthenticated",
            "--quiet",
        ],
        # Rise a CalledProcessError exception for a non-zero exit code.
        check=True,
    )

    endpoint_url = (
        subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                service_name,
                "--project",
                PROJECT_ID,
                "--region=us-central1",
                "--format=value(status.url)",
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    token = (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    yield endpoint_url, token

    # Clean-up after running the test.
    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--project",
            PROJECT_ID,
            "--async",
            "--region=us-central1",
            "--quiet",
        ],
        check=True,
    )


def test_authentication_on_cloud_run(service: tuple[str, str]) -> None:
    endpoint_url = service[0]
    token = service[1]

    req = request.Request(endpoint_url)
    try:
        _ = request.urlopen(req)
    except error.HTTPError as e:
        assert e.code == HTTP_STATUS_FORBIDDEN

    retry_strategy = Retry(
        total=3,
        status_forcelist=STATUS_FORCELIST,
        allowed_methods=["GET", "POST"],
        backoff_factor=3,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    client = requests.session()
    client.mount("https://", adapter)

    response = client.get(endpoint_url, headers={"Authorization": f"Bearer {token}"})
    response_content = response.content.decode("UTF-8")

    assert response.status_code == HTTP_STATUS_OK
    assert "Hello" in response_content
    assert "anonymous" not in response_content


def test_anonymous_request_on_cloud_run(service: tuple[str, str]) -> None:
    endpoint_url = service[0]

    req = request.Request(endpoint_url)
    try:
        _ = request.urlopen(req)
    except error.HTTPError as e:
        assert e.code == HTTP_STATUS_FORBIDDEN

    retry_strategy = Retry(
        total=3,
        status_forcelist=STATUS_FORCELIST,
        allowed_methods=["GET", "POST"],
        backoff_factor=3,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    client = requests.session()
    client.mount("https://", adapter)

    response = client.get(endpoint_url)
    response_content = response.content.decode("UTF-8")

    assert response.status_code == HTTP_STATUS_OK
    assert "Hello" in response_content
    assert "anonymous" in response_content


def test_invalid_token(service: tuple[str, str]) -> None:
    endpoint_url = service[0]

    req = request.Request(endpoint_url)
    try:
        _ = request.urlopen(req)
    except error.HTTPError as e:
        assert e.code == HTTP_STATUS_FORBIDDEN

    retry_strategy = Retry(
        total=3,
        status_forcelist=STATUS_FORCELIST,
        allowed_methods=["GET", "POST"],
        backoff_factor=3,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    client = requests.session()
    client.mount("https://", adapter)

    # Sample token from https://jwt.io for John Doe.
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    response = client.get(endpoint_url, headers={"Authorization": f"Bearer {token}"})
    response_content = response.content.decode("UTF-8")

    assert "Invalid token" in response_content