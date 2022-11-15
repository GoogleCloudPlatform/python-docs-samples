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

from product_set_management import (
    create_product_set, delete_product_set, list_product_sets)


PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = 'us-west1'

PRODUCT_SET_DISPLAY_NAME = 'fake_product_set_display_name_for_testing'
PRODUCT_SET_ID = 'test_{}'.format(uuid.uuid4())


@pytest.fixture(scope="function", autouse=True)
def setup():
    # set up
    create_product_set(
        PROJECT_ID, LOCATION, PRODUCT_SET_ID, PRODUCT_SET_DISPLAY_NAME)


def test_delete_product_set(capsys):
    list_product_sets(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_SET_ID in out

    delete_product_set(PROJECT_ID, LOCATION, PRODUCT_SET_ID)

    list_product_sets(PROJECT_ID, LOCATION)
    out, _ = capsys.readouterr()
    assert PRODUCT_SET_ID not in out
