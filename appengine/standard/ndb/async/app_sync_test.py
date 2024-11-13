# Copyright 2016 Google Inc.
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

import pytest
import webtest

import app_sync


@pytest.fixture
def app(testbed):
    return webtest.TestApp(app_sync.app)


def test_main(app, testbed, login):
    app_sync.Account(id="123", view_counter=4).put()

    # Log the user in
    login(id="123")

    response = app.get("/")

    assert response.status_int == 200
    account = app_sync.Account.get_by_id("123")
    assert account.view_counter == 5
