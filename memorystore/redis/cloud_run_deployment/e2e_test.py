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


@pytest.fixture()
def services():
    # Unique suffix to create distinct service names
    suffix = uuid.uuid4().hex[:10]
    project = os.environ["GOOGLE_CLOUD_PROJECT"]

    # Create a VPC network
    network_name = f"test-network-{suffix}"
    subprocess.run(
        [
            "gcloud",
            "compute",
            "networks",
            "create",
            network_name,
            "--project",
            project,
        ], check=True
    )

    # Create a Serverless VPC Access connector
    connector_name = f"test-connector-{suffix}"
    subprocess.run(
        [
            "gcloud",
            "compute",
            "networks",
            "vpc-access",
            "connectors",
            "create",
            connector_name,
            "--network",
            network_name,
            "--region=us-central1",
            "--range=192.168.16.0/28",
            "--project",
            project,
        ], check=True
    )

    # Create a Memorystore Redis instance
    instance_name = f"test-instance-{suffix}"
    subprocess.run(
        [
            "gcloud",
            "redis",
            "instances",
            "create",
            instance_name,
            "--region=us-central1",
            "--network",
            network_name,
            "--project",
            project,
        ], check=True
    )

    # Get the Redis instance's IP
    redis_host = subprocess.run(
        [
            "gcloud",
            "redis",
            "instances",
            "describe",
            instance_name,
            "--region=us-central1",
            "--format=value(host)",
            "--project",
            project,
        ],
        stdout=subprocess.PIPE,
        check=True
    ).stdout.strip().decode()

    # Build container image for Cloud Run deployment
    image_name = f"gcr.io/{project}/test-visit-count-{suffix}"
    subprocess.run(
        [
            "cp",
            "cloud_run_deployment/Dockerfile",
            ".",
        ], check=True
    )
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "--tag",
            image_name,
            "--project",
            project,
        ], check=True
    )
    subprocess.run(["rm", "Dockerfile"], check=True)

    # Deploy image to Cloud Run
    service_name = f"test-visit-count-{suffix}"
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--image",
            image_name,
            "--platform=managed",
            "--no-allow-unauthenticated",
            "--region=us-central1",
            "--vpc-connector",
            connector_name,
            "--set-env-vars",
            f"REDISHOST={redis_host},REDISPORT=6379",
            "--project",
            project,
        ], check=True
    )

    # Get Cloud Run service URL and auth token
    service_url = subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "describe",
            service_name,
            "--platform=managed",
            "--region=us-central1",
            "--format=value(status.url)",
            "--project",
            project,
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
            project,
        ], check=True
    )

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
            project,
        ], check=True
    )

    # Delete Redis instance
    subprocess.run(
        [
            "gcloud",
            "redis",
            "instances",
            "delete",
            instance_name,
            "--region=us-central1",
            "--quiet",
            "--async",
            "--project",
            project,
        ], check=True
    )

    # Delete Serverless VPC Access connector
    subprocess.run(
        [
            "gcloud",
            "compute",
            "networks",
            "vpc-access",
            "connectors",
            "delete",
            connector_name,
            "--region=us-central1",
            "--quiet",
            "--project",
            project,
        ], check=True
    )

    # Delete VPC network
    subprocess.run(
        [
            "gcloud",
            "compute",
            "networks",
            "delete",
            network_name,
            "--quiet",
            "--project",
            project,
        ], check=True
    )


def test_end_to_end(services):
    service_url, auth_token = services

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
