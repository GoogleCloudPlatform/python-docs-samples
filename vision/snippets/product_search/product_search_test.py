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

import pytest

from product_search import get_similar_products_file, get_similar_products_uri


PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_SET_ID = 'indexed_product_set_id_for_testing'
PRODUCT_CATEGORY = 'apparel'
PRODUCT_ID_1 = 'indexed_product_id_for_testing_1'
PRODUCT_ID_2 = 'indexed_product_id_for_testing_2'

FILE_PATH_1 = 'resources/shoes_1.jpg'
IMAGE_URI_1 = 'gs://cloud-samples-data/vision/product_search/shoes_1.jpg'
FILTER = 'style=womens'
MAX_RESULTS = 6


@pytest.mark.flaky(max_runs=5, min_passes=1)
def test_get_similar_products_file(capsys):
    get_similar_products_file(
        PROJECT_ID, LOCATION, PRODUCT_SET_ID, PRODUCT_CATEGORY, FILE_PATH_1,
        '', MAX_RESULTS)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out
    assert PRODUCT_ID_2 in out


def test_get_similar_products_uri(capsys):
    get_similar_products_uri(
        PROJECT_ID, LOCATION, PRODUCT_SET_ID, PRODUCT_CATEGORY, IMAGE_URI_1,
        '')
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out
    assert PRODUCT_ID_2 in out


def test_get_similar_products_file_with_filter(capsys):
    get_similar_products_file(
        PROJECT_ID, LOCATION, PRODUCT_SET_ID, PRODUCT_CATEGORY, FILE_PATH_1,
        FILTER, MAX_RESULTS)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out
    assert PRODUCT_ID_2 not in out


def test_get_similar_products_uri_with_filter(capsys):
    get_similar_products_uri(
        PROJECT_ID, LOCATION, PRODUCT_SET_ID, PRODUCT_CATEGORY, IMAGE_URI_1,
        FILTER)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out
    assert PRODUCT_ID_2 not in out
