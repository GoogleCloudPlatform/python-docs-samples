# Copyright 2015 Google Inc.
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

import webtest

import memcache


def test_memcache(testbed):
    app = webtest.TestApp(memcache.app)

    response = app.get("/memcache")
    assert response.status_int == 200
    assert "Global: 1" in response.body

    response = app.get("/memcache/a")
    assert response.status_int == 200
    assert "Global: 2" in response.body
    assert "a: 1" in response.body

    response = app.get("/memcache/b")
    assert response.status_int == 200
    assert "Global: 3" in response.body
    assert "b: 1" in response.body
