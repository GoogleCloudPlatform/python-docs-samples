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

from http import HTTPStatus
import os
import subprocess
from urllib import error, request
import uuid

from google.auth.transport import requests
from google.oauth2 import id_token

import pytest

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.sessions import Session

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

STATUS_FORCELIST = [
    HTTPStatus.BAD_REQUEST,
    HTTPStatus.UNAUTHORIZED,
    HTTPStatus.FORBIDDEN,
    HTTPStatus.NOT_FOUND,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
],


@pytest.fixture(scope="module")
def service_name() -> str:
    # Add a unique suffix to create distinct service names.
    # service_name_str = f"receive-python-{uuid.uuid4().hex}"
    service_name_str = "receive-python"

    # TODO: To reduce testing time, the Run Services are being deployed
    # and deleted manually. Uncomment the following lines before
    # sending a final PR.

    # Deploy the Cloud Run Service.
    # subprocess.run(
    #     [
    #         "gcloud",
    #         "run",
    #         "deploy",
    #         service_name_str,
    #         "--project",
    #         PROJECT_ID,
    #         "--source",
    #         ".",
    #         "--region=us-central1",
    #         "--allow-unauthenticated",
    #         "--quiet",
    #     ],
    #     # Rise a CalledProcessError exception for a non-zero exit code.
    #     check=True,
    # )

    yield service_name_str

    # Clean-up after running the test.
    # subprocess.run(
    #     [
    #         "gcloud",
    #         "run",
    #         "services",
    #         "delete",
    #         service_name_str,
    #         "--project",
    #         PROJECT_ID,
    #         "--async",
    #         "--region=us-central1",
    #         "--quiet",
    #     ],
    #     check=True,
    # )


@pytest.fixture(scope="module")
def endpoint_url(service_name: str) -> str:
    endpoint_url_str = (
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

    return endpoint_url_str


@pytest.fixture(scope="module")
def debug_token() -> str:
    token_str = (
        # TODO: This approach is not recommended in production environments
        # as in:
        # https://cloud.google.com/docs/authentication/get-id-token#generic-dev
        subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    return token_str


@pytest.fixture(scope="module")
def token(endpoint_url: str) -> str:
    # Cloud Run uses your service's hostname as the `audience` value.
    # For example:
    # audience = 'https://my-cloud-run-service.run.app/'
    target_audience = endpoint_url
    auth_req = requests.Request()

    # More info for the `fetch_id_token`function
    # https://googleapis.dev/python/google-auth/1.14.0/reference/google.oauth2.id_token.html
    token = id_token.fetch_id_token(auth_req, target_audience)

    return token


@pytest.fixture(scope="module")
def client(endpoint_url: str) -> Session:
    # Validate that we get an 401 (UNAUTHORIZED) when opening
    # the URL without an Authorization attempt.
    req = request.Request(endpoint_url)
    try:
        _ = request.urlopen(req)
    except error.HTTPError as e:
        # TODO: Check if we need to fix the following logic: 401 vs 403
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401
        # But the Networking tab in the Run Service uses the following
        # 403 (Forbidden) - When a Token is not supplied
        # 401 (Unauthorized) - When the token is invalid
        assert e.code == HTTPStatus.UNAUTHORIZED

    retry_strategy = Retry(
        total=3,
        status_forcelist=STATUS_FORCELIST,
        allowed_methods=["GET", "POST"],
        backoff_factor=3,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    client = requests.session()
    client.mount("https://", adapter)

    return client


def test_authentication_on_cloud_run(
    client: Session, endpoint_url: str, token: str
) -> None:
    response = client.get(
        endpoint_url, headers={"Authorization": f"Bearer {token}"}
    )
    response_content = response.content.decode("utf-8")

    assert response.status_code == HTTPStatus.OK
    assert "Hello" in response_content
    assert "anonymous" not in response_content


def test_anonymous_request_on_cloud_run(client: Session, endpoint_url: str) -> None:
    response = client.get(endpoint_url)
    response_content = response.content.decode("utf-8")

    assert response.status_code == HTTPStatus.OK
    assert "Hello" in response_content
    assert "anonymous" in response_content


def test_invalid_token(client: Session, endpoint_url: str) -> None:
    response = client.get(
        endpoint_url, headers={"Authorization": "Bearer i-am-not-a-real-token"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
