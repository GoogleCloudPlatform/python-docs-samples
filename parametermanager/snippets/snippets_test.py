# Copyright 2025 Google LLC
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
import json
import os
import time
from typing import Iterator, Optional, Tuple, Union
import uuid

from google.api_core import exceptions, retry
from google.cloud import kms, parametermanager_v1, secretmanager
import pytest

# Import the methods to be tested
from create_param import create_param
from create_param_version import create_param_version
from create_param_version_with_secret import create_param_version_with_secret
from create_param_with_kms_key import create_param_with_kms_key
from create_structured_param import create_structured_param
from create_structured_param_version import create_structured_param_version
from delete_param import delete_param
from delete_param_version import delete_param_version
from disable_param_version import disable_param_version
from enable_param_version import enable_param_version
from get_param import get_param
from get_param_version import get_param_version
from list_param_versions import list_param_versions
from list_params import list_params
from quickstart import quickstart
from remove_param_kms_key import remove_param_kms_key
from render_param_version import render_param_version
from update_param_kms_key import update_param_kms_key


@pytest.fixture()
def client() -> parametermanager_v1.ParameterManagerClient:
    return parametermanager_v1.ParameterManagerClient()


@pytest.fixture()
def secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


@pytest.fixture()
def kms_key_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()


@pytest.fixture()
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def location_id() -> str:
    return "global"


@pytest.fixture()
def label_key() -> str:
    return "googlecloud"


@pytest.fixture()
def label_value() -> str:
    return "rocks"


@retry.Retry()
def retry_client_delete_param(
    client: parametermanager_v1.ParameterManagerClient,
    request: Optional[Union[parametermanager_v1.DeleteParameterRequest, dict]],
) -> None:
    # Retry to avoid 503 error & flaky issues
    return client.delete_parameter(request=request)


@retry.Retry()
def retry_client_delete_param_version(
    client: parametermanager_v1.ParameterManagerClient,
    request: Optional[Union[parametermanager_v1.DeleteParameterVersionRequest, dict]],
) -> None:
    # Retry to avoid 503 error & flaky issues
    return client.delete_parameter_version(request=request)


@retry.Retry()
def retry_client_list_param_version(
    client: parametermanager_v1.ParameterManagerClient,
    request: Optional[Union[parametermanager_v1.ListParameterVersionsRequest, dict]],
) -> parametermanager_v1.services.parameter_manager.pagers.ListParameterVersionsPager:
    # Retry to avoid 503 error & flaky issues
    return client.list_parameter_versions(request=request)


@retry.Retry()
def retry_client_create_parameter(
    client: parametermanager_v1.ParameterManagerClient,
    request: Optional[Union[parametermanager_v1.CreateParameterRequest, dict]],
) -> parametermanager_v1.Parameter:
    # Retry to avoid 503 error & flaky issues
    return client.create_parameter(request=request)


@retry.Retry()
def retry_client_get_parameter_version(
    client: parametermanager_v1.ParameterManagerClient,
    request: Optional[Union[parametermanager_v1.GetParameterVersionRequest, dict]],
) -> parametermanager_v1.ParameterVersion:
    # Retry to avoid 503 error & flaky issues
    return client.get_parameter_version(request=request)


@retry.Retry()
def retry_client_create_secret(
    secret_manager_client: secretmanager.SecretManagerServiceClient,
    request: Optional[Union[secretmanager.CreateSecretRequest, dict]],
) -> secretmanager.Secret:
    # Retry to avoid 503 error & flaky issues
    return secret_manager_client.create_secret(request=request)


@retry.Retry()
def retry_client_delete_secret(
    secret_manager_client: secretmanager.SecretManagerServiceClient,
    request: Optional[Union[secretmanager.DeleteSecretRequest, dict]],
) -> None:
    # Retry to avoid 503 error & flaky issues
    return secret_manager_client.delete_secret(request=request)


@retry.Retry()
def retry_client_destroy_crypto_key(
    kms_key_client: kms.KeyManagementServiceClient,
    request: Optional[Union[kms.DestroyCryptoKeyVersionRequest, dict]],
) -> None:
    # Retry to avoid 503 error & flaky issues
    return kms_key_client.destroy_crypto_key_version(request=request)


@pytest.fixture()
def parameter(
    client: parametermanager_v1.ParameterManagerClient,
    project_id: str,
    parameter_id: str,
) -> Iterator[Tuple[str, str, str]]:
    param_id, version_id = parameter_id
    print(f"Creating parameter {param_id}")

    parent = client.common_location_path(project_id, "global")
    time.sleep(5)
    _ = retry_client_create_parameter(
        client,
        request={
            "parent": parent,
            "parameter_id": param_id,
        },
    )

    yield project_id, param_id, version_id


@pytest.fixture()
def structured_parameter(
    client: parametermanager_v1.ParameterManagerClient,
    project_id: str,
    parameter_id: str,
) -> Iterator[Tuple[str, str, str, parametermanager_v1.Parameter]]:
    param_id, version_id = parameter_id
    print(f"Creating parameter {param_id}")

    parent = client.common_location_path(project_id, "global")
    time.sleep(5)
    parameter = retry_client_create_parameter(
        client,
        request={
            "parent": parent,
            "parameter_id": param_id,
            "parameter": {"format": parametermanager_v1.ParameterFormat.JSON.name},
        },
    )

    yield project_id, param_id, version_id, parameter.policy_member


@pytest.fixture()
def parameter_with_kms(
    client: parametermanager_v1.ParameterManagerClient,
    project_id: str,
    parameter_id: str,
    hsm_key_id: str,
) -> Iterator[Tuple[str, str, str, parametermanager_v1.Parameter]]:
    param_id, version_id = parameter_id
    print(f"Creating parameter {param_id} with kms {hsm_key_id}")

    parent = client.common_location_path(project_id, "global")
    time.sleep(5)
    parameter = retry_client_create_parameter(
        client,
        request={
            "parent": parent,
            "parameter_id": param_id,
            "parameter": {"kms_key": hsm_key_id},
        },
    )

    yield project_id, param_id, version_id, parameter.kms_key


@pytest.fixture()
def parameter_version(
    client: parametermanager_v1.ParameterManagerClient, parameter: Tuple[str, str, str]
) -> Iterator[Tuple[str, str, str, str]]:
    project_id, param_id, version_id = parameter

    print(f"Adding secret version to {param_id}")
    parent = client.parameter_path(project_id, "global", param_id)
    payload = b"hello world!"
    time.sleep(5)
    _ = client.create_parameter_version(
        request={
            "parent": parent,
            "parameter_version_id": version_id,
            "parameter_version": {"payload": {"data": payload}},
        }
    )

    yield project_id, param_id, version_id, payload


@pytest.fixture()
def parameter_version_with_secret(
    secret_manager_client: secretmanager.SecretManagerServiceClient,
    client: parametermanager_v1.ParameterManagerClient,
    structured_parameter: Tuple[str, str, str, parametermanager_v1.Parameter],
    secret_version: Tuple[str, str, str, str],
) -> Iterator[Tuple[str, str, str, dict]]:
    project_id, param_id, version_id, member = structured_parameter
    project_id, secret_id, version_id, secret_parent = secret_version

    print(f"Adding parameter version to {param_id}")
    parent = client.parameter_path(project_id, "global", param_id)
    payload = {
        "username": "temp-user",
        "password": f"__REF__('//secretmanager.googleapis.com/{secret_id}')",
    }
    payload_str = json.dumps(payload)

    time.sleep(5)
    _ = client.create_parameter_version(
        request={
            "parent": parent,
            "parameter_version_id": version_id,
            "parameter_version": {"payload": {"data": payload_str.encode("utf-8")}},
        }
    )

    policy = secret_manager_client.get_iam_policy(request={"resource": secret_parent})
    policy.bindings.add(
        role="roles/secretmanager.secretAccessor",
        members=[member.iam_policy_uid_principal],
    )
    secret_manager_client.set_iam_policy(
        request={"resource": secret_parent, "policy": policy}
    )

    yield project_id, param_id, version_id, payload


@pytest.fixture()
def parameter_id(
    client: parametermanager_v1.ParameterManagerClient, project_id: str
) -> Iterator[str]:
    param_id = f"python-param-{uuid.uuid4()}"
    param_version_id = f"python-param-version-{uuid.uuid4()}"

    yield param_id, param_version_id
    param_path = client.parameter_path(project_id, "global", param_id)
    print(f"Deleting parameter {param_id}")
    try:
        time.sleep(5)
        list_versions = retry_client_list_param_version(
            client, request={"parent": param_path}
        )
        for version in list_versions:
            print(f"Deleting version {version}")
            retry_client_delete_param_version(client, request={"name": version.name})
        retry_client_delete_param(client, request={"name": param_path})
    except exceptions.NotFound:
        # Parameter was already deleted, probably in the test
        print(f"Parameter {param_id} was not found.")


@pytest.fixture()
def secret_id(
    secret_manager_client: secretmanager.SecretManagerServiceClient, project_id: str
) -> Iterator[str]:
    secret_id = f"python-secret-{uuid.uuid4()}"

    yield secret_id
    secret_path = secret_manager_client.secret_path(project_id, secret_id)
    print(f"Deleting secret {secret_id}")
    try:
        time.sleep(5)
        retry_client_delete_secret(secret_manager_client, request={"name": secret_path})
    except exceptions.NotFound:
        # Secret was already deleted, probably in the test
        print(f"Secret {secret_id} was not found.")


@pytest.fixture()
def secret(
    secret_manager_client: secretmanager.SecretManagerServiceClient,
    project_id: str,
    secret_id: str,
    label_key: str,
    label_value: str,
) -> Iterator[Tuple[str, str, str, str]]:
    print(f"Creating secret {secret_id}")

    parent = secret_manager_client.common_project_path(project_id)
    time.sleep(5)
    secret = retry_client_create_secret(
        secret_manager_client,
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {"automatic": {}},
                "labels": {label_key: label_value},
            },
        },
    )

    yield project_id, secret_id, secret.etag


@pytest.fixture()
def secret_version(
    secret_manager_client: secretmanager.SecretManagerServiceClient,
    secret: Tuple[str, str, str],
) -> Iterator[Tuple[str, str, str, str]]:
    project_id, secret_id, _ = secret

    print(f"Adding secret version to {secret_id}")
    parent = secret_manager_client.secret_path(project_id, secret_id)
    payload = b"hello world!"
    time.sleep(5)
    version = secret_manager_client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload}}
    )

    yield project_id, version.name, version.name.rsplit("/", 1)[-1], parent


@pytest.fixture()
def key_ring_id(
    kms_key_client: kms.KeyManagementServiceClient, project_id: str, location_id: str
) -> Tuple[str, str]:
    location_name = f"projects/{project_id}/locations/{location_id}"
    key_ring_id = "test-pm-snippets"
    key_id = f"{uuid.uuid4()}"
    try:
        key_ring = kms_key_client.create_key_ring(
            request={
                "parent": location_name,
                "key_ring_id": key_ring_id,
                "key_ring": {},
            }
        )
        yield key_ring.name, key_id
    except exceptions.AlreadyExists:
        yield f"{location_name}/keyRings/{key_ring_id}", key_id
    except Exception:
        pytest.fail("unable to create the keyring")


@pytest.fixture()
def hsm_key_id(
    kms_key_client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: Tuple[str, str],
) -> str:
    parent, key_id = key_ring_id
    key = kms_key_client.create_crypto_key(
        request={
            "parent": parent,
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
    wait_for_ready(kms_key_client, f"{key.name}/cryptoKeyVersions/1")
    yield key.name
    print(f"Destroying the key version {key.name}")
    try:
        time.sleep(5)
        for key_version in kms_key_client.list_crypto_key_versions(
            request={"parent": key.name}
        ):
            if key_version.state == key_version.state.ENABLED:
                retry_client_destroy_crypto_key(
                    kms_key_client, request={"name": key_version.name}
                )
    except exceptions.NotFound:
        # KMS key was already deleted, probably in the test
        print(f"KMS Key {key.name} was not found.")


@pytest.fixture()
def updated_hsm_key_id(
    kms_key_client: kms.KeyManagementServiceClient,
    project_id: str,
    location_id: str,
    key_ring_id: Tuple[str, str],
) -> str:
    parent, _ = key_ring_id
    key_id = f"{uuid.uuid4()}"
    key = kms_key_client.create_crypto_key(
        request={
            "parent": parent,
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
    wait_for_ready(kms_key_client, f"{key.name}/cryptoKeyVersions/1")
    yield key.name
    print(f"Destroying the key version {key.name}")
    try:
        time.sleep(5)
        for key_version in kms_key_client.list_crypto_key_versions(
            request={"parent": key.name}
        ):
            if key_version.state == key_version.state.ENABLED:
                retry_client_destroy_crypto_key(
                    kms_key_client, request={"name": key_version.name}
                )
    except exceptions.NotFound:
        # KMS key was already deleted, probably in the test
        print(f"KMS Key {key.name} was not found.")


def test_quickstart(project_id: str, parameter_id: Tuple[str, str]) -> None:
    param_id, version_id = parameter_id
    quickstart(project_id, param_id, version_id)


def test_create_param(
    project_id: str,
    parameter_id: str,
) -> None:
    param_id, _ = parameter_id
    parameter = create_param(project_id, param_id)
    assert param_id in parameter.name


def test_create_param_with_kms_key(
    project_id: str, parameter_id: str, hsm_key_id: str
) -> None:
    param_id, _ = parameter_id
    parameter = create_param_with_kms_key(project_id, param_id, hsm_key_id)
    assert param_id in parameter.name
    assert hsm_key_id == parameter.kms_key


def test_update_param_kms_key(
    project_id: str,
    parameter_with_kms: Tuple[str, str, str, str],
    updated_hsm_key_id: str,
) -> None:
    project_id, param_id, _, kms_key = parameter_with_kms
    parameter = update_param_kms_key(project_id, param_id, updated_hsm_key_id)
    assert param_id in parameter.name
    assert updated_hsm_key_id == parameter.kms_key
    assert kms_key != parameter.kms_key


def test_remove_param_kms_key(
    project_id: str, parameter_with_kms: Tuple[str, str, str, str], hsm_key_id: str
) -> None:
    project_id, param_id, _, kms_key = parameter_with_kms
    parameter = remove_param_kms_key(project_id, param_id)
    assert param_id in parameter.name
    assert parameter.kms_key == ""


def test_create_param_version(parameter: Tuple[str, str, str]) -> None:
    project_id, param_id, version_id = parameter
    payload = "test123"
    version = create_param_version(project_id, param_id, version_id, payload)
    assert param_id in version.name
    assert version_id in version.name


def test_create_param_version_with_secret(
    secret_version: Tuple[str, str, str, str],
    structured_parameter: Tuple[str, str, str, parametermanager_v1.Parameter],
) -> None:
    project_id, secret_id, version_id, _ = secret_version
    project_id, param_id, version_id, _ = structured_parameter
    version = create_param_version_with_secret(
        project_id, param_id, version_id, secret_id
    )
    assert param_id in version.name
    assert version_id in version.name


def test_create_structured_param(
    project_id: str,
    parameter_id: str,
) -> None:
    param_id, _ = parameter_id
    parameter = create_structured_param(
        project_id, param_id, parametermanager_v1.ParameterFormat.JSON
    )
    assert param_id in parameter.name


def test_create_structured_param_version(parameter: Tuple[str, str, str]) -> None:
    project_id, param_id, version_id = parameter
    payload = {"test-key": "test-value"}
    version = create_structured_param_version(project_id, param_id, version_id, payload)
    assert param_id in version.name
    assert version_id in version.name


def test_delete_parameter(
    client: parametermanager_v1.ParameterManagerClient, parameter: Tuple[str, str, str]
) -> None:
    project_id, param_id, version_id = parameter
    delete_param(project_id, param_id)
    with pytest.raises(exceptions.NotFound):
        print(f"{client}")
        name = client.parameter_version_path(project_id, "global", param_id, version_id)
        retry_client_get_parameter_version(client, request={"name": name})


def test_delete_param_version(
    client: parametermanager_v1.ParameterManagerClient,
    parameter_version: Tuple[str, str, str, str],
) -> None:
    project_id, param_id, version_id, _ = parameter_version
    delete_param_version(project_id, param_id, version_id)
    with pytest.raises(exceptions.NotFound):
        print(f"{client}")
        name = client.parameter_version_path(project_id, "global", param_id, version_id)
        retry_client_get_parameter_version(client, request={"name": name})


def test_disable_param_version(
    parameter_version: Tuple[str, str, str, str],
) -> None:
    project_id, param_id, version_id, _ = parameter_version
    version = disable_param_version(project_id, param_id, version_id)
    assert version.disabled is True


def test_enable_param_version(
    parameter_version: Tuple[str, str, str, str],
) -> None:
    project_id, param_id, version_id, _ = parameter_version
    version = enable_param_version(project_id, param_id, version_id)
    assert version.disabled is False


def test_get_param(parameter: Tuple[str, str, str]) -> None:
    project_id, param_id, _ = parameter
    snippet_param = get_param(project_id, param_id)
    assert param_id in snippet_param.name


def test_get_param_version(
    parameter_version: Tuple[str, str, str, str],
) -> None:
    project_id, param_id, version_id, payload = parameter_version
    version = get_param_version(project_id, param_id, version_id)
    assert param_id in version.name
    assert version_id in version.name
    assert version.payload.data == payload


def test_list_params(
    capsys: pytest.LogCaptureFixture, parameter: Tuple[str, str, str]
) -> None:
    project_id, param_id, _ = parameter
    got_param = get_param(project_id, param_id)
    list_params(project_id)

    out, _ = capsys.readouterr()
    assert (
        f"Found parameter {got_param.name} with format {got_param.format_.name}" in out
    )


def test_list_param_versions(
    capsys: pytest.LogCaptureFixture,
    parameter_version: Tuple[str, str, str, str],
) -> None:
    project_id, param_id, version_id, _ = parameter_version
    version_1 = get_param_version(project_id, param_id, version_id)
    list_param_versions(project_id, param_id)

    out, _ = capsys.readouterr()
    assert param_id in out
    assert f"Found parameter version: {version_1.name}" in out


def test_render_param_version(
    parameter_version_with_secret: Tuple[str, str, str, dict],
) -> None:
    project_id, param_id, version_id, _ = parameter_version_with_secret
    time.sleep(10)
    version = render_param_version(project_id, param_id, version_id)
    assert param_id in version.parameter_version
    assert version_id in version.parameter_version
    assert (
        version.rendered_payload.decode("utf-8")
        == '{"username": "temp-user", "password": "hello world!"}'
    )


def wait_for_ready(
    kms_key_client: kms.KeyManagementServiceClient, key_version_name: str
) -> None:
    for i in range(4):
        key_version = kms_key_client.get_crypto_key_version(
            request={"name": key_version_name}
        )
        if key_version.state == kms.CryptoKeyVersion.CryptoKeyVersionState.ENABLED:
            return
        time.sleep((i + 1) ** 2)
    pytest.fail(f"{key_version_name} not ready")
