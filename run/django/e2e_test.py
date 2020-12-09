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

# This test creates a Cloud SQL instance, a Cloud Storage bucket, associated
# secrets, and deploys a Django service

import os
import subprocess
from typing import Iterator, List, Tuple
import uuid

from google.cloud import secretmanager_v1 as sm
import pytest
import requests

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
POSTGRES_INSTANCE = os.environ["POSTGRES_INSTANCE"]

# Most commands in this test require the short instance form
if ":" in POSTGRES_INSTANCE:
    POSTGRES_INSTANCE = POSTGRES_INSTANCE.split(":")[-1]

CLOUD_STORAGE_BUCKET = f"{PROJECT}-media-{SUFFIX}"

POSTGRES_DATABASE = f"polls-{SUFFIX}"
POSTGRES_USER = f"django-{SUFFIX}"
POSTGRES_PASSWORD = uuid.uuid4().hex[:26]

ADMIN_NAME = "admin"
ADMIN_PASSWORD = uuid.uuid4().hex[:26]

SECRET_SETTINGS_NAME = f"django_settings-{SUFFIX}"
SECRET_PASSWORD_NAME = f"superuser_password-{SUFFIX}"


@pytest.fixture
def project_number() -> Iterator[str]:
    projectnum = (
        subprocess.run(
            [
                "gcloud",
                "projects",
                "list",
                "--filter",
                f"name={PROJECT}",
                "--format",
                "value(projectNumber)",
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    yield projectnum


@pytest.fixture
def postgres_host() -> Iterator[str]:
    # Create database
    subprocess.run(
        [
            "gcloud",
            "sql",
            "databases",
            "create",
            POSTGRES_DATABASE,
            "--instance",
            POSTGRES_INSTANCE,
            "--project",
            PROJECT,
        ],
        check=True,
    )
    # Create User
    # NOTE Creating a user via the tutorial method is not automatable.
    subprocess.run(
        [
            "gcloud",
            "sql",
            "users",
            "create",
            POSTGRES_USER,
            "--password",
            POSTGRES_PASSWORD,
            "--instance",
            POSTGRES_INSTANCE,
            "--project",
            PROJECT,
        ],
        check=True,
    )
    yield POSTGRES_INSTANCE

    subprocess.run(
        [
            "gcloud",
            "sql",
            "databases",
            "delete",
            POSTGRES_DATABASE,
            "--instance",
            POSTGRES_INSTANCE,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )

    subprocess.run(
        [
            "gcloud",
            "sql",
            "users",
            "delete",
            POSTGRES_USER,
            "--instance",
            POSTGRES_INSTANCE,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )


@pytest.fixture
def media_bucket() -> Iterator[str]:
    # Create storage bucket
    subprocess.run(
        ["gsutil", "mb", "-l", REGION, "-p", PROJECT, f"gs://{CLOUD_STORAGE_BUCKET}"],
        check=True,
    )

    yield CLOUD_STORAGE_BUCKET

    # Recursively delete assets and bucket (does not take a -p flag, apparently)
    subprocess.run(
        ["gsutil", "-m", "rm", "-r", f"gs://{CLOUD_STORAGE_BUCKET}"],
        check=True,
    )


@pytest.fixture
def secrets(project_number: str) -> Iterator[str]:
    # Create a number of secrets and allow Google Cloud services access to them

    def create_secret(name: str, value: str) -> None:
        secret = client.create_secret(
            request={
                "parent": f"projects/{PROJECT}",
                "secret": {"replication": {"automatic": {}}},
                "secret_id": name,
            }
        )

        client.add_secret_version(
            request={"parent": secret.name, "payload": {"data": value.encode("UTF-8")}}
        )

    def allow_access(name: str, member: str) -> None:
        subprocess.run(
            [
                "gcloud",
                "secrets",
                "add-iam-policy-binding",
                name,
                "--member",
                member,
                "--role",
                "roles/secretmanager.secretAccessor",
                "--project",
                PROJECT,
            ],
            check=True,
        )

    client = sm.SecretManagerServiceClient()
    secret_key = uuid.uuid4().hex[:56]
    settings = f"""
DATABASE_URL=postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@//cloudsql/{PROJECT}:{REGION}:{POSTGRES_INSTANCE}/{POSTGRES_DATABASE}
GS_BUCKET_NAME={CLOUD_STORAGE_BUCKET}
SECRET_KEY={secret_key}
PASSWORD_NAME={SECRET_PASSWORD_NAME}
    """

    create_secret(SECRET_SETTINGS_NAME, settings)
    allow_access(
        SECRET_SETTINGS_NAME,
        f"serviceAccount:{project_number}-compute@developer.gserviceaccount.com",
    )
    allow_access(
        SECRET_SETTINGS_NAME,
        f"serviceAccount:{project_number}@cloudbuild.gserviceaccount.com",
    )

    create_secret(SECRET_PASSWORD_NAME, ADMIN_PASSWORD)
    allow_access(
        SECRET_PASSWORD_NAME,
        f"serviceAccount:{project_number}@cloudbuild.gserviceaccount.com",
    )

    yield SECRET_SETTINGS_NAME

    # delete secrets
    subprocess.run(
        [
            "gcloud",
            "secrets",
            "delete",
            SECRET_PASSWORD_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )
    subprocess.run(
        [
            "gcloud",
            "secrets",
            "delete",
            SECRET_SETTINGS_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )


@pytest.fixture
def container_image(postgres_host: str, media_bucket: str, secrets: str) -> Iterator[str]:
    # Build container image for Cloud Run deployment
    image_name = f"gcr.io/{PROJECT}/polls-{SUFFIX}"
    service_name = f"polls-{SUFFIX}"
    cloudbuild_config = "cloudmigrate.yaml"
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "--config",
            cloudbuild_config,
            "--substitutions",
            (
                f"_INSTANCE_NAME={postgres_host},"
                f"_REGION={REGION},"
                f"_SERVICE_NAME={service_name},"
                f"_SECRET_SETTINGS_NAME={SECRET_SETTINGS_NAME}"
            ),
            "--project",
            PROJECT,
        ],
        check=True,
    )
    yield image_name

    # Delete container image
    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            image_name,
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def deployed_service(container_image: str) -> Iterator[str]:
    # Deploy image to Cloud Run
    service_name = f"polls-{SUFFIX}"
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--image",
            container_image,
            "--platform=managed",
            "--no-allow-unauthenticated",
            "--region",
            REGION,
            "--add-cloudsql-instances",
            f"{PROJECT}:{REGION}:{POSTGRES_INSTANCE}",
            "--set-env-vars",
            f"SETTINGS_NAME={SECRET_SETTINGS_NAME}",
            "--project",
            PROJECT,
        ],
        check=True,
    )
    yield service_name

    # Delete Cloud Run service
    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def service_url_auth_token(deployed_service: str) -> Iterator[Tuple[str, str]]:
    # Get Cloud Run service URL and auth token
    service_url = (
        subprocess.run(
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
                "value(status.url)",
                "--project",
                PROJECT,
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    auth_token = (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token", "--project", PROJECT],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    yield service_url, auth_token

    # no deletion needed


def test_end_to_end(service_url_auth_token: List[str]) -> None:
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
    assert "Site administration" in body
    assert "Polls" in body
