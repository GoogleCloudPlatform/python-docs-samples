# Copyright 2021 Google LLC
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

import uuid

import google.auth
import pytest
from google.cloud.security import privateca_v1

from create_ca_pool import create_ca_pool
from create_certificate_authority import create_certificate_authority
from create_certificate_template import create_certificate_template
from delete_ca_pool import delete_ca_pool
from delete_certificate_authority import delete_certificate_authority
from delete_certificate_template import delete_certificate_template

PROJECT = google.auth.default()[1]
LOCATION = "us-central1"
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CA_DURATION = 1000000


def delete_ca(ca_pool_name: str) -> None:
    client = privateca_v1.CertificateAuthorityServiceClient()
    for ca in client.list_certificate_authorities(parent=ca_pool_name):
        # Check if the CA is enabled.
        ca_state = client.get_certificate_authority(name=ca.name).state
        if ca_state == privateca_v1.CertificateAuthority.State.ENABLED:
            request = privateca_v1.DisableCertificateAuthorityRequest(name=ca.name)
            client.disable_certificate_authority(request=request)

        # Delete CA.
        delete_ca_request = privateca_v1.DeleteCertificateAuthorityRequest()
        delete_ca_request.name = ca.name
        delete_ca_request.ignore_active_certificates = True
        delete_ca_request.skip_grace_period = True
        client.delete_certificate_authority(request=delete_ca_request).result(timeout=300)


def delete_capool() -> None:
    client = privateca_v1.CertificateAuthorityServiceClient()
    location_path = client.common_location_path(PROJECT, LOCATION)
    request = privateca_v1.ListCaPoolsRequest(parent=location_path)
    # List CA pools.
    for ca_pool in client.list_ca_pools(request=request):
        ca_pool_name = ca_pool.name
        # Delete CA.
        delete_ca(ca_pool_name)
        # Delete CA pool.
        delete_ca_pool_request = privateca_v1.DeleteCaPoolRequest()
        delete_ca_pool_request.name = ca_pool_name
        client.delete_ca_pool(request=delete_ca_pool_request).result(timeout=300)


def delete_stale_resources() -> None:
    delete_capool()


def generate_name() -> str:
    return "test-" + uuid.uuid4().hex[:10]


@pytest.fixture
def ca_pool():
    CA_POOL_NAME = generate_name()

    create_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)

    yield CA_POOL_NAME

    delete_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)


@pytest.fixture
def certificate_authority(ca_pool):
    CA_NAME = generate_name()

    create_certificate_authority(
        PROJECT, LOCATION, ca_pool, CA_NAME, COMMON_NAME, ORGANIZATION, CA_DURATION
    )

    yield ca_pool, CA_NAME

    delete_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)


@pytest.fixture
def deleted_certificate_authority(ca_pool):
    CA_NAME = generate_name()

    create_certificate_authority(
        PROJECT, LOCATION, ca_pool, CA_NAME, COMMON_NAME, ORGANIZATION, CA_DURATION
    )

    delete_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)

    yield ca_pool, CA_NAME


@pytest.fixture
def certificate_template():
    TEMPLATE_NAME = generate_name()

    create_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)

    yield TEMPLATE_NAME

    delete_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)
