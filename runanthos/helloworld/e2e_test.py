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

# This sample creates a workload running on Cloud Run for Anthos.
# This test builds and deploys the workload and tests if it responds as
# expected.

import os
import subprocess
from urllib import request
import uuid

import pytest

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
CRFA_CLUSTER = os.environ["CRFA_CLUSTER"]
CRFA_CLUSTER_ZONE = os.environ["CRFA_CLUSTER_ZONE"]
IMAGE_NAME = f"gcr.io/{PROJECT}/helloworld-{SUFFIX}"


@pytest.fixture
def container_image():
    # Build container image for CRfA deployment
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "--tag",
            IMAGE_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )
    yield IMAGE_NAME

    # Delete container image
    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def deployed_service(container_image):
    # Deploy image to CRfA
    service_name = f"helloworld-{SUFFIX}"
    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--platform=managed",
            "--image",
            container_image,
            "--project",
            PROJECT,
            "--cluster", 
            CRFA_CLUSTER,
            "--cluster-location",
            CRFA_CLUSTER_ZONE,
        ],
        check=True,
    )

    yield service_name

    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--platform=managed",
            "--project",
            PROJECT,
            "--cluster",
            CRFA_CLUSTER,
            "--cluster-location",
            CRFA_CLUSTER_ZONE,
            "--quiet",
        ],
        check=True,
    )


@pytest.fixture
def crfa_cluster_ingress_address(deployed_service):
    service_name = deployed_service

    # Get the IP address of the load balancer associated with the Istio ingress
    # in the CRfA cluster
    ingress_addr = (
        subprocess.run(
            [
                "kubectl",
                "-n",
                "gke-system",
                "get",
                "svc",
                "istio-ingress",
                "-o",
                " "
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()[1:-1]
    )

    yield service_name, ingress_addr


def test_end_to_end(crfa_cluster_ingress_address):
    service_name, ingress_addr = crfa_cluster_ingress_address
  
    req = request.Request(
        f"http://{ingress_addr}",
        headers={
            "Host": f"{service_name}.default.example.com",
        }
    )
    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    assert "Hello World!" == body.decode()
