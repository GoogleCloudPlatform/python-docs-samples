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
import os
import time
import uuid

from google.api_core import exceptions
from google.cloud import secretmanager
import pytest

from access_secret_version import access_secret_version
from add_secret_version import add_secret_version
from consume_event_notification import consume_event_notification
from create_secret import create_secret
from create_secret_with_user_managed_replication import create_ummr_secret
from delete_secret import delete_secret
from delete_secret_with_etag import delete_secret_with_etag
from destroy_secret_version import destroy_secret_version
from destroy_secret_version_with_etag import destroy_secret_version_with_etag
from disable_secret_version import disable_secret_version
from disable_secret_version_with_etag import disable_secret_version_with_etag
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
from quickstart import quickstart
from update_secret import update_secret
from update_secret_with_alias import update_secret_with_alias
from update_secret_with_etag import update_secret_with_etag


@pytest.fixture()
def client():
    return secretmanager.SecretManagerServiceClient()


@pytest.fixture()
def project_id():
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def iam_user():
    return "serviceAccount:" + os.environ["GCLOUD_SECRETS_SERVICE_ACCOUNT"]


@pytest.fixture()
def secret_id(client, project_id):
    secret_id = f"python-secret-{uuid.uuid4()}"

    yield secret_id

    secret_path = client.secret_path(project_id, secret_id)
    print(f"deleting secret {secret_id}")
    try:
        time.sleep(5)
        client.delete_secret(request={"name": secret_path})
    except exceptions.NotFound:
        # Secret was already deleted, probably in the test
        print(f"Secret {secret_id} was not found.")
        pass


@pytest.fixture()
def secret(client, project_id, secret_id):
    print(f"creating secret {secret_id}")

    parent = f"projects/{project_id}"
    time.sleep(5)
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    yield project_id, secret_id, secret.etag


@pytest.fixture()
def secret_version(client, secret):
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
def pubsub_message():
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


def test_quickstart(project_id, secret_id):
    quickstart(project_id, secret_id)


def test_access_secret_version(secret_version):
    project_id, secret_id, version_id, _ = secret_version
    version = access_secret_version(project_id, secret_id, version_id)
    assert version.payload.data == b"hello world!"


def test_add_secret_version(secret):
    project_id, secret_id, _ = secret
    payload = "test123"
    version = add_secret_version(project_id, secret_id, payload)
    assert secret_id in version.name


def test_create_secret(client, project_id, secret_id):
    secret = create_secret(project_id, secret_id)
    assert secret_id in secret.name


def test_create_secret_with_user_managed_replication(client, project_id, secret_id):
    locations = ["us-east1", "us-east4", "us-west1"]
    secret = create_ummr_secret(project_id, secret_id, locations)
    assert secret_id in secret.name


def test_delete_secret(client, secret):
    project_id, secret_id, _ = secret
    delete_secret(project_id, secret_id)
    with pytest.raises(exceptions.NotFound):
        print(f"{client}")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        client.access_secret_version(request={"name": name})


def test_delete_secret_with_etag(client, secret):
    project_id, secret_id, etag = secret
    delete_secret_with_etag(project_id, secret_id, etag)
    with pytest.raises(exceptions.NotFound):
        print(f"{client}")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        client.access_secret_version(request={"name": name})


def test_destroy_secret_version(client, secret_version):
    project_id, secret_id, version_id, _ = secret_version
    version = destroy_secret_version(project_id, secret_id, version_id)
    assert version.destroy_time


def test_destroy_secret_version_with_etag(client, secret_version):
    project_id, secret_id, version_id, etag = secret_version
    version = destroy_secret_version_with_etag(project_id, secret_id, version_id, etag)
    assert version.destroy_time


def test_enable_disable_secret_version(client, secret_version):
    project_id, secret_id, version_id, _ = secret_version
    version = disable_secret_version(project_id, secret_id, version_id)
    assert version.state == secretmanager.SecretVersion.State.DISABLED

    version = enable_secret_version(project_id, secret_id, version_id)
    assert version.state == secretmanager.SecretVersion.State.ENABLED


def test_enable_disable_secret_version_with_etag(client, secret_version):
    project_id, secret_id, version_id, etag = secret_version
    version = disable_secret_version_with_etag(project_id, secret_id, version_id, etag)
    assert version.state == secretmanager.SecretVersion.State.DISABLED

    version = enable_secret_version_with_etag(
        project_id, secret_id, version_id, version.etag
    )
    assert version.state == secretmanager.SecretVersion.State.ENABLED


def test_get_secret_version(client, secret_version):
    project_id, secret_id, version_id, _ = secret_version
    version = get_secret_version(project_id, secret_id, version_id)
    assert secret_id in version.name
    assert version_id in version.name


def test_get_secret(client, secret):
    project_id, secret_id, _ = secret
    snippet_secret = get_secret(project_id, secret_id)
    assert secret_id in snippet_secret.name


def test_iam_grant_access(client, secret, iam_user):
    project_id, secret_id, _ = secret
    policy = iam_grant_access(project_id, secret_id, iam_user)
    assert any(iam_user in b.members for b in policy.bindings)


def test_iam_revoke_access(client, secret, iam_user):
    project_id, secret_id, _ = secret
    policy = iam_revoke_access(project_id, secret_id, iam_user)
    assert not any(iam_user in b.members for b in policy.bindings)


def test_list_secret_versions(capsys, secret_version, another_secret_version):
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
    capsys, secret_version, another_secret_version
):
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


def test_list_secrets(capsys, secret):
    project_id, secret_id, _ = secret
    secret = get_secret(project_id, secret_id)
    list_secrets(project_id)

    out, _ = capsys.readouterr()
    assert f"Found secret: {secret.name}" in out


def test_list_secrets_with_filter(capsys, secret):
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


def test_update_secret(secret):
    project_id, secret_id, _ = secret
    secret = update_secret(project_id, secret_id)
    assert secret.labels["secretmanager"] == "rocks"


def test_consume_event_notification(pubsub_message):
    got = consume_event_notification(pubsub_message, None)
    assert (
        got == "Received SECRET_UPDATE for projects/p/secrets/s. New metadata: hello!"
    )


def test_update_secret_with_etag(secret):
    project_id, secret_id, etag = secret
    secret = update_secret_with_etag(project_id, secret_id, etag)
    assert secret.labels["secretmanager"] == "rocks"


def test_update_secret_with_alias(secret_version):
    project_id, secret_id, version_id, _ = secret_version
    secret = update_secret_with_alias(project_id, secret_id)
    assert secret.version_aliases["test"] == 1
