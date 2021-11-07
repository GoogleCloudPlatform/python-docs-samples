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

# build container image + push w/ cloud build
# deploy to cloud run
# get auth

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
IMAGE_NAME = f"gcr.io/{PROJECT}/sys-package-{SUFFIX}"


@pytest.fixture
def container_image():
    # Build container image for Cloud Run deployment
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "--tag",
            IMAGE_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )
    yield IMAGE_NAME

    # Delete container image
    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def deployed_service(container_image):
    # Deploy image to Cloud Run
    service_name = f"sys-package-{SUFFIX}"
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--image",
            container_image,
            "--project",
            PROJECT,
            "--region=us-central1",
            "--platform=managed",
            "--no-allow-unauthenticated",
        ],
        check=True,
    )

    yield service_name

    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
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


def test_end_to_end(service_url_auth_token):
    service_url, auth_token = service_url_auth_token

    data = "diagram.png?dot=digraph G { A -> {B, C, D} -> {F} }".replace(" ", "%20")
    print(f"{service_url}{data}")

    req = request.Request(
        f"{service_url}/{data}",
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
    )

    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    # Response is a png
    assert b"PNG" in body
