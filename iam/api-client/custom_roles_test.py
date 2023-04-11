# Copyright 2023 Google LLC
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

import pytest

import custom_roles


GCLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


# A single custom role is created, used for all tests, then deleted, to minimize
# the total number of custom roles in existence. Once a custom role is deleted,
# it can take up to 14 days before it stops counting against the maximum number
# of custom roles allowed.
#
# Since this fixture will throw an exception upon failing to create or delete
# a custom role, there are no separatetests for those activities needed.
@pytest.fixture(scope="module")
def custom_role():
    role_name = "pythonTestCustomRole" + str(uuid.uuid4().hex)
    custom_roles.create_role(
        role_name,
        GCLOUD_PROJECT,
        "Python Test Custom Role",
        "This is a python test custom role",
        ["iam.roles.get"],
        "GA",
    )

    yield role_name

    custom_roles.delete_role(role_name, GCLOUD_PROJECT)


def test_query_testable_permissions(capsys):
    custom_roles.query_testable_permissions(
        "//cloudresourcemanager.googleapis.com/projects/" + GCLOUD_PROJECT
    )
    out, _ = capsys.readouterr()
    # Just make sure the sample printed out multiple permissions.
    assert "\n" in out


def test_list_roles(capsys):
    custom_roles.list_roles(GCLOUD_PROJECT)
    out, _ = capsys.readouterr()
    assert "roles/" in out


def test_get_role(capsys):
    custom_roles.get_role("roles/appengine.appViewer")
    out, _ = capsys.readouterr()
    assert "roles/" in out


def test_edit_role(custom_role, capsys):
    custom_roles.edit_role(
        custom_role,
        GCLOUD_PROJECT,
        "Python Test Custom Role",
        "This is a python test custom role",
        "Updated",
        ["iam.roles.get"],
        "GA",
    )
    out, _ = capsys.readouterr()
    assert "Updated role:" in out


def test_disable_role(custom_role, capsys):
    custom_roles.disable_role(custom_role, GCLOUD_PROJECT)
    out, _ = capsys.readouterr()
    assert "Disabled role:" in out
