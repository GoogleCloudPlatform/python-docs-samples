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

from datetime import datetime, timedelta, timezone
import os
import time
from typing import Iterator, Tuple, Union
import uuid

from google.api_core import exceptions, retry
from google.cloud import resourcemanager_v3
from google.cloud import secretmanager_v1
from google.protobuf.duration_pb2 import Duration
import pytest

from regional_samples import access_regional_secret_version
from regional_samples import add_regional_secret_version
from regional_samples import bind_tags_to_regional_secret
from regional_samples import create_regional_secret
from regional_samples import create_regional_secret_with_annotations
from regional_samples import create_regional_secret_with_cmek
from regional_samples import create_regional_secret_with_delayed_destroy
from regional_samples import create_regional_secret_with_expire_time
from regional_samples import create_regional_secret_with_labels
from regional_samples import create_regional_secret_with_rotation
from regional_samples import create_regional_secret_with_tags
from regional_samples import create_regional_secret_with_topic
from regional_samples import delete_regional_secret
from regional_samples import delete_regional_secret_annotation
from regional_samples import delete_regional_secret_expiration
from regional_samples import delete_regional_secret_label
from regional_samples import delete_regional_secret_rotation
from regional_samples import delete_regional_secret_with_etag
from regional_samples import destroy_regional_secret_version
from regional_samples import destroy_regional_secret_version_with_etag
from regional_samples import detach_regional_tag
from regional_samples import disable_regional_secret_delayed_destroy
from regional_samples import disable_regional_secret_version
from regional_samples import disable_regional_secret_version_with_etag
from regional_samples import edit_regional_secret_annotations
from regional_samples import edit_regional_secret_label
from regional_samples import enable_regional_secret_version
from regional_samples import enable_regional_secret_version_with_etag
from regional_samples import get_regional_secret
from regional_samples import get_regional_secret_version
from regional_samples import iam_grant_access_with_regional_secret
from regional_samples import iam_revoke_access_with_regional_secret
from regional_samples import list_regional_secret_tag_bindings
from regional_samples import list_regional_secret_versions
from regional_samples import list_regional_secret_versions_with_filter
from regional_samples import list_regional_secrets
from regional_samples import list_regional_secrets_with_filter
from regional_samples import regional_quickstart
from regional_samples import update_regional_secret
from regional_samples import update_regional_secret_expiration
from regional_samples import update_regional_secret_rotation
from regional_samples import update_regional_secret_with_alias
from regional_samples import update_regional_secret_with_delayed_destroy
from regional_samples import update_regional_secret_with_etag
from regional_samples import view_regional_secret_annotations
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
def tag_keys_client() -> resourcemanager_v3.TagKeysClient:
    return resourcemanager_v3.TagKeysClient()


@pytest.fixture()
def tag_values_client() -> resourcemanager_v3.TagValuesClient:
    return resourcemanager_v3.TagValuesClient()


@pytest.fixture()
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def iam_user() -> str:
    return "serviceAccount:" + os.environ["GCLOUD_SECRETS_SERVICE_ACCOUNT"]


@pytest.fixture()
def topic_name() -> str:
    return os.environ["GOOGLE_CLOUD_TOPIC_NAME"]


@pytest.fixture()
def kms_key_name() -> str:
    return os.environ["GOOGLE_CLOUD_REGIONAL_KMS_KEY_NAME"]


@pytest.fixture()
def rotation_period_hours() -> int:
    return 24


@pytest.fixture()
def ttl() -> str:
    return "300s"


@pytest.fixture()
def annotation_key() -> str:
    return "annotationkey"


@pytest.fixture()
def annotation_value() -> str:
    return "annotationvalue"


@pytest.fixture()
def version_destroy_ttl() -> int:
    return 604800  # 7 days in seconds


@pytest.fixture()
def short_key_name() -> str:
    return f"python-test-key-{uuid.uuid4()}"


@pytest.fixture()
def short_value_name() -> str:
    return f"python-test-value-{uuid.uuid4()}"


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


@retry.Retry()
def retry_client_create_tag_key(
    tag_keys_client: resourcemanager_v3.TagKeysClient,
    request: Union[resourcemanager_v3.CreateTagKeyRequest, dict],
) -> str:
    # Retry to avoid 503 error & flaky issues
    operation = tag_keys_client.create_tag_key(request=request)
    response = operation.result()

    return response.name


@retry.Retry()
def retry_client_create_tag_value(
    tag_values_client: resourcemanager_v3.TagValuesClient,
    request: Union[resourcemanager_v3.CreateTagValueRequest, dict],
) -> str:
    # Retry to avoid 503 error & flaky issues
    operation = tag_values_client.create_tag_value(request=request)
    response = operation.result()

    return response.name


@retry.Retry()
def retry_client_delete_tag_value(
    tag_values_client: resourcemanager_v3.TagValuesClient,
    request: Union[resourcemanager_v3.DeleteTagValueRequest, dict],
) -> str:
    # Retry to avoid 503 error & flaky issues
    time.sleep(15)  # Added a sleep to wait for the tag unbinding
    operation = tag_values_client.delete_tag_value(request=request)
    response = operation.result()
    return response.name


@retry.Retry()
def retry_client_delete_tag_key(
    tag_keys_client: resourcemanager_v3.TagKeysClient,
    request: Union[resourcemanager_v3.DeleteTagKeyRequest, dict],
) -> str:
    # Retry to avoid 503 error & flaky issues
    operation = tag_keys_client.delete_tag_key(request=request)
    response = operation.result()
    return response.name


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
    annotation_key: str,
    annotation_value: str,
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
                "annotations": {annotation_key: annotation_value},
                "labels": {label_key: label_value},
            },
        },
    )

    yield secret_id, regional_secret.etag


@pytest.fixture()
def tag_key_and_tag_value(
    tag_keys_client: resourcemanager_v3.TagKeysClient,
    tag_values_client: resourcemanager_v3.TagValuesClient,
    project_id: str,
    short_key_name: str,
    short_value_name: str,
) -> Iterator[Tuple[str, str]]:

    tag_key = retry_client_create_tag_key(
        tag_keys_client,
        request={
            "tag_key": {
                "parent": f"projects/{project_id}",
                "short_name": short_key_name,
            }
        },
    )

    print(f"created tag key {tag_key}")

    tag_value = retry_client_create_tag_value(
        tag_values_client,
        request={
            "tag_value": {
                "parent": tag_key,
                "short_name": short_value_name,
            }
        },
    )

    print(f"created tag value {tag_value}")

    yield tag_key, tag_value

    print(f"deleting tag value {tag_value} and tag key {tag_key}")

    try:
        time.sleep(5)
        retry_client_delete_tag_value(tag_values_client, request={"name": tag_value})
        retry_client_delete_tag_key(tag_keys_client, request={"name": tag_key})
    except exceptions.NotFound:
        # Tag was already deleted, probably in the test
        print("Tag value or tag key was not found.")


@pytest.fixture()
def regional_secret_with_delayed_destroy(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
    secret_id: str,
    version_destroy_ttl: int,
) -> Iterator[str]:
    print("creating secret with given secret id.")

    parent = f"projects/{project_id}/locations/{location_id}"
    time.sleep(5)
    retry_client_create_regional_secret(
        regional_client,
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "version_destroy_ttl": Duration(seconds=version_destroy_ttl),
            },
        },
    )
    print("debug")

    yield secret_id


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


def test_create_regional_secret_with_tags(
    project_id: str,
    location_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    tag_key, tag_value = tag_key_and_tag_value
    secret = create_regional_secret_with_tags.create_regional_secret_with_tags(
        project_id, location_id, secret_id, tag_key, tag_value
    )

    assert secret_id in secret.name


def test_bind_tags_to_regional_secret(
    project_id: str,
    location_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    _, tag_value = tag_key_and_tag_value
    tag_resp = bind_tags_to_regional_secret.bind_tags_to_regional_secret(
        project_id, location_id, secret_id, tag_value
    )

    assert secret_id in tag_resp.parent
    assert tag_value in tag_resp.tag_value


def test_create_regional_secret_with_annotations(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
    secret_id: str,
    annotation_key: str,
    annotation_value: str,
) -> None:
    annotations = {annotation_key: annotation_value}
    secret = (
        create_regional_secret_with_annotations.create_regional_secret_with_annotations(
            project_id, location_id, secret_id, annotations
        )
    )
    assert secret_id in secret.name


def test_create_regional_secret_with_delayed_destroy(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    project_id: str,
    location_id: str,
    secret_id: str,
    version_destroy_ttl: int,
) -> None:
    secret = create_regional_secret_with_delayed_destroy.create_regional_secret_with_delayed_destroy(project_id, location_id, secret_id, version_destroy_ttl)
    assert secret_id in secret.name
    assert timedelta(seconds=version_destroy_ttl) == secret.version_destroy_ttl


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


def test_delete_regional_secret_annotation(
    project_id: str,
    location_id: str,
    regional_secret: Tuple[str, str],
    annotation_key: str,
) -> None:
    secret_id, _ = regional_secret
    secret = delete_regional_secret_annotation.delete_regional_secret_annotation(
        project_id, location_id, secret_id, annotation_key
    )
    assert secret_id in secret.name
    assert annotation_key not in secret.annotations


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


def test_disable_regional_secret_delayed_destroy(
    regional_client: secretmanager_v1.SecretManagerServiceClient,
    regional_secret_with_delayed_destroy: str,
    project_id: str,
    location_id: str,
) -> None:
    secret_id = regional_secret_with_delayed_destroy
    updated_secret = disable_regional_secret_delayed_destroy.disable_regional_secret_delayed_destroy(project_id, location_id, secret_id)
    assert updated_secret.version_destroy_ttl == timedelta(0)


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


def test_view_regional_secret_annotations(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    location_id: str,
    regional_secret: Tuple[str, str],
    annotation_key: str,
) -> None:
    secret_id, _ = regional_secret
    view_regional_secret_annotations.view_regional_secret_annotations(
        project_id, location_id, secret_id
    )

    out, _ = capsys.readouterr()
    assert annotation_key in out


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


def test_edit_regional_secret_annotations(
    project_id: str,
    location_id: str,
    regional_secret: Tuple[str, str],
    annotation_key: str,
) -> None:
    secret_id, _ = regional_secret
    updated_annotation_value = "updatedvalue"
    annotations = {annotation_key: updated_annotation_value}
    updated_secret = edit_regional_secret_annotations.edit_regional_secret_annotations(
        project_id, location_id, secret_id, annotations
    )
    assert updated_secret.annotations[annotation_key] == updated_annotation_value


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


def test_update_regional_secret_with_delayed_destroy(
    regional_secret_with_delayed_destroy: str,
    project_id: str,
    location_id: str,
    version_destroy_ttl: int
) -> None:
    secret_id = regional_secret_with_delayed_destroy
    updated_version_delayed_destroy = 118400
    updated_secret = update_regional_secret_with_delayed_destroy.update_regional_secret_with_delayed_destroy(project_id, location_id, secret_id, updated_version_delayed_destroy)
    assert updated_secret.version_destroy_ttl == timedelta(seconds=updated_version_delayed_destroy)


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


def test_list_regional_secret_tag_bindings(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    location_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    tag_key, tag_value = tag_key_and_tag_value
    create_regional_secret_with_tags.create_regional_secret_with_tags(
        project_id, location_id, secret_id, tag_key, tag_value
    )

    # Call the function being tested

    list_regional_secret_tag_bindings.list_regional_secret_tag_bindings(
        project_id, location_id, secret_id
    )

    # Verify the tag value is in the returned bindings

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert tag_value in out


def test_detach_regional_tag(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    location_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    tag_key, tag_value = tag_key_and_tag_value

    # Create a secret and bind the tag to it for testing detach

    create_regional_secret_with_tags.create_regional_secret_with_tags(
        project_id, location_id, secret_id, tag_key, tag_value
    )

    # Call the function being tested - detach the tag

    detach_regional_tag.detach_regional_tag(
        project_id, location_id, secret_id, tag_value
    )

    # Verify the output contains the expected message

    out, _ = capsys.readouterr()
    assert "Detached tag value" in out

    # List the tags to verify the tag was detached

    list_regional_secret_tag_bindings.list_regional_secret_tag_bindings(
        project_id, location_id, secret_id
    )

    # Verify the tag value is no longer in the returned bindings

    out, _ = capsys.readouterr()
    assert tag_value not in out


def test_create_regional_secret_with_expire_time(
    project_id: str, secret_id: str, location_id: str
) -> None:
    # Set expire time to 1 hour from now

    expire_time = datetime.now(timezone.utc) + timedelta(hours=1)
    create_regional_secret_with_expire_time.create_regional_secret_with_expire_time(
        project_id, secret_id, location_id
    )

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    # Verify the secret has an expiration time

    assert (
        retrieved_secret.expire_time is not None
    ), "ExpireTime is None, expected non-None"
    retrieved_expire_time = retrieved_secret.expire_time.astimezone(timezone.utc)
    retrieved_timestamp = int(retrieved_expire_time.timestamp())

    # Convert expected datetime to seconds

    expire_time = int(expire_time.timestamp())

    time_diff = abs(retrieved_timestamp - expire_time)
    assert time_diff <= 1, f"ExpireTime difference too large: {time_diff} seconds. "


def test_update_regional_secret_expiration(
    capsys: pytest.LogCaptureFixture, project_id: str, secret_id: str, location_id: str
) -> None:
    create_regional_secret_with_expire_time.create_regional_secret_with_expire_time(
        project_id, secret_id, location_id
    )

    # Update expire time to 2 hours

    new_expire = datetime.now(timezone.utc) + timedelta(hours=2)
    update_regional_secret_expiration.update_regional_secret_expiration(
        project_id, secret_id, location_id
    )

    # Verify output contains expected message

    out, _ = capsys.readouterr()
    assert "Updated secret" in out

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    assert (
        retrieved_secret.expire_time is not None
    ), "ExpireTime is None, expected non-None"
    retrieved_expire_time = retrieved_secret.expire_time.astimezone(timezone.utc)
    retrieved_timestamp = int(retrieved_expire_time.timestamp())

    new_expire = int(new_expire.timestamp())
    time_diff = abs(retrieved_timestamp - new_expire)
    assert time_diff <= 1, f"ExpireTime difference too large: {time_diff} seconds. "


def test_delete_regional_secret_expiration(
    capsys: pytest.LogCaptureFixture, project_id: str, secret_id: str, location_id: str
) -> None:

    create_regional_secret_with_expire_time.create_regional_secret_with_expire_time(
        project_id, secret_id, location_id
    )

    delete_regional_secret_expiration.delete_regional_secret_expiration(
        project_id, secret_id, location_id
    )
    out, _ = capsys.readouterr()
    assert "Removed expiration" in out

    # Verify expire time is removed with GetSecret

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    assert (
        retrieved_secret.expire_time is None
    ), f"ExpireTime is {retrieved_secret.expire_time}, expected None"


def test_create_regional_secret_with_rotation(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    secret_id: str,
    location_id: str,
    topic_name: str,
    rotation_period_hours: int,
) -> None:

    # Create the secret with rotation

    create_regional_secret_with_rotation.create_regional_secret_with_rotation(
        project_id, secret_id, location_id, topic_name
    )

    # Verify output contains expected message

    out, _ = capsys.readouterr()
    assert "Created secret" in out, f"Expected 'Created secret' in output, got: {out}"

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )

    # Verify rotation is configured

    assert retrieved_secret.rotation is not None, "Rotation is None, expected non-None"

    # Verify rotation period is set correctly (24 hours = 86400 seconds)

    expected_seconds = rotation_period_hours * 3600
    actual_seconds = retrieved_secret.rotation.rotation_period.total_seconds()
    assert (
        actual_seconds == expected_seconds
    ), f"RotationPeriod mismatch: got {actual_seconds}, want {expected_seconds}"

    # Verify next rotation time is set

    assert (
        retrieved_secret.rotation.next_rotation_time is not None
    ), "NextRotationTime is None, expected non-None"


def test_update_regional_secret_rotation_period(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    secret_id: str,
    location_id: str,
    topic_name: str,
) -> None:

    create_regional_secret_with_rotation.create_regional_secret_with_rotation(
        project_id, secret_id, location_id, topic_name
    )
    capsys.readouterr()

    updated_rotation_hours = 48
    update_regional_secret_rotation.update_regional_secret_rotation_period(
        project_id, secret_id, location_id
    )

    # Verify output contains the secret ID

    out, _ = capsys.readouterr()
    assert secret_id in out, f"Expected '{secret_id}' in output, got: {out}"

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    assert (
        retrieved_secret.rotation is not None
    ), "GetSecret: Rotation is nil, expected non-nil"
    expected_seconds = updated_rotation_hours * 3600
    actual_seconds = retrieved_secret.rotation.rotation_period.total_seconds()
    assert (
        actual_seconds == expected_seconds
    ), f"RotationPeriod mismatch: got {actual_seconds}, want {expected_seconds}"


def test_delete_regional_secret_rotation(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    secret_id: str,
    location_id: str,
    topic_name: str,
) -> None:
    # First create a secret with rotation configuration

    create_regional_secret_with_rotation.create_regional_secret_with_rotation(
        project_id, secret_id, location_id, topic_name
    )

    # Call the function to delete the rotation configuration

    delete_regional_secret_rotation.delete_regional_secret_rotation(
        project_id, secret_id, location_id
    )

    # Check the output contains the expected message

    out, _ = capsys.readouterr()
    assert "Removed rotation" in out
    assert secret_id in out

    # Verify rotation is removed with GetSecret

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )

    # Check that rotation configuration is removed

    assert (
        retrieved_secret.rotation == secretmanager_v1.types.Rotation()
    ), f"Rotation is {repr(retrieved_secret.rotation)}, expected None or empty"


def test_create_regional_secret_with_topic(
    capsys, project_id: str, secret_id: str, location_id: str, topic_name: str
):

    # Call the function being tested

    create_regional_secret_with_topic.create_regional_secret_with_topic(
        project_id, secret_id, location_id, topic_name
    )

    # Check the output contains expected text

    out, _ = capsys.readouterr()
    assert "Created secret" in out

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )

    assert (
        len(retrieved_secret.topics) == 1
    ), f"Expected 1 topic, got {len(retrieved_secret.topics)}"
    assert (
        retrieved_secret.topics[0].name == topic_name
    ), f"Topic mismatch: got {retrieved_secret.topics[0].name}, want {topic_name}"


def test_create_regional_secret_with_cmek(
    capsys, project_id: str, secret_id: str, location_id: str, kms_key_name: str
):

    create_regional_secret_with_cmek.create_regional_secret_with_cmek(
        project_id, secret_id, location_id, kms_key_name
    )

    # Check the output contains expected text

    out, _ = capsys.readouterr()
    assert "Created secret" in out
    assert secret_id in out
    assert kms_key_name in out

    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )

    # Check that the CMEK key name matches what we specified

    actual_key_name = retrieved_secret.customer_managed_encryption.kms_key_name
    assert (
        actual_key_name == kms_key_name
    ), f"CMEK key name mismatch: got {actual_key_name}, want {kms_key_name}"


def test_update_regional_secret_with_alias(
    project_id: str, location_id: str, regional_secret_version: Tuple[str, str, str]
) -> None:
    secret_id, _, _ = regional_secret_version
    update_regional_secret_with_alias.update_regional_secret_with_alias(
        project_id, secret_id, location_id
    )
    retrieved_secret = get_regional_secret.get_regional_secret(
        project_id, location_id, secret_id
    )
    assert retrieved_secret.version_aliases["test"] == 1
