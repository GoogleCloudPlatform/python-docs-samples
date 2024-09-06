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

from google.cloud import discoveryengine_v1 as discoveryengine

import pytest

from discoveryengine import session_sample


project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
data_store_id = f"test-data-store-{uuid4()}"
user_pseudo_id = f"test-{uuid4()}"


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    # Create a data store
    # -----------------
    session_sample.create_session(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        user_pseudo_id=user_pseudo_id,
    )
    yield
    # Delete the data store
    # ---------------------


def test_create_session():
    response = session_sample.create_session(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        user_pseudo_id=user_pseudo_id,
    )

    assert response
    assert response.user_pseudo_id == user_pseudo_id


def test_delete_session():
    response = session_sample.create_session(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        user_pseudo_id=user_pseudo_id,
    )
    session_id = response.name.split("/")[-1]

    session_sample.delete_session(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        session_id=session_id,
    )


def test_update_session():
    response = session_sample.create_session(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        user_pseudo_id=user_pseudo_id,
    )
    session_id = response.name.split("/")[-1]

    response = session_sample.update_session(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        session_id=session_id,
        new_state=discoveryengine.Session.State.COMPLETED,
    )

    assert response
    assert response.state == discoveryengine.Session.State.COMPLETED


def test_list_sessions():
    response = session_sample.list_sessions(
        project_id=project_id, location=location, data_store_id=data_store_id
    )
    assert response.sessions


def test_list_sessions_with_filter():
    response = session_sample.list_sessions_with_filter(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        user_pseudo_id=user_pseudo_id,
    )
    assert response.sessions
