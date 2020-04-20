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

import json
import pytest
import subprocess
from urllib import request
import os

# Setting up variables for testing
GCLOUD_PROJECT = os.environ["GCLOUD_PROJECT"]

@pytest.fixture()
def services():
    # Change into parent directory to access renderer and editor directories
    os.chdir("..")

    # Build and Deploy Cloud Run Services
    subprocess.run(
        ["gcloud", "builds", "submit", "--config", 
         "e2e_test/test_setup.yaml", "--quiet"]
    )

    # Get the URL for the editor and the token
    editor = subprocess.run(
        [
            "gcloud",
            "run",
            "--platform=managed",
            "--region=us-central1",
            "services",
            "describe",
            "editor",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
    ).stdout.strip()

    token = subprocess.run(
        ["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE
    ).stdout.strip()

    yield editor, token


def test_end_to_end(services):
    editor = services[0].decode() + "/render"
    token = services[1].decode()
    data = json.dumps({"data": "**strong text**"})

    req = request.Request(
        editor,
        data=data.encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    assert "<p><strong>strong text</strong></p>" in body.decode()
#     tear_down()


# def tear_down():
#     subprocess.run(["gcloud", "run", "services", "delete", "editor", "--quiet"])
#     subprocess.run(
#         ["gcloud", "run", "services", "delete", "renderer", "--quiet"]
#     )
