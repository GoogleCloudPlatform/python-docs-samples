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

# This test deploys a secure application running on Cloud Run
# to test that the authentication sample works properly.

import auth

import os
import subprocess
from urllib import request
import uuid

import pytest


@pytest.fixture()
def service():
    # Unique suffix to create distinct service names
    suffix = uuid.uuid4().hex
    project = os.environ['GOOGLE_CLOUD_PROJECT']

    # Deploy hello-world Cloud Run Service from 
    # https://github.com/GoogleCloudPlatform/cloud-run-hello
    subprocess.run(
        [
            "gcloud", "run", "deploy", f"helloworld-{suffix}",
            "--image=gcr.io/cloudrun/hello",
            "--platform=managed",
            "--region=us-central1",
            "--no-allow-unauthenticated",
            "--quiet",
        ], check=True
    )

    # Get the URL for the hello-world service
    service_url = subprocess.run(
        [
            "gcloud", "run", "services", "describe", f"helloworld-{suffix}",
            "--project", project,
            "--platform=managed",
            "--region=us-central1",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
        check=True
    ).stdout.strip()

    yield service_url

    subprocess.run(
        [
            "gcloud", "run", "services", "delete", f"helloworld-{suffix}",
             "--project", project, 
             "--platform=managed",
             "--region=us-central1", 
             "--quiet",
         ],
        check=True
    )

def test_auth(service):
    response = auth.make_authorized_get_request(service.decode())
    assert "Hello World" in response.decode()
