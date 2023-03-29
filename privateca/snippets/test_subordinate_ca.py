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

import random
import re
import typing
import uuid

import backoff
import google.auth
import google.cloud.security.privateca_v1 as privateca_v1

from activate_subordinate_ca import activate_subordinate_ca
from conftest import LOCATION
from create_certificate_csr import create_certificate_csr
from create_subordinate_ca import create_subordinate_ca
from revoke_certificate import revoke_certificate

PROJECT = google.auth.default()[1]
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CA_DURATION = CERTIFICATE_LIFETIME = 1000000
DOMAIN_NAME = "domain.com"


def generate_name() -> str:
    return "test-" + uuid.uuid4().hex[:10]


# We are hitting 5 CAs per minute limit which can't be changed
# We set the backoff function to use 4 as base - this way the 3rd try
# should wait for 64 seconds and avoid per minute quota
# Adding some random amount of time to the backoff timer, so that we
# don't try to call the API at the same time in different tests running
# simultaneously.
def backoff_expo_wrapper():
    for exp in backoff.expo(base=4):
        if exp is None:
            yield None
        yield exp * (1 + random.random())


@backoff.on_exception(backoff_expo_wrapper, Exception, max_tries=3)
def test_subordinate_certificate_authority(
    certificate_authority, capsys: typing.Any
) -> None:
    CSR_CERT_NAME = generate_name()
    SUBORDINATE_CA_NAME = generate_name()

    CA_POOL_NAME, ROOT_CA_NAME = certificate_authority

    # 1. Create a Subordinate Certificate Authority.
    create_subordinate_ca(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        SUBORDINATE_CA_NAME,
        COMMON_NAME,
        ORGANIZATION,
        DOMAIN_NAME,
        CA_DURATION,
    )

    # 2. Fetch CSR of the given CA.
    ca_service_client = privateca_v1.CertificateAuthorityServiceClient()

    ca_path = ca_service_client.certificate_authority_path(
        PROJECT, LOCATION, CA_POOL_NAME, SUBORDINATE_CA_NAME
    )
    response = ca_service_client.fetch_certificate_authority_csr(name=ca_path)
    pem_csr = response.pem_csr

    # 3. Sign the CSR and create a certificate.
    create_certificate_csr(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        ROOT_CA_NAME,
        CSR_CERT_NAME,
        CERTIFICATE_LIFETIME,
        pem_csr,
    )

    # 4. Get certificate PEM format
    certificate_name = ca_service_client.certificate_path(
        PROJECT, LOCATION, CA_POOL_NAME, CSR_CERT_NAME
    )
    pem_certificate = ca_service_client.get_certificate(
        name=certificate_name
    ).pem_certificate

    # 5. Activate Subordinate CA
    activate_subordinate_ca(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        SUBORDINATE_CA_NAME,
        pem_certificate,
        ROOT_CA_NAME,
    )

    revoke_certificate(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        CSR_CERT_NAME,
    )

    out, _ = capsys.readouterr()

    assert re.search(
        f'Operation result: name: "projects/{PROJECT}/locations/{LOCATION}/caPools/{CA_POOL_NAME}/certificateAuthorities/{SUBORDINATE_CA_NAME}"',
        out,
    )

    assert "Certificate created successfully" in out
    assert f"Current state: {privateca_v1.CertificateAuthority.State.STAGED}" in out
