# Copyright 2026 Google LLC
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

import functions_framework
import pytest
from spanner_remote_functions import remote_function_handler


def test_batch_add_sums_numbers_and_large_int64_strings() -> None:
    app = functions_framework.create_app(
        target="batch_add", source=remote_function_handler.__file__
    )
    client = app.test_client()
    large = "9007199254740993"
    response = client.post(
        "/",
        json={
            "requestId": "req-1",
            "calls": [
                [1, 2],
                [3, None, 4],
                [large, 2],
            ],
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {"replies": [3, 7, "9007199254740995"]}


@pytest.mark.parametrize(
    "json_body, expected_substr",
    [
        ({"requestId": "missing-calls"}, "'calls' list"),
        ({"calls": ["not-a-list"]}, "must be a list"),
        ({"calls": [["not-an-int", 2]]}, "Invalid integer argument"),
    ],
)
def test_batch_add_invalid_payloads_return_400(
    json_body: dict[str, object], expected_substr: str
) -> None:
    app = functions_framework.create_app(
        target="batch_add", source=remote_function_handler.__file__
    )
    client = app.test_client()
    response = client.post("/", json=json_body)

    assert response.status_code == 400
    payload = response.get_json()
    assert isinstance(payload, dict)
    assert expected_substr in str(payload.get("errorMessage", ""))
