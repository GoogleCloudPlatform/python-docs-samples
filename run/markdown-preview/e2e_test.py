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

import json
import os
import subprocess
from urllib import request
import uuid

import pytest


SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
EDITOR_IMAGE_NAME = f"gcr.io/{PROJECT}/editor-{SUFFIX}"
RENDERER_IMAGE_NAME = f"gcr.io/{PROJECT}/renderer-{SUFFIX}"


@pytest.fixture()
def renderer_image():
    # Build container image for Cloud Run deployment
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "renderer/.",
            "--tag",
            RENDERER_IMAGE_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )
    yield RENDERER_IMAGE_NAME

    # Delete container image
    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            RENDERER_IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture()
def editor_image():
    # Build container image for Cloud Run deployment
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "editor/.",
            "--tag",
            EDITOR_IMAGE_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )
    yield EDITOR_IMAGE_NAME

    # Delete container image
    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            EDITOR_IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def renderer_deployed_service(renderer_image):
    # Deploy image to Cloud Run
    renderer_service_name = f"renderer-{SUFFIX}"
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            renderer_service_name,
            "--image",
            renderer_image,
            "--project",
            PROJECT,
            "--region=us-central1",
            "--platform=managed",
            "--no-allow-unauthenticated",
        ],
        check=True,
    )

    yield renderer_service_name

    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            renderer_service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def renderer_service_url_auth_token(renderer_deployed_service):
    # Get Cloud Run service URL and auth token
    renderer_service_url = (
        subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                renderer_deployed_service,
                "--platform=managed",
                "--region=us-central1",
                "--format=value(status.url)",
                "--project",
                PROJECT,
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    renderer_auth_token = (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    yield renderer_service_url, renderer_auth_token


@pytest.fixture
def editor_deployed_service(editor_image, renderer_service_url_auth_token):
    # Deploy editor image with renderer URL environment var
    editor_service_name = f"editor-{SUFFIX}"
    renderer_service_url, renderer_auth_token = renderer_service_url_auth_token
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            editor_service_name,
            "--image",
            editor_image,
            "--project",
            PROJECT,
            "--region=us-central1",
            "--platform=managed",
            "--set-env-vars",
            f"EDITOR_UPSTREAM_RENDER_URL={renderer_service_url}",
            "--no-allow-unauthenticated",
        ],
        check=True,
    )

    yield editor_service_name

    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            editor_service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def editor_service_url_auth_token(editor_deployed_service):
    # Get Cloud Run service URL and auth token
    editor_service_url = (
        subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                editor_deployed_service,
                "--platform=managed",
                "--region=us-central1",
                "--format=value(status.url)",
                "--project",
                PROJECT,
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    editor_auth_token = (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    yield editor_service_url, editor_auth_token


def test_end_to_end(editor_service_url_auth_token):
    editor_service_url, editor_auth_token = editor_service_url_auth_token
    editor = editor_service_url + "/render"
    data = json.dumps({"data": "**strong text**"})

    req = request.Request(
        editor,
        data=data.encode(),
        headers={
            "Authorization": f"Bearer {editor_auth_token}",
            "Content-Type": "application/json",
        },
    )

    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    assert "<p><strong>strong text</strong></p>" in body.decode()
