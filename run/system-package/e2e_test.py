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


@pytest.fixture()
def services():
    # Unique suffix to create distinct service names
    suffix = uuid.uuid4().hex
    project = os.environ['GOOGLE_CLOUD_PROJECT']

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
        ], check=True
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
            f"sys-package-{suffix}",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
        check=True
    ).stdout.strip()

    token = subprocess.run(
        ["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE,
        check=True
    ).stdout.strip()

    yield service, token

    subprocess.run(
        ["gcloud", "run", "services", "delete", f"sys-package-{suffix}",
         "--project", project, "--platform", "managed", "--region",
         "us-central1", "--quiet"],
        check=True
    )


def test_end_to_end(services):
    service = services[0].decode()
    token = services[1].decode()
    data = (
        "diagram.png?dot=digraph G { A -> {B, C, D} -> {F} }".replace(" ", "%20"))
    print(service)
    print(f"{service}{data}")

    req = request.Request(
        f"{service}/{data}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    # Response is a png
    assert b"PNG" in body
