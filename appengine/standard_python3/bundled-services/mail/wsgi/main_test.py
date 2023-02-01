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
    version_hostname = f"{version_id}-dot-{project_id}.appspot.com"

    # Wait for app to initialize
    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=3)
    def wait_for_app(url):
        r = requests.get(url)
        r.raise_for_status()

    wait_for_app(f"https://{version_hostname}/")

    yield project_id, version_id

    gcloud_cli(f"app versions delete {version_id}")


def test_send_receive(version):
    project_id, version_id = version
    version_hostname = f"{version_id}-dot-{project_id}.appspot.com"

    # Check that version is serving form in home page
    response = requests.get(f"https://{version_hostname}/")
    assert '<form action="" method="POST">' in response.text
    assert response.status_code == 200

    # Send valid mail
    response = requests.post(
        f"https://{version_hostname}/",
        data={
            "email": f"valid-user@{version_id}-dot-{project_id}.appspotmail.com",
            "body": "This message should be delivered",
        },
    )

    assert "Successfully sent mail" in response.text
    assert response.status_code == 201

    # External mail delivery and receipt can take varying lengths of time
    for check in range(3):
        # Give the mail some time to be delivered and logs to post
        time.sleep(60)

        # Fetch logs to check messages on received mail
        entries = gcloud_cli(
            f'logging read "resource.type=gae_app AND resource.labels.version_id={version_id}"'
        )

        text_payloads = ""
        for entry in entries:
            if "textPayload" in entry:
                text_payloads += entry["textPayload"]
                text_payloads += "\n"
                
        if "Received" in text_payloads:
            break

    expected = f"Received greeting for valid-user@{version_id}-dot-{project_id}.appspotmail.com"
    assert expected in text_payloads
    assert "This message should be delivered" in text_payloads
