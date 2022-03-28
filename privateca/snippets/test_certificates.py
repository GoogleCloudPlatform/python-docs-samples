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


import re
import time
import typing
import uuid

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat

import google.auth

from create_certificate import create_certificate
from disable_certificate_authority import disable_certificate_authority
from enable_certificate_authority import enable_certificate_authority
from filter_certificates import filter_certificates
from revoke_certificate import revoke_certificate


PROJECT = google.auth.default()[1]
LOCATION = "europe-west1"
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CERTIFICATE_LIFETIME = 1000000
DOMAIN_NAME = "domain.com"


def generate_name() -> str:
    return "test-" + uuid.uuid4().hex[:10]


def test_create_and_revoke_certificate_authority(
    certificate_authority, capsys: typing.Any
) -> None:
    CERT_NAME = generate_name()

    CA_POOL_NAME, CA_NAME = certificate_authority
    enable_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=backend
    )

    public_key_bytes = private_key.public_key().public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    )

    # Wait while crypto key is generating
    time.sleep(5)

    create_certificate(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        CA_NAME,
        CERT_NAME,
        COMMON_NAME,
        DOMAIN_NAME,
        CERTIFICATE_LIFETIME,
        public_key_bytes,
    )

    FILTER_CONDITION = (
        f"certificate_description.subject_description.subject.common_name={COMMON_NAME}"
    )
    filter_certificates(PROJECT, LOCATION, CA_POOL_NAME, FILTER_CONDITION)

    revoke_certificate(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        CERT_NAME,
    )

    disable_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)

    out, _ = capsys.readouterr()
    assert "Certificate creation result:" in out
    assert "Available certificates:" in out
    assert re.search(
        f"- projects/.*/locations/{LOCATION}/caPools/{CA_POOL_NAME}/certificates/{CERT_NAME}",
        out,
    )
    assert "Certificate revoke result:" in out
