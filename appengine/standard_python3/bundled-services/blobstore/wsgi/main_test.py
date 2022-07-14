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
import re
import subprocess

import pytest
import requests


@pytest.fixture
def version():
    """Launch a new version of the app for testing, and yield the
    project and version number so tests can invoke it, then delete it.
    """

    output = subprocess.run(
        "gcloud app deploy --no-promote --quiet --format=json",
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

    # Check that version is serving form in home page
    response = requests.get(f"https://{version_hostname}/")
    assert response.status_code == 200
    assert '<form action="' in response.text

    matches = re.search(r'action="(.*?)"', response.text)
    assert matches is not None
    upload_url = matches.group(1)

    with open("./main.py", "rb") as f:
        response = requests.post(upload_url, files={"file": f})

    assert response.status_code == 200
    assert b"from google.appengine.api" in response.content
