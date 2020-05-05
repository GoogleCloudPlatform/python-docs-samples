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

import os
import pytest
import uuid

from quickstart import quickstart
from access_secret_version import access_secret_version
from add_secret_version import add_secret_version
from create_secret import create_secret
from delete_secret import delete_secret
from destroy_secret_version import destroy_secret_version
from disable_secret_version import disable_secret_version
from enable_secret_version import enable_secret_version
from get_secret import get_secret
from get_secret_version import get_secret_version
from iam_grant_access import iam_grant_access
from iam_revoke_access import iam_revoke_access
from list_secret_versions import list_secret_versions
from list_secrets import list_secrets
from update_secret import update_secret

from google.api_core import exceptions
from google.cloud import secretmanager


@pytest.fixture()
def client():
    return secretmanager.SecretManagerServiceClient()


@pytest.fixture()
def project_id():
    return os.environ['GCLOUD_PROJECT']


@pytest.fixture()
def iam_user():
    return 'serviceAccount:' + os.environ['GCLOUD_SECRETS_SERVICE_ACCOUNT']


@pytest.fixture()
def secret(client, project_id):
    parent = client.project_path(project_id)
    secret_id = 'python-secret-{}'.format(uuid.uuid4())

    print('creating secret {}'.format(secret_id))
    secret = client.create_secret(parent, secret_id, {
        'replication': {
            'automatic': {},
        },
    })

    yield project_id, secret_id

    print('deleting secret {}'.format(secret_id))
    try:
        client.delete_secret(secret.name)
    except exceptions.NotFound:
        # Secret was already deleted, probably in the test
        pass


another_secret = secret


@pytest.fixture()
def secret_version(client, secret):
    project_id, secret_id = secret

    print('adding secret version to {}'.format(secret_id))
    parent = client.secret_path(project_id, secret_id)
    payload = 'hello world!'.encode('UTF-8')
    version = client.add_secret_version(parent, {'data': payload})

    yield project_id, secret_id, version.name.rsplit('/', 1)[-1]


another_secret_version = secret_version


def test_quickstart(project_id):
    secret_id = 'python-secret-{}'.format(uuid.uuid4())
    quickstart(project_id, secret_id)


def test_access_secret_version(secret_version):
    project_id, secret_id, version_id = secret_version
    version = access_secret_version(project_id, secret_id, version_id)
    assert version.payload.data == b'hello world!'


def test_add_secret_version(secret):
    project_id, secret_id = secret
    payload = 'test123'
    version = add_secret_version(project_id, secret_id, payload)
    assert secret_id in version.name


def test_create_secret(client, project_id):
    secret_id = 'python-secret-{}'.format(uuid.uuid4())
    secret = create_secret(project_id, secret_id)
    assert secret_id in secret.name
    client.delete_secret(secret.name)


def test_delete_secret(client, secret):
    project_id, secret_id = secret
    delete_secret(project_id, secret_id)
    with pytest.raises(exceptions.NotFound):
        print('{}'.format(client))
        name = client.secret_version_path(project_id, secret_id, 'latest')
        client.access_secret_version(name)


def test_destroy_secret_version(client, secret_version):
    project_id, secret_id, version_id = secret_version
    version = destroy_secret_version(project_id, secret_id, version_id)
    assert version.destroy_time


def test_enable_disable_secret_version(client, secret_version):
    project_id, secret_id, version_id = secret_version
    version = disable_secret_version(project_id, secret_id, version_id)
    assert version.state == secretmanager.enums.SecretVersion.State.DISABLED

    version = enable_secret_version(project_id, secret_id, version_id)
    assert version.state == secretmanager.enums.SecretVersion.State.ENABLED


def test_get_secret_version(client, secret_version):
    project_id, secret_id, version_id = secret_version
    version = get_secret_version(project_id, secret_id, version_id)
    assert secret_id in version.name
    assert version_id in version.name


def test_get_secret(client, secret):
    project_id, secret_id = secret
    snippet_secret = get_secret(project_id, secret_id)
    assert secret_id in snippet_secret.name


def test_iam_grant_access(client, secret, iam_user):
    project_id, secret_id = secret
    policy = iam_grant_access(project_id, secret_id, iam_user)
    assert any(iam_user in b.members for b in policy.bindings)


def test_iam_revoke_access(client, secret, iam_user):
    project_id, secret_id = secret
    policy = iam_revoke_access(project_id, secret_id, iam_user)
    assert not any(iam_user in b.members for b in policy.bindings)


def test_list_secret_versions(capsys, secret_version, another_secret_version):
    project_id, secret_id, version_id = secret_version
    _, _, another_version_id = another_secret_version
    list_secret_versions(project_id, secret_id)

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert version_id in out
    assert another_version_id in out


def test_list_secrets(capsys, secret, another_secret):
    project_id, secret_id = secret
    _, another_secret_id = another_secret
    list_secrets(project_id)

    out, _ = capsys.readouterr()
    assert secret_id in out
    assert another_secret_id in out


def test_update_secret(secret):
    project_id, secret_id = secret
    secret = update_secret(project_id, secret_id)
    assert secret.labels['secretmanager'] == 'rocks'
