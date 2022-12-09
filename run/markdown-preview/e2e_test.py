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

import backoff
import pytest


SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
EDITOR_IMAGE_NAME = f"gcr.io/{PROJECT}/editor-{SUFFIX}"
RENDERER_IMAGE_NAME = f"gcr.io/{PROJECT}/renderer-{SUFFIX}"


@backoff.on_exception(backoff.expo, subprocess.CalledProcessError, max_tries=10)
def run_shell_command(args):
    """
    Runs a command with given args.
    Usage: gcloud_cli(options)
        options: command line options
    Example:
        result = gcloud_cli("app deploy --no-promote")
        print(f"Deployed version {result['versions'][0]['id']}")
    Raises Exception with the stderr output of the last attempt on failure.
    """
    full_command = " ".join(args)
    print("Running command:", full_command)

    try:
        output = subprocess.run(
            full_command,
            capture_output=True,
            shell=True,
            check=True,
        )
        return output.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr}")
        raise e


@pytest.fixture()
def renderer_image():
    # Build container image for Cloud Run deployment
    run_shell_command(
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
        ]
    )
    yield RENDERER_IMAGE_NAME

    # Delete container image
    run_shell_command(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            RENDERER_IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture()
def editor_image():
    # Build container image for Cloud Run deployment
    run_shell_command(
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
        ]
    )
    yield EDITOR_IMAGE_NAME

    # Delete container image
    run_shell_command(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            EDITOR_IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture
def renderer_deployed_service(renderer_image):
    # Deploy image to Cloud Run
    renderer_service_name = f"renderer-{SUFFIX}"
    run_shell_command(
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
        ]
    )

    yield renderer_service_name

    run_shell_command(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            renderer_service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--async",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture
def renderer_service_url_auth_token(renderer_deployed_service):
    # Get Cloud Run service URL and auth token
    renderer_service_url = (
        run_shell_command(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                renderer_deployed_service,
                "--platform=managed",
                "--region=us-central1",
                "--format=\"value(status.url)\"",
                "--project",
                PROJECT,
            ]
        )
        .strip()
        .decode()
    )
    renderer_auth_token = (
        run_shell_command(
            ["gcloud", "auth", "print-identity-token"]
        )
        .strip()
        .decode()
    )

    yield renderer_service_url, renderer_auth_token


@pytest.fixture
def editor_deployed_service(editor_image, renderer_service_url_auth_token):
    # Deploy editor image with renderer URL environment var
    editor_service_name = f"editor-{SUFFIX}"
    renderer_service_url, renderer_auth_token = renderer_service_url_auth_token
    run_shell_command(
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
        ]
    )

    yield editor_service_name

    run_shell_command(
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
        ]
    )


@pytest.fixture
def editor_service_url_auth_token(editor_deployed_service):
    # Get Cloud Run service URL and auth token
    editor_service_url = (
        run_shell_command(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                editor_deployed_service,
                "--platform=managed",
                "--region=us-central1",
                "--format=\"value(status.url)\"",
                "--project",
                PROJECT,
            ]
        )
        .strip()
        .decode()
    )
    editor_auth_token = (
        run_shell_command(
            ["gcloud", "auth", "print-identity-token"]
        )
        .strip()
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
