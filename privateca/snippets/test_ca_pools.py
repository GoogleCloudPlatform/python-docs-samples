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

import re
import typing
import uuid

import google.auth

from conftest import delete_stale_resources, LOCATION

from create_ca_pool import create_ca_pool
from delete_ca_pool import delete_ca_pool
from list_ca_pools import list_ca_pools
from update_ca_pool_issuance_policy import update_ca_pool_issuance_policy

PROJECT = google.auth.default()[1]

delete_stale_resources()


def generate_name() -> str:
    return "test-" + uuid.uuid4().hex[:10]


def test_create_ca_pool(capsys: typing.Any, ca_pool_autodelete_name) -> None:

    create_ca_pool(PROJECT, LOCATION, ca_pool_autodelete_name)

    out, _ = capsys.readouterr()

    assert re.search(
        f'Operation result: name: "projects/{PROJECT}/locations/{LOCATION}/caPools/{ca_pool_autodelete_name}"',
        out,
    )


def test_list_ca_pools(capsys: typing.Any, ca_pool_autodelete_name, ca_pool_autodelete_name2) -> None:

    create_ca_pool(PROJECT, LOCATION, ca_pool_autodelete_name)
    create_ca_pool(PROJECT, LOCATION, ca_pool_autodelete_name2)
    list_ca_pools(PROJECT, LOCATION)

    out, _ = capsys.readouterr()

    assert "Available CA pools:" in out
    assert f"{ca_pool_autodelete_name}\n" in out
    assert f"{ca_pool_autodelete_name2}\n" in out


def test_delete_ca_pool(capsys: typing.Any) -> None:
    CA_POOL_NAME = generate_name()

    create_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)
    delete_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)

    out, _ = capsys.readouterr()

    assert re.search(f"Deleted CA Pool: {CA_POOL_NAME}", out)


def test_update_ca_pool_issuance_policy(ca_pool, capsys: typing.Any) -> None:
    CA_POOL_NAME = ca_pool

    update_ca_pool_issuance_policy(PROJECT, LOCATION, CA_POOL_NAME)

    out, _ = capsys.readouterr()

    assert "CA Pool Issuance policy has been updated successfully!" in out
