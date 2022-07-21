# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess
import time
import uuid

import pytest
import requests


@pytest.fixture
def version():
    """Launch a new version of the app for testing, and yield the
    project and version number so tests can invoke it, then delete it.
    """

    output = subprocess.run(
        f"gcloud app deploy --no-promote --quiet --format=json --version={uuid.uuid4().hex}",
        capture_output=True,
        shell=True,
    )

    result = json.loads(output.stdout)
    version_id = result["versions"][0]["id"]
    project_id = result["versions"][0]["project"]

    yield project_id, version_id

    output = subprocess.run(
        f"gcloud app versions delete {version_id}",
        capture_output=True,
        shell=True,
    )


def test_upload_and_view(version):
    project_id, version_id = version
    version_hostname = f"{version_id}-dot-{project_id}.appspot.com"

    # Initial value of counter should be 0
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.status_code == 200
    assert response.text == "0"

    # Request counter be incremented
    response = requests.get(f"https://{version_hostname}/counter/increment")
    assert response.status_code == 200

    # counter should be 10 almost immediately
    time.sleep(2)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.status_code == 200
    assert response.text == "10"

    # After 10 seconds, counter should be 20
    time.sleep(10)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.status_code == 200
    assert response.text == "20"

    # After 20 seconds, counter should be 30
    time.sleep(10)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.status_code == 200
    assert response.text == "30"

    # counter should stay at 30 unless another request to increment it is set
    time.sleep(10)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.status_code == 200
    assert response.text == "30"
