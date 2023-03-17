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
import random
import re
import typing
import uuid

import backoff
import google.auth

from create_ca_pool import create_ca_pool
from create_certificate_authority import create_certificate_authority
from delete_ca_pool import delete_ca_pool
from delete_certificate_authority import delete_certificate_authority
from disable_certificate_authority import disable_certificate_authority
from enable_certificate_authority import enable_certificate_authority
from monitor_certificate_authority import create_ca_monitor_policy
from undelete_certificate_authority import undelete_certificate_authority
from update_certificate_authority import update_ca_label

PROJECT = google.auth.default()[1]
LOCATION = "us-central1"
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CA_DURATION = 1000000


def generate_name() -> str:
    return "i" + uuid.uuid4().hex[:10]


# We are hitting 5 CAs per minute limit which can't be changed
# We set the backoff function to use 4 as base - this way the 3rd try
# should wait for 64 seconds and avoid per minute quota
# Adding some random amount of time to the backoff timer, so that we
# don't try to call the API at the same time in different tests running
# simultaneously.
def backoff_expo_wrapper():
    for exp in backoff.expo(base=4):
        if exp is None:
            yield None
        yield exp * (1 + random.random())


@backoff.on_exception(backoff_expo_wrapper, Exception, max_tries=3)
def test_create_certificate(capsys: typing.Any) -> None:
    CA_POOL_NAME = generate_name()
    CA_NAME = generate_name()

    create_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)
    create_certificate_authority(
        PROJECT, LOCATION, CA_POOL_NAME, CA_NAME, COMMON_NAME, ORGANIZATION, CA_DURATION
    )

    out, _ = capsys.readouterr()

    assert re.search(
        f'Operation result: name: "projects/{PROJECT}/locations/{LOCATION}/caPools/{CA_POOL_NAME}/certificateAuthorities/{CA_NAME}"',
        out,
    )

    delete_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)
    delete_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)


def test_enable_and_disable_certificate_authority(
    certificate_authority, capsys: typing.Any
) -> None:
    CA_POOL_NAME, CA_NAME = certificate_authority

    enable_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)
    disable_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)

    out, _ = capsys.readouterr()

    assert re.search(
        f"Enabled Certificate Authority: {CA_NAME}",
        out,
    )
    assert re.search(
        f"Disabled Certificate Authority: {CA_NAME}",
        out,
    )


def test_undelete_certificate_authority(
    deleted_certificate_authority, capsys: typing.Any
) -> None:
    CA_POOL_NAME, CA_NAME = deleted_certificate_authority

    undelete_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)
    delete_certificate_authority(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)
    delete_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)

    out, _ = capsys.readouterr()
    assert re.search(
        f"Successfully undeleted Certificate Authority: {CA_NAME}",
        out,
    )
    assert re.search(
        f"Successfully deleted Certificate Authority: {CA_NAME}",
        out,
    )


def test_update_certificate_authority(
    certificate_authority, capsys: typing.Any
) -> None:
    CA_POOL_NAME, CA_NAME = certificate_authority

    update_ca_label(PROJECT, LOCATION, CA_POOL_NAME, CA_NAME)

    out, _ = capsys.readouterr()

    assert "Successfully updated the labels !" in out


@backoff.on_exception(backoff_expo_wrapper, Exception, max_tries=3)
def test_create_monitor_ca_policy(capsys: typing.Any) -> None:
    create_ca_monitor_policy(PROJECT)

    out, _ = capsys.readouterr()

    assert "Monitoring policy successfully created!" in out
