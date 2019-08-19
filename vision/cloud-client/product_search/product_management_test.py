# Copyright 2016 Google Inc. All Rights Reserved.
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

import pytest

from product_management import (
    create_product, delete_product, get_product, list_products,
    purge_orphan_products, update_product_labels)


PROJECT_ID = os.getenv('GCLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_DISPLAY_NAME = 'fake_product_display_name_for_testing'
PRODUCT_CATEGORY = 'homegoods'
PRODUCT_ID = 'fake_product_id_for_testing'
KEY = 'fake_key_for_testing'
VALUE = 'fake_value_for_testing'


@pytest.fixture
def product():
    # set up
    create_product(
        PROJECT_ID, LOCATION, PRODUCT_ID,
        PRODUCT_DISPLAY_NAME, PRODUCT_CATEGORY)

    yield None

    # tear down
    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)


def test_create_product(capsys):
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID not in out

    create_product(
        PROJECT_ID, LOCATION, PRODUCT_ID,
        PRODUCT_DISPLAY_NAME, PRODUCT_CATEGORY)
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID in out

    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)


def test_delete_product(capsys, product):
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID in out

    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID not in out


def test_update_product_labels(capsys, product):
    get_product(PROJECT_ID, LOCATION, PRODUCT_ID)
    out, _ = capsys.readouterr()
    assert KEY not in out
    assert VALUE not in out

    update_product_labels(PROJECT_ID, LOCATION, PRODUCT_ID, KEY, VALUE)
    out, _ = capsys.readouterr()
    assert KEY in out
    assert VALUE in out

    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)


def test_purge_orphan_products(capsys, product):
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID in out

    purge_orphan_products(PROJECT_ID, LOCATION, force=True)

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID not in out
