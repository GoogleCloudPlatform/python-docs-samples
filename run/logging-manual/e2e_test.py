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

import datetime
import os
import subprocess
import time
from urllib import request
import uuid

from google.cloud import logging_v2

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

    yield service, id_token, project, f"logging-{suffix}"

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
    project = services[2]
    service_name = services[3]

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
    client = logging_v2.LoggingServiceV2Client()
    resource_names = [f"projects/{project}"]
    # We add timestamp for making the query faster.
    now = datetime.datetime.now(datetime.timezone.utc)
    filter_date = now - datetime.timedelta(minutes=1)
    filters = (
        f"timestamp>=\"{filter_date.isoformat('T')}\" "
        "resource.type=cloud_run_revision "
        "AND severity=NOTICE "
        f"AND resource.labels.service_name={service_name} "
        "AND jsonPayload.component=arbitrary-property"
    )

    # Retry a maximum number of 10 times to find results in stackdriver
    for x in range(10):
        iterator = client.list_log_entries(resource_names, filter_=filters)
        for entry in iterator:
            # If there are any results, exit loop
            break

    assert iterator.num_results
