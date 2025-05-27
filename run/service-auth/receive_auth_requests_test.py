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
# to validate receiving authenticated requests.

from http import HTTPStatus
import os
import subprocess
import uuid

import backoff

from google.auth.transport import requests as transport_requests
from google.oauth2 import id_token

import pytest

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.sessions import Session

from app import get_service_url

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"

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
def full_service_name() -> str:
    # Add a unique suffix to create distinct service names.
    service_name = f"receive-python-{uuid.uuid4().hex}"

    full_service_name = f"projects/{PROJECT_ID}/locations/{REGION}/services/{service_name}"

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
            f"--region={REGION}",
            "--allow-unauthenticated",
            f"--set-env-vars=FULL_SERVICE_NAME={full_service_name}",
            "--quiet",
        ],
        # Rise a CalledProcessError exception for a non-zero exit code.
        check=True,
    )

    yield full_service_name

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
            f"--region={REGION}",
            "--quiet",
        ],
        check=True,
    )


@pytest.fixture(scope="module")
def service_url(full_service_name: str) -> str:
    return get_service_url(full_service_name)


@pytest.fixture(scope="module")
def token(service_url: str) -> str:
    auth_req = transport_requests.Request()
    target_audience = service_url

    # More info for the `fetch_id_token` function:
    # https://googleapis.dev/python/google-auth/latest/reference/google.oauth2.id_token.html#google.oauth2.id_token.fetch_id_token
    token = id_token.fetch_id_token(auth_req, target_audience)

    return token


@pytest.fixture(scope="module")
def client() -> Session:
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


@backoff.on_exception(backoff.expo, Exception, max_time=60)
def test_authenticated_request(
    client: Session, service_url: str, token: str,
) -> None:
    response = client.get(
        service_url, headers={"Authorization": f"Bearer {token}"}
    )
    response_content = response.content.decode("utf-8")

    assert response.status_code == HTTPStatus.OK
    assert "Hello" in response_content


def test_anonymous_request(client: Session, service_url: str) -> None:
    response = client.get(service_url)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_invalid_token(client: Session, service_url: str) -> None:
    response = client.get(
        service_url, headers={"Authorization": "Bearer i-am-not-a-real-token"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
