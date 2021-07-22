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


import time
import typing
import uuid

import google.auth
from google.cloud import kms

from create_certificate import create_certificate
from disable_certificate_authority import disable_certificate_authority
from enable_certificate_authority import enable_certificate_authority
from revoke_certificate import revoke_certificate


PROJECT = google.auth.default()[1]
LOCATION = "europe-west1"
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CERTIFICATE_LIFETIME = 1000000
KEY_VERSION = 1
DOMAIN_NAME = "domain.com"


def generate_name() -> str:
    return "test-" + uuid.uuid4().hex[:10]


def test_create_and_revoke_certificate_authority(
    certificate_authority, capsys: typing.Any
) -> None:
    KEY_RING_ID = generate_name()
    CRYPTO_KEY_ID = generate_name()
    CERT_NAME = generate_name()

    CA_POOL_NAME, CA_NAME = certificate_authority
    enable_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)

    kms_client = kms.KeyManagementServiceClient()

    kms_location_name = kms_client.common_location_path(PROJECT, LOCATION)

    kms_client.create_key_ring(
        request={
            "parent": kms_location_name,
            "key_ring_id": KEY_RING_ID,
            "key_ring": {},
        }
    )

    key_ring_path = kms_client.key_ring_path(PROJECT, LOCATION, KEY_RING_ID)

    purpose = kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
    algorithm = (
        kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PKCS1_4096_SHA256
    )
    key = {
        "purpose": purpose,
        "version_template": {
            "algorithm": algorithm,
        },
    }

    kms_client.create_crypto_key(
        request={
            "parent": key_ring_path,
            "crypto_key_id": CRYPTO_KEY_ID,
            "crypto_key": key,
        }
    )

    # Wait while crypto key is generating
    time.sleep(30)

    create_certificate(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        CA_NAME,
        CERT_NAME,
        LOCATION,
        KEY_RING_ID,
        CRYPTO_KEY_ID,
        KEY_VERSION,
        COMMON_NAME,
        DOMAIN_NAME,
        CERTIFICATE_LIFETIME,
    )

    revoke_certificate(
        PROJECT,
        LOCATION,
        CA_POOL_NAME,
        CERT_NAME,
    )

    disable_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)

    out, _ = capsys.readouterr()

    assert "Certificate creation result:" in out
    assert "Certificate revoke result:" in out
