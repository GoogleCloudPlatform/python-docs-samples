# Copyright 2022 Google LLC.
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
import uuid

import backoff
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client

import pytest

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
SERVICE = "job-quickstart-" + SUFFIX
REGION = "us-west1"


@pytest.fixture
def setup_job():
    # Build container image and run the job
    @backoff.on_exception(backoff.expo, subprocess.CalledProcessError)
    def setup():
        subprocess.check_call(
            [
                "gcloud",
                "builds",
                "submit",
                "--config",
                "e2e_test_setup.yaml",
                "--project",
                PROJECT,
                "--substitutions",
                "_SERVICE=" + SERVICE + ",_VERSION=" + SUFFIX + ",_REGION=" + REGION,
            ]
        )

    # Clean up the test resource
    @backoff.on_exception(backoff.expo, subprocess.CalledProcessError)
    def teardown():
        subprocess.check_call(
            [
                "gcloud",
                "builds",
                "submit",
                "--config",
                "e2e_test_cleanup.yaml",
                "--project",
                PROJECT,
                "--substitutions",
                "_SERVICE=" + SERVICE + ",_VERSION=" + SUFFIX + ",_REGION=" + REGION,
            ]
        )

    # Run the fixture
    setup()
    yield SERVICE
    teardown()


def test_end_to_end(setup_job):
    client = LoggingServiceV2Client()
    resource_names = [f"projects/{PROJECT}"]
    # We add timestamp for making the query faster.
    now = datetime.datetime.now(datetime.timezone.utc)
    filter_date = now - datetime.timedelta(minutes=3)
    filters = (
        f"timestamp>=\"{filter_date.isoformat('T')}\" "
        "resource.type=cloud_run_job "
        f"AND resource.labels.job_name={SERVICE} "
        f"resource.labels.location = \"{REGION}\" "
        "-protoPayload.serviceName=\"run.googleapis.com\""
    )

    # Retry a maximum number of 5 times to find results in Cloud Logging
    found = False
    for x in range(5):
        iterator = client.list_log_entries(
            {"resource_names": resource_names, "filter": filters}
        )
        for entry in iterator:
            if "Task" in entry.text_payload:
                found = True
                # If there are any results, exit loop
                break
        if found:
            break
        # Linear backoff
        time.sleep(x * 10)

    assert found
