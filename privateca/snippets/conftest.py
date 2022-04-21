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

import uuid

import google.auth
import pytest

from create_ca_pool import create_ca_pool
from create_certificate_authority import create_certificate_authority
from create_certificate_template import create_certificate_template
from delete_ca_pool import delete_ca_pool
from delete_certificate_authority import delete_certificate_authority
from delete_certificate_template import delete_certificate_template

PROJECT = google.auth.default()[1]
LOCATION = "europe-west1"
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CA_DURATION = 1000000


def generate_name() -> str:
    return "test-" + uuid.uuid4().hex[:10]


@pytest.fixture
def ca_pool():
    CA_POOL_NAME = generate_name()

    create_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)

    yield CA_POOL_NAME

    delete_ca_pool(PROJECT, LOCATION, CA_POOL_NAME)


@pytest.fixture
def certificate_authority(ca_pool):
    CA_NAME = generate_name()

    create_certificate_authority(
        PROJECT, LOCATION, ca_pool, CA_NAME, COMMON_NAME, ORGANIZATION, CA_DURATION
    )

    yield ca_pool, CA_NAME

    delete_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)


@pytest.fixture
def deleted_certificate_authority(ca_pool):
    CA_NAME = generate_name()

    create_certificate_authority(
        PROJECT, LOCATION, ca_pool, CA_NAME, COMMON_NAME, ORGANIZATION, CA_DURATION
    )

    delete_certificate_authority(PROJECT, LOCATION, ca_pool, CA_NAME)

    yield ca_pool, CA_NAME


@pytest.fixture
def certificate_template():
    TEMPLATE_NAME = generate_name()

    create_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)

    yield TEMPLATE_NAME

    delete_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)
