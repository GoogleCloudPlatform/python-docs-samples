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

import pytest

from product_management import (
    create_product, delete_product, list_products,
    purge_orphan_products, update_product_labels)


PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_DISPLAY_NAME = 'fake_product_display_name_for_testing'
PRODUCT_CATEGORY = 'homegoods'
PRODUCT_ID = f'test_{uuid.uuid4()}'
KEY = 'fake_key_for_testing'
VALUE = 'fake_value_for_testing'


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # set up
    create_product(
        PROJECT_ID, LOCATION, PRODUCT_ID,
        PRODUCT_DISPLAY_NAME, PRODUCT_CATEGORY)

    yield None

    # tear down
    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)


def test_delete_product(capsys):
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID in out

    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID not in out


def test_update_product_labels(capsys):
    update_product_labels(PROJECT_ID, LOCATION, PRODUCT_ID, KEY, VALUE)
    out, _ = capsys.readouterr()
    assert KEY in out
    assert VALUE in out


def test_purge_orphan_products(capsys):
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID in out

    purge_orphan_products(PROJECT_ID, LOCATION, force=True)

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID not in out
