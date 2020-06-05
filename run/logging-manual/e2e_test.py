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

import json
import os
import subprocess
import time
from urllib import request
import uuid

import pytest


@pytest.fixture()
def services():
    # Unique suffix to create distinct service names
    suffix = uuid.uuid4().hex
    project = os.environ["GOOGLE_CLOUD_PROJECT"]

    # Build and Deploy Cloud Run Services
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "--project",
            project,
            "--substitutions",
            f"_SUFFIX={suffix}",
            "--config",
            "e2e_test_setup.yaml",
            "--quiet",
        ],
        check=True,
    )

    # Get the URL for the service and the token
    service = subprocess.run(
        [
            "gcloud",
            "run",
            "--project",
            project,
            "--platform=managed",
            "--region=us-central1",
            "services",
            "describe",
            f"logging-{suffix}",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.strip()

    id_token = subprocess.run(
        ["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE, check=True
    ).stdout.strip()

    access_token = subprocess.run(
        ["gcloud", "auth", "print-access-token"], stdout=subprocess.PIPE, check=True
    ).stdout.strip()

    yield service, id_token, access_token, project, f"logging-{suffix}"

    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            f"logging-{suffix}",
            "--project",
            project,
            "--platform",
            "managed",
            "--region",
            "us-central1",
            "--quiet",
        ],
        check=True,
    )


def test_end_to_end(services):
    service = services[0].decode()
    id_token = services[1].decode()
    access_token = services[2].decode()
    project = services[3]
    service_name = services[4]

    # Test that the service is responding
    req = request.Request(
        service,
        headers={
            "Authorization": f"Bearer {id_token}",
            "X-Cloud-Trace-Context": "foo/bar",
        },
    )
    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    assert body.decode() == "Hello Logger!"

    # Test that the logs are writing properly to stackdriver
    time.sleep(10)  # Slight delay writing to stackdriver
    response = stackdriver_request(service_name, project, access_token)

    entries = json.loads(response).get("entries")
    assert entries


def stackdriver_request(service_name, project, access_token):
    # Stackdriver API request
    logging_url = "https://logging.googleapis.com/v2/entries:list"
    filters = (
        "resource.type=cloud_run_revision "
        "AND severity=NOTICE "
        f"AND resource.labels.service_name={service_name} "
        "AND jsonPayload.component=arbitrary-property"
    )

    data = json.dumps(
        {
            "resourceNames": [f"projects/{project}"],
            "filter": filters,
            "orderBy": "timestamp desc",
        }
    )

    req = request.Request(
        logging_url,
        data=data.encode(),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    response = request.urlopen(req)
    return response.read().decode()
