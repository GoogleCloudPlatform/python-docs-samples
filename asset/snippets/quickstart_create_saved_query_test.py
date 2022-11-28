#!/usr/bin/env python

# Copyright 2022 Google LLC.
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

import quickstart_create_saved_query


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
SAVED_QUERY_ID = f"saved-query-{uuid.uuid4().hex}"


def test_create_saved_query(capsys, saved_query_deleter):
    saved_query = quickstart_create_saved_query.create_saved_query(
        PROJECT, SAVED_QUERY_ID, "saved query foo")
    saved_query_deleter.append(saved_query.name)
    expected_resource_name_suffix = f"savedQueries/{SAVED_QUERY_ID}"
    assert saved_query.name.endswith(expected_resource_name_suffix)
