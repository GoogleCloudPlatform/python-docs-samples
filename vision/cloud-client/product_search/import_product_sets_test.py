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

from import_product_sets import import_product_sets
from product_in_product_set_management import list_products_in_product_set
from product_management import delete_product, list_products
from product_set_management import delete_product_set, list_product_sets
from reference_image_management import list_reference_images


PROJECT_ID = os.getenv('GCLOUD_PROJECT')
LOCATION = 'us-west1'

GCS_URI = 'gs://python-docs-samples-tests/product_search/product_sets.csv'
PRODUCT_SET_DISPLAY_NAME = 'fake_product_set_display_name_for_testing'
PRODUCT_SET_ID = 'fake_product_set_id_for_testing'
PRODUCT_ID_1 = 'fake_product_id_for_testing_1'
PRODUCT_ID_2 = 'fake_product_id_for_testing_2'
IMAGE_URI_1 = 'shoes_1.jpg'
IMAGE_URI_2 = 'shoes_2.jpg'


@pytest.fixture
def teardown():
    # no set up, tear down only
    yield None

    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID_1)
    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID_2)
    delete_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)


def test_import_product_sets(capsys, teardown):
    list_product_sets(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_SET_ID not in out

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 not in out
    assert PRODUCT_ID_2 not in out

    list_products_in_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 not in out
    assert PRODUCT_ID_2 not in out

    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID_1)
    out, _ = capsys.readouterr()
    assert IMAGE_URI_1 not in out

    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID_2)
    out, _ = capsys.readouterr()
    assert IMAGE_URI_2 not in out

    import_product_sets(PROJECT_ID, LOCATION, GCS_URI)

    list_product_sets(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_SET_ID in out

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out
    assert PRODUCT_ID_2 in out

    list_products_in_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out
    assert PRODUCT_ID_2 in out

    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID_1)
    out, _ = capsys.readouterr()
    assert IMAGE_URI_1 in out

    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID_2)
    out, _ = capsys.readouterr()
    assert IMAGE_URI_2 in out
