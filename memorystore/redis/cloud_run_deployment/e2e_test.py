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

# This test creates a Memorystore instance, Serverless VPC Access
# connector, and Cloud Run service and tests that the Cloud Run
# service can reach the Memorystore instance.

import os
import re
import subprocess
from urllib import request
import uuid

import pytest

# Unique suffix to create distinct service names

SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
VPC_CONNECTOR_NAME = "test-connector"
MEMORYSTORE_REDIS_NAME = "static-test-instance"


@pytest.fixture
def redis_host():
    # Get the Redis instance's IP
    redis_host = subprocess.run(
        [
            "gcloud",
            "redis",
            "instances",
            "describe",
            MEMORYSTORE_REDIS_NAME,
            "--region=us-central1",
            "--format=value(host)",
            "--project",
            PROJECT,
        ],
        stdout=subprocess.PIPE,
        check=True
    ).stdout.strip().decode()
    yield redis_host

    # no deletion needs to happen, this is a "get" of a static instance


@pytest.fixture
def container_image():
    # Build container image for Cloud Run deployment
    image_name = f"gcr.io/{PROJECT}/test-visit-count-{SUFFIX}"
    subprocess.check_call(
        [
            "cp",
            "cloud_run_deployment/Dockerfile",
            ".",
        ]
    )

    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
            "--tag",
            image_name,
            "--project",
            PROJECT,
        ]
    )

    yield image_name

    subprocess.check_call(["rm", "Dockerfile"])

    # Delete container image
    subprocess.check_call(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            image_name,
            "--quiet",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture
def deployed_service(container_image, redis_host):
    # Deploy image to Cloud Run
    service_name = f"test-visit-count-{SUFFIX}"
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--image",
            container_image,
            "--platform=managed",
            "--no-allow-unauthenticated",
            "--region=us-central1",
            "--vpc-connector",
            VPC_CONNECTOR_NAME,
            "--set-env-vars",
            f"REDISHOST={redis_host},REDISPORT=6379",
            "--project",
            PROJECT,
        ]
    )
    yield service_name

    # Delete Cloud Run service
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--async",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture
def service_url_auth_token(deployed_service):
    # Get Cloud Run service URL and auth token
    service_url = subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "describe",
            deployed_service,
            "--platform=managed",
            "--region=us-central1",
            "--format=value(status.url)",
            "--project",
            PROJECT,
        ],
        stdout=subprocess.PIPE,
        check=True
    ).stdout.strip().decode()
    auth_token = subprocess.run(
        ["gcloud", "auth", "print-identity-token"],
        stdout=subprocess.PIPE,
        check=True
    ).stdout.strip().decode()

    yield service_url, auth_token

    # no deletion needed


def test_end_to_end(service_url_auth_token):
    service_url, auth_token = service_url_auth_token

    req = request.Request(
        service_url,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    response = request.urlopen(req)
    assert response.status == 200

    body = response.read().decode()
    assert re.search(r"Visitor number: \d+", body) is not None
