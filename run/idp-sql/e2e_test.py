# Copyright 2021 Google LLC
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

import json
import os
import subprocess
from datetime import date

import uuid

import firebase_admin  # noqa: F401
from firebase_admin import auth  # noqa: F401
import pytest
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

default_app = firebase_admin.initialize_app()

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", None)
if not GOOGLE_CLOUD_PROJECT:
    raise Exception("'GOOGLE_CLOUD_PROJECT' env var not found")

SERVICE_NAME = os.environ.get("SERVICE_NAME", None)
if not SERVICE_NAME:
    print(
        "'SERVICE_NAME' envvar not found. Defaulting to 'idp-sql' with a unique suffix"
    )
    SERVICE_NAME = f"idp-sql-{SUFFIX}"

SAMPLE_VERSION = os.environ.get("SAMPLE_VERSION", None)

REGION = "us-central1"
PLATFORM = "managed"

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

POSTGRES_DATABASE = f"idp-sql-database-{SUFFIX}"

POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
if not POSTGRES_PASSWORD:
    raise Exception("'POSTGRES_PASSWORD' env var not found")

# Firebase key to create Id Tokens
IDP_KEY = os.environ.get("IDP_KEY", None)
if not IDP_KEY:
    raise Exception("'IDP_KEY' env var not found")


retry_strategy = Retry(
    total=5,
    status_forcelist=[400, 401, 403, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
    backoff_factor=5
)

retry_strategy_500 = Retry(
    total=5,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
    backoff_factor=5
)


@pytest.fixture
def deployed_service() -> str:
    substitutions = [
        f"_SERVICE={SERVICE_NAME},"
        f"_PLATFORM={PLATFORM},"
        f"_REGION={REGION},"
        f"_DB_NAME={POSTGRES_DATABASE},"
        f"_DB_INSTANCE={POSTGRES_INSTANCE_NAME},"
        f"_DB_PASSWORD={POSTGRES_PASSWORD},"
        f"_CLOUD_SQL_CONNECTION_NAME={POSTGRES_INSTANCE_FULL},"
    ]
    if SAMPLE_VERSION:
        substitutions.append(f"_SAMPLE_VERSION={SAMPLE_VERSION}")

    subprocess.check_call(
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

    service_url = (
        subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                SERVICE_NAME,
                "--project",
                GOOGLE_CLOUD_PROJECT,
                "--platform",
                PLATFORM,
                "--region",
                REGION,
                "--format",
                "value(status.url)",
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    yield service_url

    # Cleanup

    substitutions = [
        f"_SERVICE={SERVICE_NAME},"
        f"_PLATFORM={PLATFORM},"
        f"_REGION={REGION},"
        f"_DB_NAME={POSTGRES_DATABASE},"
        f"_DB_INSTANCE={POSTGRES_INSTANCE_NAME},"
    ]
    if SAMPLE_VERSION:
        substitutions.append(f"_SAMPLE_VERSION={SAMPLE_VERSION}")

    subprocess.check_call(
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
def jwt_token() -> str:
    custom_token = auth.create_custom_token("a-user-id").decode("UTF-8")
    adapter = HTTPAdapter(max_retries=retry_strategy)

    client = requests.session()
    client.mount("https://", adapter)

    resp = client.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={IDP_KEY}",
        data=json.dumps({"token": custom_token, "returnSecureToken": True}),
    )
    response = resp.json()
    assert "error" not in response.keys()
    assert "idToken" in response.keys()

    id_token = response["idToken"]
    yield id_token

    # no cleanup required


def test_end_to_end(jwt_token: str, deployed_service: str) -> None:

    if date.today() > date(2023, 6, 5):
        raise Exception(
            'REMINDER: Remove urllib3<2.0.0, and this exception code, if no longer needed (otherwise bump the date later).'
            'Context: https://github.com/GoogleCloudPlatform/python-docs-samples/pull/9903'
        )

    token = jwt_token
    service_url = deployed_service

    adapter = HTTPAdapter(max_retries=retry_strategy)

    client = requests.session()
    client.mount("https://", adapter)

    # Can successfully make a request
    response = client.get(service_url)
    assert response.status_code == 200

    # Can make post with token
    response = client.post(
        service_url, data={"team": "DOGS"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Vote successfully cast" in response.content.decode("UTF-8")

    # Confirm updated results
    response = client.get(service_url)
    assert response.status_code == 200
    assert "🐶" in response.content.decode("UTF-8")

    adapter = HTTPAdapter(max_retries=retry_strategy_500)
    client.mount("https://", adapter)
    # Cannot make post with bad token
    response = client.post(
        service_url,
        data={"team": "DOGS"},
        headers={"Authorization": "Bearer iam-a-token"},
    )
    assert response.status_code == 403

    # Cannot make post with no token
    response = client.post(service_url, data={"team": "DOGS"})
    assert response.status_code == 401
