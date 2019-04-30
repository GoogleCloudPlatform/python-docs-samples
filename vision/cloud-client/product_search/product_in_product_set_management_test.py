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

from product_in_product_set_management import (
    add_product_to_product_set, list_products_in_product_set,
    remove_product_from_product_set)
from product_management import create_product, delete_product
from product_set_management import (
    create_product_set, delete_product_set)


PROJECT_ID = os.getenv('GCLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_SET_DISPLAY_NAME = 'fake_product_set_display_name_for_testing'
PRODUCT_SET_ID = 'fake_product_set_id_for_testing'

PRODUCT_DISPLAY_NAME = 'fake_product_display_name_for_testing'
PRODUCT_CATEGORY = 'homegoods'
PRODUCT_ID = 'fake_product_id_for_testing'


@pytest.fixture
def product_and_product_set():
    # set up
    create_product_set(
        PROJECT_ID, LOCATION, PRODUCT_SET_ID, PRODUCT_SET_DISPLAY_NAME)
    create_product(
        PROJECT_ID, LOCATION, PRODUCT_ID,
        PRODUCT_DISPLAY_NAME, PRODUCT_CATEGORY)

    yield None

    # tear down
    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)
    delete_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)


def test_add_product_to_product_set(capsys, product_and_product_set):
    list_products_in_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(PRODUCT_ID) not in out

    add_product_to_product_set(
        PROJECT_ID, LOCATION, PRODUCT_ID, PRODUCT_SET_ID)
    list_products_in_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(PRODUCT_ID) in out


def test_remove_product_from_product_set(capsys, product_and_product_set):
    add_product_to_product_set(
        PROJECT_ID, LOCATION, PRODUCT_ID, PRODUCT_SET_ID)
    list_products_in_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(PRODUCT_ID) in out

    remove_product_from_product_set(
        PROJECT_ID, LOCATION, PRODUCT_ID, PRODUCT_SET_ID)
    list_products_in_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    out, _ = capsys.readouterr()
    assert 'Product id: {}'.format(PRODUCT_ID) not in out
