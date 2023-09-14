# Copyright 2020 Google, LLC.
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

# This sample creates a secure two-service application running on Cloud Run.
# This test builds and deploys the two secure services
# to test that they interact properly together.

import os
import subprocess
from urllib import request
import uuid

import pytest

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
IMAGE_NAME = f"gcr.io/{PROJECT}/helloworld-{SUFFIX}"


@pytest.fixture
def deployed_service():
    # Deploy image to Cloud Run
    service_name = f"helloworld-{SUFFIX}"
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--source",
            ".",
            "--project",
            PROJECT,
            "--region=us-central1",
            "--platform=managed",
            "--no-allow-unauthenticated",
            "--set-env-vars=NAME=Test",
        ]
    )

    yield service_name

    subprocess.check_call(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--async",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture
def service_url_auth_token(deployed_service):
    # Get Cloud Run service URL and auth token
    service_url = (
        subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                deployed_service,
                "--platform=managed",
                "--region=us-central1",
                "--format=value(status.url)",
                "--project",
                PROJECT,
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    auth_token = (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    yield service_url, auth_token

    # no deletion needed


def test_end_to_end(service_url_auth_token):
    service_url, auth_token = service_url_auth_token

    req = request.Request(
        f"{service_url}/", headers={"Authorization": f"Bearer {auth_token}"}
    )
    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    assert "Hello Test!" == body.decode()
