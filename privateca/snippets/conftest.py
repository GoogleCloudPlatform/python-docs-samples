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

from multiprocessing import Pool
import os
import random
import uuid

import backoff
from google.api_core.exceptions import FailedPrecondition
from google.api_core.exceptions import ServiceUnavailable
import google.auth
from google.cloud.security import privateca_v1
import pytest

from create_ca_pool import create_ca_pool
from create_certificate_authority import create_certificate_authority
from create_certificate_template import create_certificate_template
from delete_certificate_authority import delete_certificate_authority
from delete_certificate_template import delete_certificate_template
from disable_certificate_authority import disable_certificate_authority
from enable_certificate_authority import enable_certificate_authority

PROJECT = google.auth.default()[1]
LOCATIONS = ("us-central1", "europe-north1", "europe-central2", "europe-west2", "us-east4", "europe-west1")
LOCATION = random.choice(LOCATIONS)
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CA_DURATION = 1000000


def delete_cas_from_pool(ca_pool_name: str) -> None:
    client = privateca_v1.CertificateAuthorityServiceClient()
    for ca in client.list_certificate_authorities(parent=ca_pool_name):
        # Check if the CA is enabled.
        if ca.state == privateca_v1.CertificateAuthority.State.ENABLED:
            request = privateca_v1.DisableCertificateAuthorityRequest(name=ca.name)
            client.disable_certificate_authority(request=request)

        # Delete CA.
        ca_state = client.get_certificate_authority(name=ca.name).state
        try:
            if ca_state != privateca_v1.CertificateAuthority.State.DELETED:
                delete_ca_request = privateca_v1.DeleteCertificateAuthorityRequest()
                delete_ca_request.name = ca.name
                delete_ca_request.ignore_active_certificates = True
                delete_ca_request.skip_grace_period = True
                client.delete_certificate_authority(request=delete_ca_request).result(
                    timeout=300
                )
                print(f" * {ca.name} Deleted!")
        except FailedPrecondition as err:
            print(err)
            continue


def delete_one_pool(ca_pool_name: str) -> None:
    client = privateca_v1.CertificateAuthorityServiceClient()
    try:
        delete_ca_pool_request = privateca_v1.DeleteCaPoolRequest()
        delete_ca_pool_request.name = ca_pool_name
        print(f"Deleting {ca_pool_name}")
        client.delete_ca_pool(request=delete_ca_pool_request).result(timeout=300)
    except FailedPrecondition:
        print(f"Precondition failed for {ca_pool_name} :(")


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=3)
def delete_stale_resources() -> None:
    client = privateca_v1.CertificateAuthorityServiceClient()
    pool_names = []
    for location in LOCATIONS:
        location_path = client.common_location_path(PROJECT, location)
        request = privateca_v1.ListCaPoolsRequest(parent=location_path)
        for ca_pool in client.list_ca_pools(request=request):
            pool_names.append(ca_pool.name)

    with Pool(max(2, os.cpu_count() - 2)) as p:
        print(f"Going to clean up CAs from {len(pool_names)} pools.")
        p.map(delete_cas_from_pool, pool_names)

    with Pool(max(2, os.cpu_count() - 2)) as p:
        print(f"Going to delete {len(pool_names)} pools.")
        p.map(delete_one_pool, pool_names)


def generate_name() -> str:
    return "test-" + uuid.uuid4().hex[:10]


@pytest.fixture
def ca_pool(ca_pool_autodelete_name):
    create_ca_pool(PROJECT, LOCATION, ca_pool_autodelete_name)
    yield ca_pool_autodelete_name


@pytest.fixture
def certificate_authority(ca_pool):
    CA_NAME = generate_name()

    create_certificate_authority(
        PROJECT, LOCATION, ca_pool, CA_NAME, COMMON_NAME, ORGANIZATION, CA_DURATION
    )

    yield ca_pool, CA_NAME

    # CA Pool cleanup will remove the certificate.
    # delete_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)


@pytest.fixture
def deleted_certificate_authority(ca_pool):
    CA_NAME = generate_name()

    create_certificate_authority(
        PROJECT, LOCATION, ca_pool, CA_NAME, COMMON_NAME, ORGANIZATION, CA_DURATION
    )

    enable_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)
    disable_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)
    delete_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)

    yield ca_pool, CA_NAME


@pytest.fixture
def certificate_template():
    TEMPLATE_NAME = generate_name()

    create_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)

    yield TEMPLATE_NAME

    delete_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)


@pytest.fixture
def ca_pool_autodelete_name():
    name = generate_name()
    yield name
    ca_client = privateca_v1.CertificateAuthorityServiceClient()

    ca_pool_path = ca_client.ca_pool_path(PROJECT, LOCATION, name)
    delete_cas_from_pool(ca_pool_path)
    delete_one_pool(ca_pool_path)


@pytest.fixture
def ca_pool_autodelete_name2():
    name = generate_name()
    yield name
    ca_client = privateca_v1.CertificateAuthorityServiceClient()

    ca_pool_path = ca_client.ca_pool_path(PROJECT, LOCATION, name)
    delete_cas_from_pool(ca_pool_path)
    delete_one_pool(ca_pool_path)
