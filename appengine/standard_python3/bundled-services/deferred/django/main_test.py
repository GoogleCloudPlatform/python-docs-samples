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

import backoff
import pytest
import requests


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def gcloud_cli(command):
    """
    Runs the gcloud CLI with given options, parses the json formatted output
    and returns the resulting Python object.

    Usage: gcloud_cli(options)
        options: command line options

    Example:
        result = gcloud_cli("app deploy --no-promote")
        print(f"Deployed version {result['versions'][0]['id']}")

    Raises Exception with the stderr output of the last attempt on failure.
    """
    full_command = f"gcloud {command} --quiet --format=json"
    print("Running command:", full_command)

    output = subprocess.run(
        full_command,
        capture_output=True,
        shell=True,
        check=True,
    )
    try:
        entries = json.loads(output.stdout)
        return entries
    except Exception:
        print("Failed to read log")
        print(f"gcloud stderr was {output.stderr}")

    raise Exception(output.stderr)


@pytest.fixture
def version():
    """Launch a new version of the app for testing, and yield the
    project and version number so tests can invoke it, then delete it.
    """

    result = gcloud_cli(f"app deploy --no-promote --version={uuid.uuid4().hex}")
    version_id = result["versions"][0]["id"]
    project_id = result["versions"][0]["project"]

    yield project_id, version_id

    gcloud_cli(f"app versions delete {version_id}")


def test_upload_and_view(version):
    project_id, version_id = version
    version_hostname = f"{version_id}-dot-{project_id}.appspot.com"

    # Initial value of counter should be 0
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.text == "0"
    assert response.status_code == 200

    # Request counter be incremented
    response = requests.get(f"https://{version_hostname}/counter/increment")
    assert response.status_code == 200

    # counter should be 10 almost immediately
    time.sleep(10)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.text == "10"
    assert response.status_code == 200

    # After 20 seconds, counter should be 20
    time.sleep(20)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.text == "20"
    assert response.status_code == 200

    # After 40 seconds, counter should be 30
    time.sleep(20)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.text == "30"
    assert response.status_code == 200

    # counter should stay at 30 unless another request to increment it is set
    time.sleep(10)
    response = requests.get(f"https://{version_hostname}/counter/get")
    assert response.text == "30"
    assert response.status_code == 200
