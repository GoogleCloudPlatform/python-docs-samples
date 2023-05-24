# Copyright 2020 Google LLC
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

from product_management import create_product, delete_product, list_products


PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_DISPLAY_NAME = 'fake_product_display_name_for_testing'
PRODUCT_CATEGORY = 'homegoods'
PRODUCT_ID = f'test_{uuid.uuid4()}'


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # tear down
    delete_product(PROJECT_ID, LOCATION, PRODUCT_ID)


def test_create_product(capsys):
    create_product(
        PROJECT_ID, LOCATION, PRODUCT_ID,
        PRODUCT_DISPLAY_NAME, PRODUCT_CATEGORY)
    list_products(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_ID in out
