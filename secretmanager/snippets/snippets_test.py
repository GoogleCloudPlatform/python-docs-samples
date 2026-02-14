# Copyright 2019 Google LLC
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

import base64
from datetime import datetime, timedelta, timezone
import os
import time
from typing import Iterator, Optional, Tuple, Union
import uuid

from google.api_core import exceptions, retry
from google.cloud import resourcemanager_v3
from google.cloud import secretmanager, secretmanager_v1
from google.protobuf.duration_pb2 import Duration

import pytest

from access_secret_version import access_secret_version
from add_secret_version import add_secret_version
from bind_tags_to_secret import bind_tags_to_secret
from consume_event_notification import consume_event_notification
from create_secret import create_secret
from create_secret_with_annotations import create_secret_with_annotations
from create_secret_with_delayed_destroy import create_secret_with_delayed_destroy
from create_secret_with_expiration import create_secret_with_expiration
from create_secret_with_labels import create_secret_with_labels
from create_secret_with_rotation import create_secret_with_rotation
from create_secret_with_tags import create_secret_with_tags
from create_secret_with_topic import create_secret_with_topic
from create_secret_with_user_managed_replication import create_ummr_secret
from create_update_secret_label import create_update_secret_label
from delete_secret import delete_secret
from delete_secret_annotation import delete_secret_annotation
from delete_secret_expiration import delete_secret_expiration
from delete_secret_label import delete_secret_label
from delete_secret_rotation import delete_secret_rotation
from delete_secret_with_etag import delete_secret_with_etag
from destroy_secret_version import destroy_secret_version
from destroy_secret_version_with_etag import destroy_secret_version_with_etag
from detach_tag_binding import detach_tag
from disable_secret_version import disable_secret_version
from disable_secret_version_with_etag import disable_secret_version_with_etag
from disable_secret_with_delayed_destroy import disable_secret_with_delayed_destroy
from edit_secret_annotations import edit_secret_annotations
from enable_secret_version import enable_secret_version
from enable_secret_version_with_etag import enable_secret_version_with_etag
from get_secret import get_secret
from get_secret_version import get_secret_version
from iam_grant_access import iam_grant_access
from iam_revoke_access import iam_revoke_access
from list_secret_versions import list_secret_versions
from list_secret_versions_with_filter import list_secret_versions_with_filter
from list_secrets import list_secrets
from list_secrets_with_filter import list_secrets_with_filter
from list_tag_bindings import list_tag_bindings
from quickstart import quickstart
from update_secret import update_secret
from update_secret_expiration import update_secret_expiration
from update_secret_rotation import update_secret_rotation
from update_secret_with_alias import update_secret_with_alias
from update_secret_with_delayed_destroy import update_secret_with_delayed_destroy
from update_secret_with_etag import update_secret_with_etag
from view_secret_annotations import view_secret_annotations
from view_secret_labels import view_secret_labels


@pytest.fixture()
def client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


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
def rotation_period_hours() -> int:
    return 24


@pytest.fixture()
def ttl() -> Optional[str]:
    return "300s"


@pytest.fixture()
def label_key() -> str:
    return "googlecloud"


@pytest.fixture()
def label_value() -> str:
    return "rocks"


@pytest.fixture()
def annotation_key() -> str:
    return "annotationkey"


@pytest.fixture()
def annotation_value() -> str:
    return "annotationvalue"


@pytest.fixture()
def version_destroy_ttl() -> str:
    return 604800  # 7 days in seconds


@pytest.fixture()
def short_key_name() -> str:
    return f"python-test-key-{uuid.uuid4()}"


@pytest.fixture()
def short_value_name() -> str:
    return f"python-test-value-{uuid.uuid4()}"


@retry.Retry()
def retry_client_create_secret(
    client: secretmanager.SecretManagerServiceClient,
    request: Optional[Union[secretmanager.CreateSecretRequest, dict]],
) -> secretmanager.Secret:
    # Retry to avoid 503 error & flaky issues
    return client.create_secret(request=request)


@retry.Retry()
def retry_client_access_secret_version(
    client: secretmanager.SecretManagerServiceClient,
    request: Optional[Union[secretmanager.AccessSecretVersionRequest, dict]],
) -> secretmanager.AccessSecretVersionResponse:
    # Retry to avoid 503 error & flaky issues
    return client.access_secret_version(request=request)


@retry.Retry()
def retry_client_delete_secret(
    client: secretmanager.SecretManagerServiceClient,
    request: Optional[Union[secretmanager.DeleteSecretRequest, dict]],
) -> None:
    # Retry to avoid 503 error & flaky issues
    return client.delete_secret(request=request)


@retry.Retry()
def retry_client_add_secret_version(
    client: secretmanager.SecretManagerServiceClient,
    request: Optional[Union[secretmanager.AddSecretVersionRequest, dict]],
) -> secretmanager.SecretVersion:
    # Retry to avoid 503 error & flaky issues
    return client.add_secret_version(request=request)


@retry.Retry()
def retry_client_create_tag_key(
    tag_keys_client: resourcemanager_v3.TagKeysClient,
    request: Optional[Union[resourcemanager_v3.CreateTagKeyRequest, dict]],
) -> str:
    # Retry to avoid 503 error & flaky issues
    operation = tag_keys_client.create_tag_key(request=request)
    response = operation.result()

    return response.name


@retry.Retry()
def retry_client_create_tag_value(
    tag_values_client: resourcemanager_v3.TagValuesClient,
    request: Optional[Union[resourcemanager_v3.CreateTagValueRequest, dict]],
) -> str:
    # Retry to avoid 503 error & flaky issues
    operation = tag_values_client.create_tag_value(request=request)
    response = operation.result()

    return response.name


@retry.Retry()
def retry_client_delete_tag_value(
    tag_values_client: resourcemanager_v3.TagValuesClient,
    request: Optional[Union[resourcemanager_v3.DeleteTagValueRequest, dict]],
) -> str:
    # Retry to avoid 503 error & flaky issues
    time.sleep(15)  # Added a sleep to wait for the tag unbinding
    operation = tag_values_client.delete_tag_value(request=request)
    response = operation.result()
    return response.name


@retry.Retry()
def retry_client_delete_tag_key(
    tag_keys_client: resourcemanager_v3.TagKeysClient,
    request: Optional[Union[resourcemanager_v3.DeleteTagKeyRequest, dict]],
) -> str:
    # Retry to avoid 503 error & flaky issues
    operation = tag_keys_client.delete_tag_key(request=request)
    response = operation.result()
    return response.name


@pytest.fixture()
def secret_id(
    client: secretmanager.SecretManagerServiceClient, project_id: str
) -> Iterator[str]:
    secret_id = f"python-secret-{uuid.uuid4()}"

    yield secret_id
    secret_path = client.secret_path(project_id, secret_id)
    print(f"deleting secret {secret_id}")
    try:
        time.sleep(5)
        retry_client_delete_secret(client, request={"name": secret_path})
    except exceptions.NotFound:
        # Secret was already deleted, probably in the test
        print(f"Secret {secret_id} was not found.")


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
def secret(
    client: secretmanager.SecretManagerServiceClient,
    project_id: str,
    secret_id: str,
    label_key: str,
    label_value: str,
    annotation_key: str,
    annotation_value: str,
    ttl: Optional[str],
) -> Iterator[Tuple[str, str, str, str]]:
    print(f"creating secret {secret_id}")

    parent = f"projects/{project_id}"
    time.sleep(5)
    secret = retry_client_create_secret(
        client,
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {"automatic": {}},
                "ttl": ttl,
                "labels": {label_key: label_value},
                "annotations": {annotation_key: annotation_value},
            },
        },
    )

    yield project_id, secret_id, secret.etag


@pytest.fixture()
def secret_with_delayed_destroy(
    client: secretmanager.SecretManagerServiceClient,
    project_id: str,
    secret_id: str,
    version_destroy_ttl: int,
    ttl: Optional[str],
) -> Iterator[Tuple[str, str]]:
    print("creating secret with given secret id.")

    parent = f"projects/{project_id}"
    time.sleep(5)
    retry_client_create_secret(
        client,
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {"automatic": {}},
                "version_destroy_ttl": Duration(seconds=version_destroy_ttl),
            },
        },
    )

    yield project_id, secret_id


@pytest.fixture()
def secret_version(
    client: secretmanager.SecretManagerServiceClient, secret: Tuple[str, str, str]
) -> Iterator[Tuple[str, str, str, str]]:
    project_id, secret_id, _ = secret

    print(f"adding secret version to {secret_id}")
    parent = client.secret_path(project_id, secret_id)
    payload = b"hello world!"
    time.sleep(5)
    version = client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload}}
    )

    yield project_id, secret_id, version.name.rsplit("/", 1)[-1], version.etag


another_secret_version = secret_version


@pytest.fixture()
def pubsub_message() -> dict:
    message = "hello!"
    message_bytes = message.encode()
    base64_bytes = base64.b64encode(message_bytes)
    return {
        "attributes": {
            "eventType": "SECRET_UPDATE",
            "secretId": "projects/p/secrets/s",
        },
        "data": base64_bytes,
    }


def test_quickstart(project_id: str, secret_id: str) -> None:
    quickstart(project_id, secret_id)


def test_access_secret_version(secret_version: Tuple[str, str, str, str]) -> None:
    project_id, secret_id, version_id, _ = secret_version
    version = access_secret_version(project_id, secret_id, version_id)
    assert version.payload.data == b"hello world!"


def test_add_secret_version(secret: Tuple[str, str, str]) -> None:
    project_id, secret_id, _ = secret
    payload = "test123"
    version = add_secret_version(project_id, secret_id, payload)
    assert secret_id in version.name


def test_create_secret(
    project_id: str,
    secret_id: str,
    ttl: Optional[str],
) -> None:
    secret = create_secret(project_id, secret_id, ttl)

    assert secret_id in secret.name
    assert secret.expire_time


def test_create_secret_with_tags(
    project_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    tag_key, tag_value = tag_key_and_tag_value
    secret = create_secret_with_tags(project_id, secret_id, tag_key, tag_value)

    assert secret_id in secret.name


def test_bind_tags_to_secret(
    project_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    _, tag_value = tag_key_and_tag_value
    tag_resp = bind_tags_to_secret(project_id, secret_id, tag_value)

    assert secret_id in tag_resp.parent
    assert tag_value in tag_resp.tag_value


def test_create_secret_without_ttl(
    project_id: str,
    secret_id: str,
) -> None:
    secret = create_secret(project_id, secret_id, None)

    assert secret_id in secret.name
    assert not secret.expire_time


def test_create_secret_with_user_managed_replication(
    client: secretmanager.SecretManagerServiceClient,
    project_id: str,
    secret_id: str,
    ttl: Optional[str],
) -> None:
    locations = ["us-east1", "us-east4", "us-west1"]
    secret = create_ummr_secret(project_id, secret_id, locations, ttl)
    assert secret_id in secret.name


def test_create_secret_with_label(
    client: secretmanager.SecretManagerServiceClient,
    project_id: str,
    secret_id: str,
    label_key: str,
    label_value: str,
    ttl: Optional[str],
) -> None:
    labels = {label_key: label_value}
    secret = create_secret_with_labels(project_id, secret_id, labels, ttl)
    assert secret_id in secret.name


def test_create_secret_with_annotations(
    client: secretmanager.SecretManagerServiceClient,
    project_id: str,
    secret_id: str,
    annotation_key: str,
    annotation_value: str,
) -> None:
    annotations = {annotation_key: annotation_value}
    secret = create_secret_with_annotations(project_id, secret_id, annotations)
    assert secret_id in secret.name


def test_create_secret_with_delayed_destroy(
    client: secretmanager.SecretManagerServiceClient,
    project_id: str, secret_id: str, version_destroy_ttl: int
) -> None:
    secret = create_secret_with_delayed_destroy(project_id, secret_id, version_destroy_ttl)
    assert secret_id in secret.name
    assert timedelta(seconds=version_destroy_ttl) == secret.version_destroy_ttl


def test_delete_secret(
    client: secretmanager.SecretManagerServiceClient, secret: Tuple[str, str, str]
) -> None:
    project_id, secret_id, _ = secret
    delete_secret(project_id, secret_id)
    with pytest.raises(exceptions.NotFound):
        print(f"{client}")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        retry_client_access_secret_version(client, request={"name": name})


def test_delete_secret_annotation(
    secret: Tuple[str, str, str],
    annotation_key: str,
) -> None:
    project_id, secret_id, _ = secret
    secret = delete_secret_annotation(project_id, secret_id, annotation_key)
    assert secret_id in secret.name
    assert annotation_key not in secret.annotations


def test_delete_secret_labels(
    client: secretmanager.SecretManagerServiceClient,
    secret: Tuple[str, str, str],
    label_key: str,
) -> None:
    project_id, secret_id, _ = secret
    delete_secret_label(project_id, secret_id, label_key)
    with pytest.raises(exceptions.NotFound):
        print(f"{client}")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        retry_client_access_secret_version(client, request={"name": name})


def test_delete_secret_with_etag(
    client: secretmanager.SecretManagerServiceClient, secret: Tuple[str, str, str]
) -> None:
    project_id, secret_id, etag = secret
    delete_secret_with_etag(project_id, secret_id, etag)
    with pytest.raises(exceptions.NotFound):
        print(f"{client}")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        retry_client_access_secret_version(client, request={"name": name})


def test_destroy_secret_version(
    client: secretmanager.SecretManagerServiceClient,
    secret_version: Tuple[str, str, str, str],
) -> None:
    project_id, secret_id, version_id, _ = secret_version
    version = destroy_secret_version(project_id, secret_id, version_id)
    assert version.destroy_time


def test_destroy_secret_version_with_etag(
    client: secretmanager.SecretManagerServiceClient,
    secret_version: Tuple[str, str, str, str],
) -> None:
    project_id, secret_id, version_id, etag = secret_version
    version = destroy_secret_version_with_etag(project_id, secret_id, version_id, etag)
    assert version.destroy_time


def test_disable_secret_with_delayed_destroy(
    client: secretmanager.SecretManagerServiceClient,
    secret_with_delayed_destroy: Tuple[str, str],
) -> None:
    project_id, secret_id = secret_with_delayed_destroy
    updated_secret = disable_secret_with_delayed_destroy(project_id, secret_id)
    assert updated_secret.version_destroy_ttl == timedelta(0)


def test_enable_disable_secret_version(
    client: secretmanager.SecretManagerServiceClient,
    secret_version: Tuple[str, str, str, str],
) -> None:
    project_id, secret_id, version_id, _ = secret_version
    version = disable_secret_version(project_id, secret_id, version_id)
    assert version.state == secretmanager.SecretVersion.State.DISABLED

    version = enable_secret_version(project_id, secret_id, version_id)
    assert version.state == secretmanager.SecretVersion.State.ENABLED


def test_enable_disable_secret_version_with_etag(
    client: secretmanager.SecretManagerServiceClient,
    secret_version: Tuple[str, str, str, str],
) -> None:
    project_id, secret_id, version_id, etag = secret_version
    version = disable_secret_version_with_etag(project_id, secret_id, version_id, etag)
    assert version.state == secretmanager.SecretVersion.State.DISABLED

    version = enable_secret_version_with_etag(
        project_id, secret_id, version_id, version.etag
    )
    assert version.state == secretmanager.SecretVersion.State.ENABLED


def test_get_secret_version(
    client: secretmanager.SecretManagerServiceClient,
    secret_version: Tuple[str, str, str, str],
) -> None:
    project_id, secret_id, version_id, _ = secret_version
    version = get_secret_version(project_id, secret_id, version_id)
    assert secret_id in version.name
    assert version_id in version.name


def test_get_secret(
    client: secretmanager.SecretManagerServiceClient, secret: Tuple[str, str, str]
) -> None:
    project_id, secret_id, _ = secret
    snippet_secret = get_secret(project_id, secret_id)
    assert secret_id in snippet_secret.name


def test_iam_grant_access(
    client: secretmanager.SecretManagerServiceClient,
    secret: Tuple[str, str, str],
    iam_user: str,
) -> None:
    project_id, secret_id, _ = secret
    policy = iam_grant_access(project_id, secret_id, iam_user)
    assert any(iam_user in b.members for b in policy.bindings)


def test_iam_revoke_access(
    client: secretmanager.SecretManagerServiceClient,
    secret: Tuple[str, str, str],
    iam_user: str,
) -> None:
    project_id, secret_id, _ = secret
    policy = iam_revoke_access(project_id, secret_id, iam_user)
    assert not any(iam_user in b.members for b in policy.bindings)


def test_list_secret_versions(
    capsys: pytest.LogCaptureFixture,
    secret_version: Tuple[str, str, str, str],
    another_secret_version: Tuple[str, str, str, str],
) -> None:
    project_id, secret_id, version_id, _ = secret_version
    version_1 = get_secret_version(project_id, secret_id, version_id)
    _, _, another_version_id, _ = another_secret_version
    version_2 = get_secret_version(project_id, secret_id, another_version_id)
    list_secret_versions(project_id, secret_id)

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert f"Found secret version: {version_1.name}" in out
    assert f"Found secret version: {version_2.name}" in out


def test_list_secret_versions_with_filter(
    capsys: pytest.LogCaptureFixture,
    secret_version: Tuple[str, str, str, str],
    another_secret_version: Tuple[str, str, str, str],
) -> None:
    project_id, secret_id, version_id, _ = secret_version
    enabled = get_secret_version(project_id, secret_id, version_id)
    _, _, another_version_id, _ = another_secret_version
    disabled = disable_secret_version(project_id, secret_id, another_version_id)
    assert disabled.state == secretmanager.SecretVersion.State.DISABLED
    list_secret_versions_with_filter(project_id, secret_id, "state:ENABLED")

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert f"Found secret version: {enabled.name}" in out
    assert f"Found secret version: {disabled.name}" not in out


def test_view_secret_labels(
    capsys: pytest.LogCaptureFixture, secret: Tuple[str, str, str], label_key: str
) -> None:
    project_id, secret_id, _ = secret
    view_secret_labels(project_id, secret_id)

    out, _ = capsys.readouterr()
    assert label_key in out


def test_view_secret_annotations(
    capsys: pytest.LogCaptureFixture, secret: Tuple[str, str, str], annotation_key: str
) -> None:
    project_id, secret_id, _ = secret
    view_secret_annotations(project_id, secret_id)

    out, _ = capsys.readouterr()
    assert annotation_key in out


def test_list_secrets(
    capsys: pytest.LogCaptureFixture, secret: Tuple[str, str, str]
) -> None:
    project_id, secret_id, _ = secret
    got_secret = get_secret(project_id, secret_id)
    list_secrets(project_id)

    out, _ = capsys.readouterr()
    assert f"Found secret: {got_secret.name}" in out


def test_list_secrets_with_filter(
    capsys: pytest.LogCaptureFixture, secret: Tuple[str, str, str]
) -> None:
    project_id, secret_id, _ = secret
    unlabeled = get_secret(project_id, secret_id)
    list_secrets_with_filter(project_id, "labels.secretmanager:rocks")

    out, _ = capsys.readouterr()
    assert f"Found secret: {unlabeled.name}" not in out

    labeled = update_secret(project_id, secret_id)
    assert labeled.labels["secretmanager"] == "rocks"
    list_secrets_with_filter(project_id, "labels.secretmanager:rocks")

    out, _ = capsys.readouterr()
    assert f"Found secret: {labeled.name}" in out


def test_create_update_secret_label(
    secret: Tuple[str, str, str], label_key: str
) -> None:
    project_id, secret_id, _ = secret
    updated_label_value = "vibes"
    labels = {label_key: updated_label_value}
    updated_secret = create_update_secret_label(project_id, secret_id, labels)
    assert updated_secret.labels[label_key] == updated_label_value


def test_edit_secret_annotations(
    secret: Tuple[str, str, str], annotation_key: str
) -> None:
    project_id, secret_id, _ = secret
    updated_annotation_value = "updatedannotationvalue"
    annotations = {annotation_key: updated_annotation_value}
    updated_secret = edit_secret_annotations(project_id, secret_id, annotations)
    assert updated_secret.annotations[annotation_key] == updated_annotation_value


def test_update_secret(secret: Tuple[str, str, str]) -> None:
    project_id, secret_id, _ = secret
    updated_secret = update_secret(project_id, secret_id)
    assert updated_secret.labels["secretmanager"] == "rocks"


def test_consume_event_notification(pubsub_message: dict) -> None:
    got = consume_event_notification(pubsub_message, None)
    assert (
        got == "Received SECRET_UPDATE for projects/p/secrets/s. New metadata: hello!"
    )


def test_update_secret_with_etag(secret: Tuple[str, str, str]) -> None:
    project_id, secret_id, etag = secret
    updated_secret = update_secret_with_etag(project_id, secret_id, etag)
    assert updated_secret.labels["secretmanager"] == "rocks"


def test_update_secret_with_alias(secret_version: Tuple[str, str, str, str]) -> None:
    project_id, secret_id, version_id, _ = secret_version
    secret = update_secret_with_alias(project_id, secret_id)
    assert secret.version_aliases["test"] == 1


def test_update_secret_with_delayed_destroy(secret_with_delayed_destroy: Tuple[str, str], version_destroy_ttl: str) -> None:
    project_id, secret_id = secret_with_delayed_destroy
    updated_version_destroy_ttl_value = 118400
    updated_secret = update_secret_with_delayed_destroy(project_id, secret_id, updated_version_destroy_ttl_value)
    assert updated_secret.version_destroy_ttl == timedelta(seconds=updated_version_destroy_ttl_value)


def test_list_tag_bindings(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    # Get the tag value from the fixture

    _, tag_value = tag_key_and_tag_value

    # Create the secret and bind tag (using existing fixtures)

    bind_tags_to_secret(project_id, secret_id, tag_value)

    # Call the function being tested

    list_tag_bindings(project_id, secret_id)

    # Verify the tag value is in the returned bindings

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert tag_value in out


def test_detach_tag(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    tag_key_and_tag_value: Tuple[str, str],
    secret_id: str,
) -> None:
    """Test detaching a tag from a secret."""
    # Get the tag value from the fixture

    _, tag_value = tag_key_and_tag_value

    # First bind the tag to the secret

    bind_tags_to_secret(project_id, secret_id, tag_value)

    # Now detach the tag

    detach_tag(project_id, secret_id, tag_value)

    out, _ = capsys.readouterr()
    assert "Detached tag value" in out

    list_tag_bindings(project_id, secret_id)

    # Verify the tag value is no longer in the returned bindings

    out, _ = capsys.readouterr()
    assert tag_value not in out


def test_create_secret_with_expiration(project_id: str, secret_id: str) -> None:
    """Test creating a secret with an expiration time."""

    # Set expire time to 1 hour from now

    expire_time = datetime.now(timezone.utc) + timedelta(hours=1)
    create_secret_with_expiration(project_id, secret_id)

    retrieved_secret = get_secret(project_id, secret_id)
    # Verify the secret has an expiration time

    assert (
        retrieved_secret.expire_time is not None
    ), "ExpireTime is None, expected non-None"

    retrieved_expire_time = retrieved_secret.expire_time.astimezone(timezone.utc)

    retrieved_timestamp = int(retrieved_expire_time.timestamp())
    expected_timestamp = int(expire_time.timestamp())

    time_diff = abs(retrieved_timestamp - expected_timestamp)
    assert time_diff <= 1, f"ExpireTime difference too large: {time_diff} seconds."


def test_update_secret_expiration(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    secret_id: str,
) -> None:
    create_secret_with_expiration(project_id, secret_id)

    # Update expire time to 2 hours

    new_expire = datetime.now(timezone.utc) + timedelta(
        hours=2
    )  # 2 hours from now in seconds
    update_secret_expiration(project_id, secret_id)

    # Verify output contains expected message

    out, _ = capsys.readouterr()
    assert "Updated secret" in out

    retrieved_secret = get_secret(project_id, secret_id)
    assert (
        retrieved_secret.expire_time is not None
    ), "ExpireTime is None, expected non-None"
    retrieved_expire_time = retrieved_secret.expire_time.astimezone(timezone.utc)
    retrieved_timestamp = int(retrieved_expire_time.timestamp())

    new_expire = int(new_expire.timestamp())
    time_diff = abs(retrieved_timestamp - new_expire)
    assert time_diff <= 1, f"ExpireTime difference too large: {time_diff} seconds. "


def test_delete_expiration(
    capsys: pytest.LogCaptureFixture, project_id: str, secret_id: str
) -> None:

    create_secret_with_expiration(project_id, secret_id)

    delete_secret_expiration(project_id, secret_id)
    out, _ = capsys.readouterr()
    assert "Removed expiration" in out

    # Verify expire time is removed with GetSecret

    retrieved_secret = get_secret(project_id, secret_id)
    assert (
        retrieved_secret.expire_time is None
    ), f"ExpireTime is {retrieved_secret.expire_time}, expected None"


def test_create_secret_with_rotation(
    capsys: pytest.LogCaptureFixture,
    project_id: str,
    secret_id: str,
    topic_name: str,
    rotation_period_hours: int,
) -> None:
    """Test creating a secret with rotation configuration."""

    # Create the secret with rotation

    create_secret_with_rotation(project_id, secret_id, topic_name)

    # Verify output contains expected message

    out, _ = capsys.readouterr()
    assert "Created secret" in out, f"Expected 'Created secret' in output, got: {out}"

    retrieved_secret = get_secret(project_id, secret_id)

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


def test_update_secret_rotation_period(
    capsys: pytest.LogCaptureFixture, project_id: str, secret_id: str, topic_name: str
) -> None:

    create_secret_with_rotation(project_id, secret_id, topic_name)
    capsys.readouterr()

    updated_rotation_hours = 48
    update_secret_rotation(project_id, secret_id)

    # Verify output contains the secret ID

    out, _ = capsys.readouterr()
    assert secret_id in out, f"Expected '{secret_id}' in output, got: {out}"

    retrieved_secret = get_secret(project_id, secret_id)
    assert (
        retrieved_secret.rotation is not None
    ), "GetSecret: Rotation is nil, expected non-nil"
    expected_seconds = updated_rotation_hours * 3600
    actual_seconds = retrieved_secret.rotation.rotation_period.total_seconds()
    assert (
        actual_seconds == expected_seconds
    ), f"RotationPeriod mismatch: got {actual_seconds}, want {expected_seconds}"


def test_delete_secret_rotation(
    capsys: pytest.LogCaptureFixture, project_id: str, secret_id: str, topic_name: str
) -> None:

    create_secret_with_rotation(project_id, secret_id, topic_name)

    # Delete the rotation

    delete_secret_rotation(project_id, secret_id)
    out, _ = capsys.readouterr()
    assert "Removed rotation from secret" in out
    assert secret_id in out

    retrieved_secret = get_secret(project_id, secret_id)
    assert (
        retrieved_secret.rotation == secretmanager_v1.types.Rotation()
    ), f"Rotation is {repr(retrieved_secret.rotation)}, expected None or empty"


def test_create_secret_with_topic(
    capsys, project_id: str, secret_id: str, topic_name: str
):

    # Call the function being tested

    create_secret_with_topic(project_id, secret_id, topic_name)

    # Check the output contains expected text

    out, _ = capsys.readouterr()
    assert "Created secret" in out

    retrieved_secret = get_secret(project_id, secret_id)

    assert (
        len(retrieved_secret.topics) == 1
    ), f"Expected 1 topic, got {len(retrieved_secret.topics)}"
    assert (
        retrieved_secret.topics[0].name == topic_name
    ), f"Topic mismatch: got {retrieved_secret.topics[0].name}, want {topic_name}"
