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

from product_in_product_set_management import (
    add_product_to_product_set, list_products_in_product_set,
    purge_products_in_product_set, remove_product_from_product_set)
from product_management import create_product, delete_product, list_products
from product_set_management import (
    create_product_set, delete_product_set)


PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_SET_DISPLAY_NAME = 'fake_product_set_display_name_for_testing'

PRODUCT_DISPLAY_NAME = 'fake_product_display_name_for_testing'
PRODUCT_CATEGORY = 'homegoods'


@pytest.fixture(scope="function")
def test_resources():
    # set up
    product_set_id = f'test_set_{uuid.uuid4()}'
    product_id = f'test_product_{uuid.uuid4()}'
    create_product_set(
        PROJECT_ID, LOCATION, product_set_id, PRODUCT_SET_DISPLAY_NAME)
    create_product(
        PROJECT_ID, LOCATION, product_id,
        PRODUCT_DISPLAY_NAME, PRODUCT_CATEGORY)

    yield product_set_id, product_id

    # tear down
    delete_product(PROJECT_ID, LOCATION, product_id)
    delete_product_set(PROJECT_ID, LOCATION, product_set_id)


def test_add_product_to_product_set(capsys, test_resources):
    product_set_id, product_id = test_resources
    add_product_to_product_set(
        PROJECT_ID, LOCATION, product_id, product_set_id)
    list_products_in_product_set(PROJECT_ID, LOCATION, product_set_id)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(product_id) in out


def test_remove_product_from_product_set(capsys, test_resources):
    product_set_id, product_id = test_resources
    add_product_to_product_set(
        PROJECT_ID, LOCATION, product_id, product_set_id)
    list_products_in_product_set(PROJECT_ID, LOCATION, product_set_id)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(product_id) in out

    remove_product_from_product_set(
        PROJECT_ID, LOCATION, product_id, product_set_id)
    list_products_in_product_set(PROJECT_ID, LOCATION, product_set_id)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(product_id) not in out


def test_purge_products_in_product_set(capsys, test_resources):
    product_set_id, product_id = test_resources
    add_product_to_product_set(
        PROJECT_ID, LOCATION, product_id, product_set_id)
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(product_id) in out

    purge_products_in_product_set(
        PROJECT_ID, LOCATION, product_set_id, force=True)

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(product_id) not in out
