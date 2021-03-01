"""
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
import main


def test_index() -> None:
    """
    GIVEN the app
    WHEN multiple requests to the / endpoint are made
    THEN check that most of them succeed
    """
    client = main.app.test_client()
    success_counter = 0
    for x in range(10):
        r = client.get("/")
        if r.status_code == 200:
            success_counter = success_counter + 1
    assert success_counter >= 5


def test_metrics() -> None:
    """
    GIVEN the app
    WHEN a request to the /metrics endpoint is made
    THEN check that it's a valid Prometheus endpoint
    """
    client = main.app.test_client()
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "HELP" in res.data.decode("utf-8")
