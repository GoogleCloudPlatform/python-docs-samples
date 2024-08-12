# Copyright 2024 Google LLC
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
#

import os
from uuid import uuid4

from discoveryengine import (
    create_data_store_sample,
    delete_data_store_sample,
    get_data_store_sample,
    list_data_stores_sample,
)

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
data_store_id = f"test-data-store-{str(uuid4())}"


def test_create_data_store():
    operation_name = create_data_store_sample.create_data_store_sample(
        project_id, location, data_store_id
    )
    assert operation_name


def test_get_data_store():
    data_store = get_data_store_sample.get_data_store_sample(
        project_id, location, data_store_id
    )
    assert data_store


def test_list_data_stores():
    response = list_data_stores_sample.list_data_stores_sample(project_id, location)
    assert response


def test_delete_data_store():
    operation_name = delete_data_store_sample.delete_data_store_sample(
        project_id, location, data_store_id
    )
    assert operation_name
