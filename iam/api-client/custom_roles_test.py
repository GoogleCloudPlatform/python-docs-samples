# Copyright 2016 Google LLC
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

import os
import uuid

import googleapiclient.errors
import pytest

import custom_roles


GCLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]

CUSTOM_ROLE_NAME = "pythonTestCustomRole" + str(uuid.uuid1().int)
CUSTOM_ROLE_TITLE = "Python Test Custom Role"
CUSTOM_ROLE_DESCRIPTION = "This is a python test custom role"
CUSTOM_ROLE_PERMISSIONS = ["iam.roles.get"]
CUSTOM_ROLE_STAGE = "GA"
CUSTOM_ROLE_EMAIL = (
    CUSTOM_ROLE_NAME + "@" + GCLOUD_PROJECT + ".iam.gserviceaccount.com"
)


@pytest.fixture(scope="module")
def test_custom_role():
    # This custom role is reused in read/update tests.
    try:
        custom_roles.create_role(
            CUSTOM_ROLE_NAME,
            GCLOUD_PROJECT,
            CUSTOM_ROLE_TITLE,
            CUSTOM_ROLE_DESCRIPTION,
            CUSTOM_ROLE_PERMISSIONS,
            CUSTOM_ROLE_STAGE,
        )
    except googleapiclient.errors.HttpError as e:
        if "HttpError 409" not in str(e):
            raise e
        # Ignore error since we just reuse the same custom role.
        print('Re-using the custom role "{}".'.format(CUSTOM_ROLE_NAME))
    yield CUSTOM_ROLE_NAME
    # we don't delete this custom role for future tests.


@pytest.fixture(scope="function")
def unique_custom_role_name():
    UNIQUE_CUSTOM_ROLE_NAME = "pythonTestCustomRole" + str(uuid.uuid1().int)
    yield UNIQUE_CUSTOM_ROLE_NAME

    # Delete the custom role
    try:
        custom_roles.delete_role(UNIQUE_CUSTOM_ROLE_NAME, GCLOUD_PROJECT)
    except googleapiclient.errors.HttpError:
        print("Custom role already deleted.")


def test_query_testable_permissions(capsys):
    custom_roles.query_testable_permissions(
        "//cloudresourcemanager.googleapis.com/projects/" + GCLOUD_PROJECT
    )
    out, _ = capsys.readouterr()
    # Just make sure the sample printed out multiple permissions.
    assert "\n" in out


def test_get_role(capsys):
    custom_roles.get_role("roles/appengine.appViewer")
    out, _ = capsys.readouterr()
    assert "roles/" in out


def test_create_role(unique_custom_role_name, capsys):
    custom_roles.create_role(
        unique_custom_role_name,
        GCLOUD_PROJECT,
        CUSTOM_ROLE_TITLE,
        CUSTOM_ROLE_DESCRIPTION,
        CUSTOM_ROLE_PERMISSIONS,
        CUSTOM_ROLE_STAGE,
    )
    out, _ = capsys.readouterr()
    assert "Created role:" in out


def test_edit_role(test_custom_role, capsys):
    custom_roles.edit_role(
        test_custom_role,
        GCLOUD_PROJECT,
        CUSTOM_ROLE_TITLE,
        "Updated",
        CUSTOM_ROLE_PERMISSIONS,
        CUSTOM_ROLE_STAGE,
    )
    out, _ = capsys.readouterr()
    assert "Updated role:" in out


def test_list_roles(capsys):
    custom_roles.list_roles(GCLOUD_PROJECT)
    out, _ = capsys.readouterr()
    assert "roles/" in out


def test_disable_role(test_custom_role, capsys):
    custom_roles.disable_role(test_custom_role, GCLOUD_PROJECT)
    out, _ = capsys.readouterr()
    assert "Disabled role:" in out


def test_delete_role(unique_custom_role_name, capsys):
    custom_roles.create_role(
        unique_custom_role_name,
        GCLOUD_PROJECT,
        CUSTOM_ROLE_TITLE,
        CUSTOM_ROLE_DESCRIPTION,
        CUSTOM_ROLE_PERMISSIONS,
        CUSTOM_ROLE_STAGE,
    )
    custom_roles.delete_role(unique_custom_role_name, GCLOUD_PROJECT)
    out, _ = capsys.readouterr()
    assert "Deleted role:" in out
