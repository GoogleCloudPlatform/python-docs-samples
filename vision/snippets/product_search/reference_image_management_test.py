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

from product_management import create_product, delete_product
from reference_image_management import (
    create_reference_image, delete_reference_image, list_reference_images)


PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_DISPLAY_NAME = 'fake_product_display_name_for_testing'
PRODUCT_CATEGORY = 'homegoods'
PRODUCT_ID = 'test_{}'.format(uuid.uuid4())

REFERENCE_IMAGE_ID = 'fake_reference_image_id_for_testing'
GCS_URI = 'gs://cloud-samples-data/vision/product_search/shoes_1.jpg'


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # set up
    create_product(
        PROJECT_ID, LOCATION, PRODUCT_ID,
        PRODUCT_DISPLAY_NAME, PRODUCT_CATEGORY)

    yield None

    # tear down
    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)


def test_create_reference_image(capsys):
    create_reference_image(
        PROJECT_ID, LOCATION, PRODUCT_ID, REFERENCE_IMAGE_ID,
        GCS_URI)
    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID)
    out, _ = capsys.readouterr()
    assert REFERENCE_IMAGE_ID in out


def test_delete_reference_image(capsys):
    create_reference_image(
        PROJECT_ID, LOCATION, PRODUCT_ID, REFERENCE_IMAGE_ID,
        GCS_URI)
    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID)
    out, _ = capsys.readouterr()
    assert REFERENCE_IMAGE_ID in out

    delete_reference_image(
        PROJECT_ID, LOCATION, PRODUCT_ID, REFERENCE_IMAGE_ID)
    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID)
    out, _ = capsys.readouterr()
    assert REFERENCE_IMAGE_ID not in out
