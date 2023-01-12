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

from google.cloud import storage
import pytest

from import_product_sets import import_product_sets
from product_in_product_set_management import list_products_in_product_set
from product_management import delete_product, list_products
from product_set_management import delete_product_set, list_product_sets
from reference_image_management import list_reference_images


PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = 'us-west1'

FILENAME = uuid.uuid4()
GCS_URI = 'gs://{}/vision/{}.csv'.format(PROJECT_ID, FILENAME)
PRODUCT_SET_DISPLAY_NAME = 'fake_product_set_display_name_for_testing'
PRODUCT_SET_ID = 'test_{}'.format(uuid.uuid4())
PRODUCT_ID_1 = 'test_{}'.format(uuid.uuid4())
IMAGE_URI_1 = 'shoes_1.jpg'


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # Create the product set csv file locally and upload it to GCS
    # This is so that there is a unique product set ID for all python version
    # tests.
    client = storage.Client(project=PROJECT_ID)
    bucket = client.get_bucket(PROJECT_ID)
    blob = storage.Blob("vision/{}.csv".format(FILENAME), bucket)
    blob.upload_from_string(
        '"gs://cloud-samples-data/vision/product_search/shoes_1.jpg",' +
        '"{}",'.format(IMAGE_URI_1) +
        '"{}",'.format(PRODUCT_SET_ID) +
        '"{}",'.format(PRODUCT_ID_1) +
        '"apparel",,"style=womens","0.1,0.1,0.9,0.1,0.9,0.9,0.1,0.9"')

    yield

    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID_1)
    delete_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    # Delete the created file
    blob.delete(client)


def test_import_product_sets(capsys):
    import_product_sets(PROJECT_ID, LOCATION, GCS_URI)

    list_product_sets(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_SET_ID in out

    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out

    list_products_in_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID_1 in out

    list_reference_images(PROJECT_ID, LOCATION, PRODUCT_ID_1)
    out, _ = capsys.readouterr()
    assert IMAGE_URI_1 in out
