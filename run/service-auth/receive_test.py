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


@pytest.fixture()
def services():
    # Unique suffix to create distinct service names
    suffix = uuid.uuid4().hex
    service_name = f"receive-{suffix}"
    project = os.environ["GOOGLE_CLOUD_PROJECT"]

    # Deploy receive Cloud Run Service
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--project",
            project,
            "--source",
            ".",
            "--region=us-central1",
            "--no-allow-unauthenticated",
            "--quiet",
        ],
        check=True,
    )

    # Get the URL for the service
    endpoint_url = subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "describe",
            service_name,
            "--project",
            project,
            "--platform=managed",
            "--region=us-central1",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.strip()

    token = subprocess.run(
        ["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE, check=True
    ).stdout.strip()

    yield endpoint_url, token

    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--project",
            project,
            "--async",
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
        ],
        check=True,
    )


def test_auth(services):
    url = services[0].decode()
    token = services[1].decode()

    req = request.Request(url, headers={"Authorization": f"Bearer {token}"})

    response = request.urlopen(req)
    assert response.status == 200
    assert "Hello" in response.read().decode()
    assert "anonymous" not in response.read().decode()


def test_noauth(services):
    url = services[0].decode()

    req = request.Request(url)

    try:
        _ = request.urlopen(req)
    except error.HTTPError as e:
        assert e.code == 403
