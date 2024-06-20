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
    create_engine_sample,
    delete_data_store_sample,
    delete_engine_sample,
    get_engine_sample,
    list_engines_sample,
)

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
engine_id = f"test-engine-{str(uuid4())}"
data_store_id = f"test-data-store-{str(uuid4())}"


def test_create_engine():
    create_data_store_sample.create_data_store_sample(
        project_id, location, data_store_id
    )
    operation_name = create_engine_sample.create_engine_sample(
        project_id, location, engine_id, data_store_ids=[data_store_id]
    )
    assert operation_name, operation_name


def test_get_engine():
    engine = get_engine_sample.get_engine_sample(project_id, location, engine_id)
    assert engine.name, engine.name


def test_list_engines():
    response = list_engines_sample.list_engines_sample(
        project_id,
        location,
    )
    assert response.engines, response.engines


def test_delete_engine():
    operation_name = delete_engine_sample.delete_engine_sample(
        project_id, location, engine_id
    )
    assert operation_name, operation_name
    delete_data_store_sample.delete_data_store_sample(
        project_id, location, data_store_id
    )
