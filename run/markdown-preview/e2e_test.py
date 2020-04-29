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
import random
import subprocess
from urllib import request


@pytest.fixture()
def services():
    #Unique suffix to create distinct service names
    suffix = random.randint(100000,999999)

    # Build and Deploy Cloud Run Services
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "--substitutions",
            f"_SUFFIX={suffix}",
            "--config",
            "e2e_test_setup.yaml",
            "--quiet",
        ]
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
            f"editor-{suffix}",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
    ).stdout.strip()

    token = subprocess.run(
        ["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE
    ).stdout.strip()

    yield editor, token

    subprocess.run(
        ["gcloud", "run", "services", "delete", f"editor-{suffix}",
         "--platform", "managed", "--region", "us-central1", "--quiet"]
    )
    subprocess.run(
        ["gcloud", "run", "services", "delete", f"renderer-{suffix}",
         "--platform", "managed", "--region", "us-central1", "--quiet"]
    )


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
