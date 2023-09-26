# Copyright 2021 Google LLC
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

import datetime
import os
import subprocess
import uuid

import pytest
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
region = "us-central1"


@pytest.fixture
def deployed_service():
    # Deploy image to Cloud Run
    service_name = f"filesystem-{SUFFIX}"
    connector = os.environ["CONNECTOR"]
    ip_address = os.environ["IP_ADDRESS"]

    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
            "--config",
            "cloudbuild.yaml",
            "--project",
            PROJECT,
            f"--substitutions=_SERVICE_NAME={service_name},_FILESTORE_IP_ADDRESS={ip_address},_CONNECTOR={connector}",
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
            f"--region={region}",
            "--platform=managed",
            "--quiet",
            "--project",
            PROJECT,
        ]
    )

    subprocess.check_call(
        [
            "gcloud",
            "artifacts",
            "docker",
            "images",
            "delete",
            f"{region}-docker.pkg.dev/{PROJECT}/cloud-run-source-deploy/{service_name}",
            "--quiet",
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
                f"--region={region}",
                "--platform=managed",
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

    retry_strategy = Retry(
        total=3,
        status_forcelist=[400, 401, 403, 404, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
        backoff_factor=3,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    client = requests.session()
    client.mount("https://", adapter)

    # Non mnt directory
    response = client.get(
        service_url, headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200

    # Mnt directory
    mnt_url = f"{service_url}/mnt/nfs/filestore"
    response = client.get(mnt_url, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200

    date = datetime.datetime.utcnow()
    body = response.content.decode("UTF-8")
    assert "{dt:%a}-{dt:%b}-{dt:%d}-{dt:%H}".format(dt=date) in body
