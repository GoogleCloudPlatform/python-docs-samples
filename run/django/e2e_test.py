# Copyright 2021 Google LLC.
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

# This test creates a Cloud SQL instance, a Cloud Storage bucket, associated
# secrets, and deploys a Django service

from collections.abc import Iterator
import os
import subprocess
import uuid

import backoff
import pytest
import requests

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]

SAMPLE_VERSION = os.environ.get("SAMPLE_VERSION", None)
GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
PLATFORM = "managed"

SERVICE = f"polls-{SUFFIX}"

# Retreieve Cloud SQL test config
POSTGRES_INSTANCE = os.environ.get("POSTGRES_INSTANCE", None)
if not POSTGRES_INSTANCE:
    raise Exception("'POSTGRES_INSTANCE' env var not found")

# Presuming POSTGRES_INSTANCE comes in the form project:region:instance
# Require the short form in some cases.
# POSTGRES_INSTANCE_FULL: project:region:instance
# POSTGRES_INSTANCE_NAME: instance only
if ":" in POSTGRES_INSTANCE:
    POSTGRES_INSTANCE_FULL = POSTGRES_INSTANCE
    POSTGRES_INSTANCE_NAME = POSTGRES_INSTANCE.split(":")[-1]
else:
    POSTGRES_INSTANCE_FULL = f"{GOOGLE_CLOUD_PROJECT}:{REGION}:{POSTGRES_INSTANCE}"
    POSTGRES_INSTANCE_NAME = POSTGRES_INSTANCE

POSTGRES_DATABASE = f"django-database-{SUFFIX}"

CLOUD_STORAGE_BUCKET = f"{GOOGLE_CLOUD_PROJECT}-media-{SUFFIX}"

POSTGRES_DATABASE = f"polls-{SUFFIX}"
POSTGRES_USER = f"django-{SUFFIX}"
POSTGRES_PASSWORD = uuid.uuid4().hex[:26]

ADMIN_NAME = "admin"
ADMIN_PASSWORD = uuid.uuid4().hex[:26]

SECRET_SETTINGS_NAME = f"django_settings-{SUFFIX}"
SECRET_PASSWORD_NAME = f"superuser_password-{SUFFIX}"


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def run_shell_cmd(args: list) -> subprocess.CompletedProcess:
    """
    Runs a shell command and returns its output.
    Usage: run_shell_cmd(args)
        args: an array of command line arguments
    Example:
        result = run_shell_command(["gcloud, "app", "deploy"])
        print("The command's stdout was:", result.stdout)

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

        return output
    except subprocess.CalledProcessError as e:
        print("Command failed")
        print(f"stderr was {e.stderr}")
        raise e


@pytest.fixture
def deployed_service() -> str:

    substitutions = [
        f"_SERVICE={SERVICE},"
        f"_PLATFORM={PLATFORM},"
        f"_REGION={REGION},"
        f"_STORAGE_BUCKET={CLOUD_STORAGE_BUCKET},"
        f"_DB_NAME={POSTGRES_DATABASE},"
        f"_DB_USER={POSTGRES_USER},"
        f"_DB_PASS={POSTGRES_PASSWORD},"
        f"_DB_INSTANCE={POSTGRES_INSTANCE_NAME},"
        f"_SECRET_SETTINGS_NAME={SECRET_SETTINGS_NAME},"
        f"_SECRET_PASSWORD_NAME={SECRET_PASSWORD_NAME},"
        f"_SECRET_PASSWORD_VALUE={ADMIN_PASSWORD},"
        f"_CLOUD_SQL_CONNECTION_NAME={POSTGRES_INSTANCE_FULL}"
    ]
    if SAMPLE_VERSION:
        substitutions.append(f",_VERSION={SAMPLE_VERSION}")

    run_shell_cmd(
        [
            "gcloud",
            "builds",
            "submit",
            "--project",
            GOOGLE_CLOUD_PROJECT,
            "--config",
            "./e2e_test_setup.yaml",
            "--substitutions",
        ]
        + substitutions
    )

    yield SERVICE

    # Cleanup

    substitutions = [
        f"_SERVICE={SERVICE},"
        f"_PLATFORM={PLATFORM},"
        f"_REGION={REGION},"
        f"_DB_USER={POSTGRES_USER},"
        f"_DB_NAME={POSTGRES_DATABASE},"
        f"_DB_INSTANCE={POSTGRES_INSTANCE_NAME},"
        f"_SECRET_SETTINGS_NAME={SECRET_SETTINGS_NAME},"
        f"_SECRET_PASSWORD_NAME={SECRET_PASSWORD_NAME},"
        f"_STORAGE_BUCKET={CLOUD_STORAGE_BUCKET},"
    ]
    if SAMPLE_VERSION:
        substitutions.append(f"_SAMPLE_VERSION={SAMPLE_VERSION}")

    run_shell_cmd(
        [
            "gcloud",
            "builds",
            "submit",
            "--project",
            GOOGLE_CLOUD_PROJECT,
            "--config",
            "./e2e_test_cleanup.yaml",
            "--substitutions",
        ]
        + substitutions
    )


@pytest.fixture
def service_url_auth_token(deployed_service: str) -> Iterator[tuple[str, str]]:
    # Get Cloud Run service URL and auth token
    service_url = (
        run_shell_cmd(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                deployed_service,
                "--platform",
                "managed",
                "--region",
                REGION,
                "--format",
                "\"value(status.url)\"",
                "--project",
                GOOGLE_CLOUD_PROJECT,
            ]
        )
        .stdout.strip()
        .decode()
    )
    auth_token = (
        run_shell_cmd(
            [
                "gcloud",
                "auth",
                "print-identity-token",
                "--project",
                GOOGLE_CLOUD_PROJECT,
            ]
        )
        .stdout.strip()
        .decode()
    )

    yield service_url, auth_token

    # no deletion needed


def test_end_to_end(service_url_auth_token: list[str]) -> None:
    service_url, auth_token = service_url_auth_token
    headers = {"Authorization": f"Bearer {auth_token}"}
    login_slug = "/admin/login/?next=/admin/"
    client = requests.session()

    # Check homepage
    response = client.get(service_url, headers=headers)
    body = response.text

    assert response.status_code == 200
    assert "Hello, world" in body

    # Load login page, collecting csrf token
    client.get(service_url + login_slug, headers=headers)
    csrftoken = client.cookies["csrftoken"]

    # Log into Django admin
    payload = {
        "username": ADMIN_NAME,
        "password": ADMIN_PASSWORD,
        "csrfmiddlewaretoken": csrftoken,
    }
    response = client.post(service_url + login_slug, data=payload, headers=headers)
    body = response.text

    # Check Django admin landing page
    assert response.status_code == 200
    assert "Please enter the correct username and password" not in body
    assert "Site administration" in body
    assert "Polls" in body
