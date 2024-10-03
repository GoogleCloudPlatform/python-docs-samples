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

from discoveryengine import session_sample

import pytest

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
engine_id = "test-unstructured-engine_1697471976692"
user_pseudo_id = f"test-{uuid4()}"


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    session = session_sample.create_session(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
        user_pseudo_id=user_pseudo_id,
    )
    yield session

    session_id = session.name.split("/")[-1]
    session_sample.delete_session(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
        session_id=session_id,
    )


def test_create_session(setup_teardown):
    session = setup_teardown

    assert session
    assert session.user_pseudo_id == user_pseudo_id


def test_get_session(setup_teardown):
    session = setup_teardown

    session_id = session.name.split("/")[-1]

    response = session_sample.get_session(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
        session_id=session_id,
    )
    assert response


def test_update_session(setup_teardown):
    session = setup_teardown
    session_id = session.name.split("/")[-1]

    response = session_sample.update_session(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
        session_id=session_id,
    )
    assert response


def test_list_sessions():
    response = session_sample.list_sessions(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
    )
    assert response.sessions
