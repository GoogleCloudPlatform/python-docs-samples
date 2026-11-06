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

from unittest import mock

import flask
import pytest

from .. import main

app = flask.Flask(__name__)

HEADERS = {
    "X-CloudScheduler-JobName": "test-job",
    "X-CloudScheduler-ScheduleTime": "2026-11-06T09:00:00Z",
}


@pytest.fixture(autouse=True)
def reset_claimed_runs() -> None:
    """Gives each test an empty set of claimed runs."""
    main.claimed_runs.clear()


def call_function(
    headers: dict[str, str] | None = None, data: str = "example-payload"
) -> tuple[str, int]:
    with app.test_request_context("/", method="POST", headers=headers, data=data):
        return main.handle_scheduled_run(flask.request)


def test_first_delivery_is_processed(capsys: pytest.CaptureFixture[str]) -> None:
    body, status = call_function(HEADERS)

    assert status == 200
    assert body == "Run processed"
    assert "example-payload" in capsys.readouterr().out


def test_duplicate_delivery_is_skipped(capsys: pytest.CaptureFixture[str]) -> None:
    call_function(HEADERS)

    body, status = call_function(HEADERS)

    assert status == 200
    assert body == "Duplicate run skipped"
    assert "Skipped duplicate run" in capsys.readouterr().out


def test_failed_run_releases_claim_for_retry() -> None:
    with mock.patch.object(main, "process_run", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError):
            call_function(HEADERS)

    body, status = call_function(HEADERS)

    assert status == 200
    assert body == "Run processed"


def test_missing_scheduler_headers_are_rejected() -> None:
    body, status = call_function()

    assert status == 400
    assert body.startswith("error:")
