# Copyright 2017 Google, Inc
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
"""
Tests for the KMS samples.

The service account running the tests needs to have the following roles:
 * roles/cloudkms.admin
 * roles/cloudkms.cryptoKeyEncrypterDecrypter
 * roles/cloudkms.cryptoOperator
 * roles/cloudkms.publicKeyViewer
 * roles/cloudkms.signerVerifier
"""

import datetime
import hashlib
import os
import time
from typing import Iterator
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from google.cloud import kms
import pytest

from check_state_import_job import check_state_import_job
from check_state_imported_key import check_state_imported_key
from create_import_job import create_import_job
from create_key_asymmetric_decrypt import create_key_asymmetric_decrypt
from create_key_asymmetric_sign import create_key_asymmetric_sign
from create_key_for_import import create_key_for_import
from create_key_hsm import create_key_hsm
from create_key_labels import create_key_labels
from create_key_mac import create_key_mac
from create_key_ring import create_key_ring
from create_key_rotation_schedule import create_key_rotation_schedule
from create_key_symmetric_encrypt_decrypt import \
    create_key_symmetric_encrypt_decrypt
from create_key_version import create_key_version
from decrypt_asymmetric import decrypt_asymmetric
from decrypt_symmetric import decrypt_symmetric
from destroy_key_version import destroy_key_version
from disable_key_version import disable_key_version
from enable_key_version import enable_key_version
from encrypt_asymmetric import encrypt_asymmetric
from encrypt_symmetric import encrypt_symmetric
from generate_random_bytes import generate_random_bytes
from get_key_labels import get_key_labels
from get_key_version_attestation import get_key_version_attestation
from get_public_key import get_public_key
from get_public_key_jwk import get_public_key_jwk
from iam_add_member import iam_add_member
from iam_get_policy import iam_get_policy
from iam_remove_member import iam_remove_member
from import_manually_wrapped_key import import_manually_wrapped_key
from quickstart import quickstart
from restore_key_version import restore_key_version
from sign_asymmetric import sign_asymmetric
from sign_mac import sign_mac
from update_key_add_rotation import update_key_add_rotation
from update_key_remove_labels import update_key_remove_labels
from update_key_remove_rotation import update_key_remove_rotation
from update_key_set_primary import update_key_set_primary
from update_key_update_labels import update_key_update_labels
from verify_asymmetric_ec import verify_asymmetric_ec
from verify_asymmetric_rsa import verify_asymmetric_rsa
from verify_mac import verify_mac


@pytest.fixture(scope="module")
def client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()


@pytest.fixture(scope="module")
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="module")
def location_id() -> str:
    return "us-east1"


@pytest.fixture(scope="module")
def import_job_id() -> str:
    return "my-import-job"


@pytest.fixture(scope="module")
def import_tests_key_id() -> str:
    return "my-import-job-ec-key"


@pytest.fixture(scope="module")
def key_ring_id(
    client: kms.KeyManagementServiceClient, project_id: str, location_id: str
) -> Iterator[kms.KeyRing]:
    location_name = f"projects/{project_id}/locations/{location_id}"
    key_ring_id = f"{uuid.uuid4()}"
    key_ring = client.create_key_ring(
        request={"parent": location_name, "key_ring_id": key_ring_id, "key_ring": {}}
    )

    yield key_ring_id

    for key in client.list_crypto_keys(request={"parent": key_ring.name}):
        if key.rotation_period or key.next_rotation_time:
            updated_key = {"name": key.name}
            update_mask = {"paths": ["rotation_period", "next_rotation_time"]}
            client.update_crypto_key(
                request={"crypto_key": updated_key, "update_mask": update_mask}
            )

        f = "state != DESTROYED AND state != DESTROY_SCHEDULED"
        for version in client.list_crypto_key_versions(
            request={"parent": key.name, "filter": f}
        ):
            client.destroy_crypto_key_version(request={"name": version.name})


@pytest.fixture(scope="module")
def asymmetric_decrypt_key_id(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
) -> str:
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    key_id = f"{uuid.uuid4()}"
    key = client.create_crypto_key(
        request={
            "parent": key_ring_name,
            "crypto_key_id": key_id,
            "crypto_key": {
                "purpose": kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT,
                "version_template": {
                    "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_DECRYPT_OAEP_2048_SHA256
                },
                "labels": {"foo": "bar", "zip": "zap"},
            },
        }
    )
    wait_for_ready(client, f"{key.name}/cryptoKeyVersions/1")
    return key_id


@pytest.fixture(scope="module")
def asymmetric_sign_ec_key_id(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
) -> str:
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    key_id = f"{uuid.uuid4()}"
    key = client.create_crypto_key(
        request={
            "parent": key_ring_name,
            "crypto_key_id": key_id,
            "crypto_key": {
                "purpose": kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN,
                "version_template": {
                    "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.EC_SIGN_P256_SHA256
                },
                "labels": {"foo": "bar", "zip": "zap"},
            },
        }
    )
    wait_for_ready(client, f"{key.name}/cryptoKeyVersions/1")
    return key_id


@pytest.fixture(scope="module")
def asymmetric_sign_rsa_key_id(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
) -> str:
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    key_id = f"{uuid.uuid4()}"
    key = client.create_crypto_key(
        request={
            "parent": key_ring_name,
            "crypto_key_id": key_id,
            "crypto_key": {
                "purpose": kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN,
                "version_template": {
                    "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PKCS1_2048_SHA256
                },
                "labels": {"foo": "bar", "zip": "zap"},
            },
        }
    )
    wait_for_ready(client, f"{key.name}/cryptoKeyVersions/1")
    return key_id


@pytest.fixture(scope="module")
def hsm_key_id(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
) -> str:
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    key_id = f"{uuid.uuid4()}"
    key = client.create_crypto_key(
        request={
            "parent": key_ring_name,
            "crypto_key_id": key_id,
            "crypto_key": {
                "purpose": kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                "version_template": {
                    "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
                    "protection_level": kms.ProtectionLevel.HSM,
                },
                "labels": {"foo": "bar", "zip": "zap"},
            },
        }
    )
    wait_for_ready(client, f"{key.name}/cryptoKeyVersions/1")
    return key_id


@pytest.fixture(scope="module")
def hmac_key_id(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
) -> str:
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    key_id = f"{uuid.uuid4()}"
    key = client.create_crypto_key(
        request={
            "parent": key_ring_name,
            "crypto_key_id": key_id,
            "crypto_key": {
                "purpose": kms.CryptoKey.CryptoKeyPurpose.MAC,
                "version_template": {
                    "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.HMAC_SHA256,
                    "protection_level": kms.ProtectionLevel.HSM,
                },
                "labels": {"foo": "bar", "zip": "zap"},
            },
        }
    )
    wait_for_ready(client, f"{key.name}/cryptoKeyVersions/1")
    return key_id


@pytest.fixture(scope="module")
def symmetric_key_id(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
) -> str:
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    key_id = f"{uuid.uuid4()}"
    key = client.create_crypto_key(
        request={
            "parent": key_ring_name,
            "crypto_key_id": key_id,
            "crypto_key": {
                "purpose": kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
                "version_template": {
                    "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
                },
                "labels": {"foo": "bar", "zip": "zap"},
            },
        }
    )
    wait_for_ready(client, f"{key.name}/cryptoKeyVersions/1")
    return key_id


def wait_for_ready(
    client: kms.KeyManagementServiceClient, key_version_name: str
) -> None:
    for i in range(4):
        key_version = client.get_crypto_key_version(request={"name": key_version_name})
        if key_version.state == kms.CryptoKeyVersion.CryptoKeyVersionState.ENABLED:
            return
        time.sleep((i + 1) ** 2)
    pytest.fail(f"{key_version_name} not ready")


def test_create_import_job(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    import_job_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
    create_import_job(project_id, location_id, key_ring_id, import_job_id)
    out, _ = capsys.readouterr()
    assert "Created import job" in out


def test_check_state_import_job(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    import_job_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
    check_state_import_job(project_id, location_id, key_ring_id, import_job_id)
    out, _ = capsys.readouterr()
    assert "Current state" in out


def test_check_state_imported_key(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    import_job_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
    check_state_imported_key(project_id, location_id, key_ring_id, import_job_id)
    out, _ = capsys.readouterr()
    assert "Current state" in out


def test_create_key_asymmetric_decrypt(
    project_id: str, location_id: str, key_ring_id: str
) -> None:
    key_id = f"{uuid.uuid4()}"
    key = create_key_asymmetric_decrypt(project_id, location_id, key_ring_id, key_id)
    assert key.purpose == kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT
    assert (
        key.version_template.algorithm
        == kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_DECRYPT_OAEP_2048_SHA256
    )


def test_create_key_asymmetric_sign(
    project_id: str, location_id: str, key_ring_id: str
) -> None:
    key_id = f"{uuid.uuid4()}"
    key = create_key_asymmetric_sign(project_id, location_id, key_ring_id, key_id)
    assert key.purpose == kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
    assert (
        key.version_template.algorithm
        == kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PKCS1_2048_SHA256
    )


def test_create_key_for_import(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    import_tests_key_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
    create_key_for_import(project_id, location_id, key_ring_id, import_tests_key_id)
    out, _ = capsys.readouterr()
    assert "Created hsm key" in out


def test_create_key_hsm(project_id: str, location_id: str, key_ring_id: str) -> None:
    key_id = f"{uuid.uuid4()}"
    key = create_key_hsm(project_id, location_id, key_ring_id, key_id)
    assert key.purpose == kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert (
        key.version_template.algorithm
        == kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert key.version_template.protection_level == kms.ProtectionLevel.HSM


def test_create_key_labels(project_id: str, location_id: str, key_ring_id: str) -> None:
    key_id = f"{uuid.uuid4()}"
    key = create_key_labels(project_id, location_id, key_ring_id, key_id)
    assert key.purpose == kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert (
        key.version_template.algorithm
        == kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )
    assert key.labels == {"team": "alpha", "cost_center": "cc1234"}


def test_create_key_mac(project_id: str, location_id: str, key_ring_id: str) -> None:
    key_id = f"{uuid.uuid4()}"
    key = create_key_mac(project_id, location_id, key_ring_id, key_id)
    assert key.purpose == kms.CryptoKey.CryptoKeyPurpose.MAC
    assert (
        key.version_template.algorithm
        == kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.HMAC_SHA256
    )


def test_create_key_ring(project_id: str, location_id: str, key_ring_id: str) -> None:
    key_ring_id = f"{uuid.uuid4()}"
    key_ring = create_key_ring(project_id, location_id, key_ring_id)
    assert key_ring


def test_create_key_rotation_schedule(
    project_id: str, location_id: str, key_ring_id: str
) -> None:
    key_id = f"{uuid.uuid4()}"
    key = create_key_rotation_schedule(project_id, location_id, key_ring_id, key_id)
    assert key.rotation_period == datetime.timedelta(seconds=60 * 60 * 24 * 30)
    assert key.next_rotation_time


def test_create_key_symmetric_encrypt_decrypt(
    project_id: str, location_id: str, key_ring_id: str
) -> None:
    key_id = f"{uuid.uuid4()}"
    key = create_key_symmetric_encrypt_decrypt(
        project_id, location_id, key_ring_id, key_id
    )
    assert key.purpose == kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    assert (
        key.version_template.algorithm
        == kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    )


def test_create_key_version(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    version = create_key_version(project_id, location_id, key_ring_id, symmetric_key_id)
    assert version


def test_decrypt_asymmetric(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_decrypt_key_id: str,
) -> None:
    message = b"my message"

    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, "1"
    )
    public_key = client.get_public_key(request={"name": key_version_name})

    pem = public_key.pem.encode("utf-8")
    rsa_key = serialization.load_pem_public_key(pem, default_backend())

    pad = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
    ciphertext = rsa_key.encrypt(message, pad)

    response = decrypt_asymmetric(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, "1", ciphertext
    )
    assert response.plaintext == message


def test_decrypt_symmetric(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    symmetric_key_id: str,
) -> None:
    plaintext = b"my message"

    key_version_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, symmetric_key_id
    )
    encrypt_response = client.encrypt(
        request={"name": key_version_name, "plaintext": plaintext}
    )
    ciphertext = encrypt_response.ciphertext

    decrypt_response = decrypt_symmetric(
        project_id, location_id, key_ring_id, symmetric_key_id, ciphertext
    )
    assert decrypt_response.plaintext == plaintext


def test_destroy_restore_key_version(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_decrypt_key_id: str,
) -> None:
    key_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id
    )
    version = client.create_crypto_key_version(
        request={"parent": key_name, "crypto_key_version": {}}
    )
    version_id = version.name.split("/")[-1]

    wait_for_ready(client, version.name)

    destroyed_version = destroy_key_version(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, version_id
    )
    assert (
        destroyed_version.state
        == kms.CryptoKeyVersion.CryptoKeyVersionState.DESTROY_SCHEDULED
    )

    restored_version = restore_key_version(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, version_id
    )
    assert restored_version.state == kms.CryptoKeyVersion.CryptoKeyVersionState.DISABLED


def test_disable_enable_key_version(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_decrypt_key_id: str,
) -> None:
    key_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id
    )
    version = client.create_crypto_key_version(
        request={"parent": key_name, "crypto_key_version": {}}
    )
    version_id = version.name.split("/")[-1]

    wait_for_ready(client, version.name)

    disabled_version = disable_key_version(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, version_id
    )
    assert disabled_version.state == kms.CryptoKeyVersion.CryptoKeyVersionState.DISABLED

    enabled_version = enable_key_version(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, version_id
    )
    assert enabled_version.state == kms.CryptoKeyVersion.CryptoKeyVersionState.ENABLED


def test_encrypt_asymmetric(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_decrypt_key_id: str,
) -> None:
    plaintext = "my message"
    ciphertext = encrypt_asymmetric(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, "1", plaintext
    )

    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, "1"
    )
    response = client.asymmetric_decrypt(
        request={"name": key_version_name, "ciphertext": ciphertext}
    )
    assert response.plaintext == plaintext.encode("utf-8")


def test_encrypt_symmetric(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    symmetric_key_id: str,
) -> None:
    plaintext = "my message"
    encrypt_response = encrypt_symmetric(
        project_id, location_id, key_ring_id, symmetric_key_id, plaintext
    )

    key_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, symmetric_key_id
    )
    decrypt_response = client.decrypt(
        request={"name": key_name, "ciphertext": encrypt_response.ciphertext}
    )
    assert decrypt_response.plaintext == plaintext.encode("utf-8")


def test_generate_random_bytes(
    client: kms.KeyManagementServiceClient, project_id: str, location_id: str
) -> None:
    generate_random_bytes_response = generate_random_bytes(project_id, location_id, 256)
    assert len(generate_random_bytes_response.data) == 256


def test_get_key_labels(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    key = get_key_labels(project_id, location_id, key_ring_id, symmetric_key_id)
    assert key.labels == {"foo": "bar", "zip": "zap"}


def test_get_key_version_attestation(
    project_id: str, location_id: str, key_ring_id: str, hsm_key_id: str
) -> None:
    attestation = get_key_version_attestation(
        project_id, location_id, key_ring_id, hsm_key_id, "1"
    )
    assert attestation.format
    assert attestation.content


def test_get_public_key(
    project_id: str, location_id: str, key_ring_id: str, asymmetric_decrypt_key_id: str
) -> None:
    public_key = get_public_key(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, "1"
    )
    assert public_key.pem


def test_get_public_key_jwk(
    project_id: str, location_id: str, key_ring_id: str, asymmetric_decrypt_key_id: str
) -> None:
    public_key = get_public_key_jwk(
        project_id, location_id, key_ring_id, asymmetric_decrypt_key_id, "1"
    )
    assert "kty" in public_key


def test_iam_add_member(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    member = "group:test@google.com"
    policy = iam_add_member(
        project_id, location_id, key_ring_id, symmetric_key_id, member
    )
    assert any(member in b.members for b in policy.bindings)


def test_iam_get_policy(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    policy = iam_get_policy(project_id, location_id, key_ring_id, symmetric_key_id)
    assert policy


def test_iam_remove_member(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_sign_rsa_key_id: str,
) -> None:
    resource_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, asymmetric_sign_rsa_key_id
    )

    policy = client.get_iam_policy(request={"resource": resource_name})
    policy.bindings.add(
        role="roles/cloudkms.cryptoKeyEncrypterDecrypter",
        members=["group:test@google.com", "group:tester@google.com"],
    )
    client.set_iam_policy(request={"resource": resource_name, "policy": policy})

    policy = iam_remove_member(
        project_id,
        location_id,
        key_ring_id,
        asymmetric_sign_rsa_key_id,
        "group:test@google.com",
    )
    assert not any("group:test@google.com" in b.members for b in policy.bindings)
    assert any("group:tester@google.com" in b.members for b in policy.bindings)


def test_import_manually_wrapped_key(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    import_job_id: str,
    import_tests_key_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
    import_manually_wrapped_key(
        project_id, location_id, key_ring_id, import_tests_key_id, import_job_id
    )
    out, _ = capsys.readouterr()
    assert "Imported" in out


def test_sign_asymmetric(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_sign_rsa_key_id: str,
) -> None:
    message = "my message"

    sign_response = sign_asymmetric(
        project_id, location_id, key_ring_id, asymmetric_sign_rsa_key_id, "1", message
    )
    assert sign_response.signature

    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, asymmetric_sign_rsa_key_id, "1"
    )
    public_key = client.get_public_key(request={"name": key_version_name})
    pem = public_key.pem.encode("utf-8")
    rsa_key = serialization.load_pem_public_key(pem, default_backend())
    hash_ = hashlib.sha256(message.encode("utf-8")).digest()

    try:
        sha256 = hashes.SHA256()
        pad = padding.PKCS1v15()
        rsa_key.verify(sign_response.signature, hash_, pad, utils.Prehashed(sha256))
    except InvalidSignature:
        pytest.fail("invalid signature")


def test_sign_mac(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    hmac_key_id: str,
) -> None:
    data = "my data"

    sign_response = sign_mac(
        project_id, location_id, key_ring_id, hmac_key_id, "1", data
    )
    assert sign_response.mac

    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, hmac_key_id, "1"
    )
    verify_response = client.mac_verify(
        request={
            "name": key_version_name,
            "data": data.encode("utf-8"),
            "mac": sign_response.mac,
        }
    )

    assert verify_response.success


def test_update_key_add_rotation(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    key = update_key_add_rotation(
        project_id, location_id, key_ring_id, symmetric_key_id
    )
    assert key.rotation_period == datetime.timedelta(seconds=60 * 60 * 24 * 30)
    assert key.next_rotation_time


def test_update_key_remove_labels(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    key = update_key_remove_labels(
        project_id, location_id, key_ring_id, symmetric_key_id
    )
    assert key.labels == {}


def test_update_key_remove_rotation(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    key = update_key_remove_rotation(
        project_id, location_id, key_ring_id, symmetric_key_id
    )
    assert not key.rotation_period
    assert not key.next_rotation_time


def test_update_key_set_primary(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    key = update_key_set_primary(
        project_id, location_id, key_ring_id, symmetric_key_id, "1"
    )
    assert "1" in key.primary.name


def test_update_key_update_labels(
    project_id: str, location_id: str, key_ring_id: str, symmetric_key_id: str
) -> None:
    key = update_key_update_labels(
        project_id, location_id, key_ring_id, symmetric_key_id
    )
    assert key.labels == {"new_label": "new_value"}


def test_verify_asymmetric_ec(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_sign_ec_key_id: str,
) -> None:
    message = "my message"

    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, asymmetric_sign_ec_key_id, "1"
    )
    hash_ = hashlib.sha256(message.encode("utf-8")).digest()
    sign_response = client.asymmetric_sign(
        request={"name": key_version_name, "digest": {"sha256": hash_}}
    )

    verified = verify_asymmetric_ec(
        project_id,
        location_id,
        key_ring_id,
        asymmetric_sign_ec_key_id,
        "1",
        message,
        sign_response.signature,
    )
    assert verified


def test_verify_asymmetric_rsa(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    asymmetric_sign_rsa_key_id: str,
) -> None:
    message = "my message"

    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, asymmetric_sign_rsa_key_id, "1"
    )
    hash_ = hashlib.sha256(message.encode("utf-8")).digest()
    sign_response = client.asymmetric_sign(
        request={"name": key_version_name, "digest": {"sha256": hash_}}
    )

    verified = verify_asymmetric_rsa(
        project_id,
        location_id,
        key_ring_id,
        asymmetric_sign_rsa_key_id,
        "1",
        message,
        sign_response.signature,
    )
    assert verified


def test_verify_mac(
    client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: str,
    hmac_key_id: str,
) -> None:
    data = "my data"

    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, hmac_key_id, "1"
    )
    sign_response = client.mac_sign(
        request={"name": key_version_name, "data": data.encode("utf-8")}
    )

    verify_response = verify_mac(
        project_id, location_id, key_ring_id, hmac_key_id, "1", data, sign_response.mac
    )
    assert verify_response.success


def test_quickstart(project_id: str, location_id: str) -> None:
    key_rings = quickstart(project_id, location_id)
    assert key_rings
