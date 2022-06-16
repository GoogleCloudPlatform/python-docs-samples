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

import pytest
import requests


@pytest.fixture
def version():
    """Launch a new version of the app for testing, and yield the
    version number so tests can invoke it.
    """
    output = subprocess.run(
        "gcloud app deploy --no-promote --quiet --format=json",
        capture_output=True,
        shell=True,
    )

    # For debugging:
    print(f"App deploy return code is '{output.returncode}'\n\n")
    print(f"App deploy stderr is '{output.stderr}'\n\n")
    print(f"App deploy stdout is '{output.stdout}'\n\n")

    result = json.loads(output.stdout)
    yield result["versions"][0]["version"]["name"]

    # TODO: kill new version

    return


def test_send_receive_and_bounce(version):
    _, project_id, _, service_id, _, version_id = version.split("/")
    version_hostname = f"{version_id}-dot-{project_id}.appspot.com"

    # Check that version is serving form in home page
    response = requests.get(f"https://{version_hostname}/")
    assert response.status_code == 200
    assert '<form action="" method="POST">' in response.text

    # Send valid mail
    response = requests.post(
        f"https://{version_hostname}/",
        data={
            "email": f"valid-user@{version_id}-dot-{project_id}.appspotmail.com",
            "body": "This message should be delivered",
        },
    )

    assert response.status_code == 201
    assert "Successfully sent mail" in response.text

    # Send invalid mail that will bounce
    response = requests.post(
        f"https://{version_hostname}/",
        data={
            "email": "nobody@example.com",
            "body": "This message should bounce",
        },
    )

    assert response.status_code == 201
    assert "Successfully sent mail" in response.text

    # Give the mail some time to be delivered or bounced
    time.sleep(60)

    # Fetch logs to check messages on received mail
    output = subprocess.run(
        [
            "gcloud",
            "logging",
            "read",
            f"resource.type=gae_app AND resource.labels.version_id={version_id}",
            "--format=json",
        ],
        capture_output=True,
        shell=True,
    )
    entries = json.loads(output.stdout)

    textPayloads = ""
    for entry in entries:
        if "textPayload" in entry:
            textPayloads += entry["textPayload"]
            textPayloads += "\n"

    expected = f"Received greeting for valid-user@{version_id}-dot-{project_id}.appspotmail.com"
    assert expected in textPayloads
    assert "This message should be delivered" in textPayloads

    assert "Bounce original:  {'to': ['nobody@example.com']," in textPayloads
    assert "Bounce notification:" in textPayloads
