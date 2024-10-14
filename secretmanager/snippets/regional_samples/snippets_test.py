# Copyright 2024 Google LLC
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

import os
import time
from typing import Iterator, Tuple, Union
import uuid

from google.api_core import exceptions, retry
from google.cloud import secretmanager_v1
import pytest

from regional_samples import access_regional_secret_version
from regional_samples import add_regional_secret_version
from regional_samples import create_regional_secret
from regional_samples import create_regional_secret_with_labels
from regional_samples import delete_regional_secret
from regional_samples import delete_regional_secret_label
from regional_samples import delete_regional_secret_with_etag
from regional_samples import destroy_regional_secret_version
from regional_samples import destroy_regional_secret_version_with_etag
from regional_samples import disable_regional_secret_version
from regional_samples import disable_regional_secret_version_with_etag
from regional_samples import edit_regional_secret_label
from regional_samples import enable_regional_secret_version
from regional_samples import enable_regional_secret_version_with_etag
from regional_samples import get_regional_secret
from regional_samples import get_regional_secret_version
from regional_samples import iam_grant_access_with_regional_secret
from regional_samples import iam_revoke_access_with_regional_secret
from regional_samples import list_regional_secret_versions
from regional_samples import list_regional_secret_versions_with_filter
from regional_samples import list_regional_secrets
from regional_samples import list_regional_secrets_with_filter
from regional_samples import regional_quickstart
from regional_samples import update_regional_secret
from regional_samples import update_regional_secret_with_etag
from regional_samples import view_regional_secret_labels


@pytest.fixture()
def location_id() -> str:
    return "us-east5"


@pytest.fixture()
def label_key() -> str:
    return "googlecloud"


@pytest.fixture()
def label_value() -> str:
    return "rocks"


@pytest.fixture()
def regional_client(location_id: str) -> secretmanager_v1.SecretManagerServiceClient:
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"
    return secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint}
    )


@pytest.fixture()
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def iam_user() -> str:
    return "serviceAccount:" + os.environ["GCLOUD_SECRETS_SERVICE_ACCOUNT"]


@pytest.fixture()
def ttl() -> str:
    return "300s"


@retry.Retry()
def retry_client_create_regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    request: Union[secretmanager_v1.CreateSecretRequest, dict],
) -> secretmanager_v1.Secret:
    # Retry to avoid 503 error & flaky issues
    return regional_client.create_secret(request=request)


@retry.Retry()
def retry_client_delete_regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    request: Union[secretmanager_v1.DeleteSecretRequest, dict],
) -> None:
    # Retry to avoid 503 error & flaky issues
    return regional_client.delete_secret(request=request)


@retry.Retry()
def retry_client_access_regional_secret_version(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    request: Union[secretmanager_v1.AccessSecretVersionRequest, dict],
) -> secretmanager_v1.AccessSecretVersionResponse:
    # Retry to avoid 503 error & flaky issues
    return regional_client.access_secret_version(request=request)


@pytest.fixture()
def secret_id(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
) -> Iterator[str]:
    secret_id = f"python-secret-{uuid.uuid4()}"

    yield secret_id
    secret_path = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"
    print(f"deleting secret {secret_id}")
    try:
        time.sleep(5)
        retry_client_delete_regional_secret(
            regional_client, request={"name": secret_path}
        )
    except exceptions.NotFound:
        # Secret was already deleted, probably in the test
        print(f"Secret {secret_id} was not found.")


@pytest.fixture()
def regional_secret_version(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> Iterator[Tuple[str, str, str]]:
    secret_id, _ = regional_secret

    print(f"adding secret version to {secret_id}")
    parent = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"
    time.sleep(5)
    version = regional_client.add_secret_version(
        request={"parent": parent, "payload": {"data": b"hello world!"}}
    )

    yield secret_id, version.name.rsplit("/", 1)[-1], version.etag


another_regional_secret_version = regional_secret_version


@pytest.fixture()
def regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
    secret_id: str,
    label_key: str,
    label_value: str,
    ttl: str,
) -> Iterator[Tuple[str, str]]:
    print(f"creating secret {secret_id}")

    parent = f"projects/{project_id}/locations/{location_id}"
    time.sleep(5)
    regional_secret = retry_client_create_regional_secret(
        regional_client,
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "ttl": ttl,
                "labels": {label_key: label_value},
            },
        },
    )

    yield secret_id, regional_secret.etag


def test_regional_quickstart(project_id: str, location_id: str, secret_id: str) -> None:
    regional_quickstart.regional_quickstart(project_id, location_id, secret_id)


def test_access_regional_secret_version(
    regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, _ = regional_secret_version
    version = access_regional_secret_version.access_regional_secret_version(
        project_id, location_id, secret_id, version_id
    )
    assert version.payload.data == b"hello world!"


def test_add_regional_secret_version(
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, _ = regional_secret
    version = add_regional_secret_version.add_regional_secret_version(
        project_id, location_id, secret_id, "test123"
    )
    assert secret_id in version.name


def test_create_regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
    secret_id: str,
    ttl: str,
) -> None:
    secret = create_regional_secret.create_regional_secret(
        project_id, location_id, secret_id, ttl
    )
    assert secret_id in secret.name


def test_create_regional_secret_with_label(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
    secret_id: str,
    label_key: str,
    label_value: str,
    ttl: str,
) -> None:
    labels = {label_key: label_value}
    secret = create_regional_secret_with_labels.create_regional_secret_with_labels(
        project_id, location_id, secret_id, labels, ttl
    )
    assert secret_id in secret.name


def test_delete_regional_secret_labels(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
    regional_secret: Tuple[str, str],
    label_key: str,
) -> None:
    secret_id, _ = regional_secret
    delete_regional_secret_label.delete_regional_secret_label(
        project_id, location_id, secret_id, label_key
    )
    with pytest.raises(exceptions.NotFound):
        name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}/versions/latest"
        retry_client_access_regional_secret_version(
            regional_client, request={"name": name}
        )


def test_delete_regional_secret_with_etag(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, etag = regional_secret
    delete_regional_secret_with_etag.delete_regional_secret_with_etag(
        project_id, location_id, secret_id, etag
    )
    with pytest.raises(exceptions.NotFound):
        name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}/versions/latest"
        retry_client_access_regional_secret_version(
            regional_client, request={"name": name}
        )


def test_destroy_regional_secret_version(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, _ = regional_secret_version
    version = destroy_regional_secret_version.destroy_regional_secret_version(
        project_id, location_id, secret_id, version_id
    )
    assert version.destroy_time


def test_destroy_regional_secret_version_with_etag(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, etag = regional_secret_version
    version = destroy_regional_secret_version_with_etag.destroy_regional_secret_version_with_etag(
        project_id, location_id, secret_id, version_id, etag
    )
    assert version.destroy_time


def test_enable_disable_regional_secret_version(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, _ = regional_secret_version
    version = disable_regional_secret_version.disable_regional_secret_version(
        project_id, location_id, secret_id, version_id
    )
    assert version.state == secretmanager_v1.SecretVersion.State.DISABLED

    version = enable_regional_secret_version.enable_regional_secret_version(
        project_id, location_id, secret_id, version_id
    )
    assert version.state == secretmanager_v1.SecretVersion.State.ENABLED


def test_enable_disable_regional_secret_version_with_etag(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, etag = regional_secret_version
    version = disable_regional_secret_version_with_etag.disable_regional_secret_version_with_etag(
        project_id, location_id, secret_id, version_id, etag
    )
    assert version.state == secretmanager_v1.SecretVersion.State.DISABLED

    version = enable_regional_secret_version_with_etag.enable_regional_secret_version_with_etag(
        project_id, location_id, secret_id, version_id, version.etag
    )
    assert version.state == secretmanager_v1.SecretVersion.State.ENABLED


def test_get_regional_secret_version(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, _ = regional_secret_version
    version = get_regional_secret_version.get_regional_secret_version(
        project_id, location_id, secret_id, version_id
    )
    assert secret_id in version.name
    assert version_id in version.name


def test_iam_grant_access_with_regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
    iam_user: str,
) -> None:
    secret_id, _ = regional_secret
    policy = (
        iam_grant_access_with_regional_secret.iam_grant_access_with_regional_secret(
            project_id, location_id, secret_id, iam_user
        )
    )
    assert any(iam_user in b.members for b in policy.bindings)


def test_iam_revoke_access_with_regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
    iam_user: str,
) -> None:
    secret_id, _ = regional_secret
    policy = (
        iam_revoke_access_with_regional_secret.iam_revoke_access_with_regional_secret(
            project_id, location_id, secret_id, iam_user
        )
    )
    assert all(iam_user not in b.members for b in policy.bindings)


def test_list_regional_secret_versions(
    capsys: pytest.LogCaptureFixture,
    regional_secret_version: Tuple[str, str, str],
    another_regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, _ = regional_secret_version
    version_1 = get_regional_secret_version.get_regional_secret_version(
        project_id, location_id, secret_id, version_id
    )
    _, another_version_id, _ = another_regional_secret_version
    version_2 = get_regional_secret_version.get_regional_secret_version(
        project_id, location_id, secret_id, another_version_id
    )
    list_regional_secret_versions.list_regional_secret_versions(
        project_id, location_id, secret_id
    )

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert f"Found secret version: {version_1.name}" in out
    assert f"Found secret version: {version_2.name}" in out


def test_list_regional_secret_versions_with_filter(
    capsys: pytest.LogCaptureFixture,
    regional_secret_version: Tuple[str, str, str],
    another_regional_secret_version: Tuple[str, str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, version_id, _ = regional_secret_version
    enabled = get_regional_secret_version.get_regional_secret_version(
        project_id, location_id, secret_id, version_id
    )
    _, another_version_id, _ = another_regional_secret_version
    disabled = disable_regional_secret_version.disable_regional_secret_version(
        project_id, location_id, secret_id, another_version_id
    )
    assert disabled.state == secretmanager_v1.SecretVersion.State.DISABLED
    list_regional_secret_versions_with_filter.list_regional_secret_versions_with_filter(
        project_id, location_id, secret_id, "state:ENABLED"
    )

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert f"Found secret version: {enabled.name}" in out
    assert f"Found secret version: {disabled.name}" not in out


def test_list_regional_secrets(
    capsys: pytest.LogCaptureFixture,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, _ = regional_secret
    got_regional_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    list_regional_secrets.list_regional_secrets(project_id, location_id)

    out, _ = capsys.readouterr()
    assert f"Found secret: {got_regional_secret.name}" in out


def test_list_regional_secrets_with_filter(
    capsys: pytest.LogCaptureFixture,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, _ = regional_secret
    unlabeled = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    list_regional_secrets_with_filter.list_regional_secrets_with_filter(
        project_id, location_id, "labels.secretmanager:rocks"
    )

    out, _ = capsys.readouterr()
    assert f"Found secret: {unlabeled.name}" not in out

    labeled = update_regional_secret.update_regional_secret(
        project_id, location_id, secret_id
    )
    assert labeled.labels["secretmanager"] == "rocks"
    list_regional_secrets_with_filter.list_regional_secrets_with_filter(
        project_id, location_id, "labels.secretmanager:rocks"
    )

    out, _ = capsys.readouterr()
    assert f"Found secret: {labeled.name}" in out


def test_delete_regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, _ = regional_secret
    delete_regional_secret.delete_regional_secret(project_id, location_id, secret_id)
    with pytest.raises(exceptions.NotFound):
        print(f"{regional_client}")
        name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}/versions/latest"
        retry_client_access_regional_secret_version(
            regional_client, request={"name": name}
        )


def test_get_regional_secret(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, _ = regional_secret
    snippet_regional_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    assert secret_id in snippet_regional_secret.name


def test_edit_regional_secret_label(
    project_id: str, location_id: str, regional_secret: Tuple[str, str], label_key: str
) -> None:
    secret_id, _ = regional_secret
    updated_label_value = "updatedvalue"
    labels = {label_key: updated_label_value}
    updated_secret = edit_regional_secret_label.edit_regional_secret_label(
        project_id, location_id, secret_id, labels
    )
    assert updated_secret.labels[label_key] == updated_label_value


def test_update_regional_secret_with_etag(
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, etag = regional_secret
    updated_regional_secret = (
        update_regional_secret_with_etag.update_regional_secret_with_etag(
            project_id, location_id, secret_id, etag
        )
    )
    assert updated_regional_secret.labels["secretmanager"] == "rocks"


def test_update_regional_secret(
    regional_secret: Tuple[str, str],
    project_id: str,
    location_id: str,
) -> None:
    secret_id, _ = regional_secret
    updated_regional_secret = update_regional_secret.update_regional_secret(
        project_id, location_id, secret_id
    )
    assert updated_regional_secret.labels["secretmanager"] == "rocks"


def test_view_regional_secret_labels(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    location_id: str,
    regional_secret: Tuple[str, str],
    label_key: str,
) -> None:
    secret_id, _ = regional_secret
    view_regional_secret_labels.view_regional_secret_labels(
        project_id, location_id, secret_id
    )

    out, _ = capsys.readouterr()
    assert label_key in out
