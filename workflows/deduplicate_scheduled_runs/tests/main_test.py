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

import datetime
import json
import os
import pathlib
import subprocess
import sys
from typing import Any
from unittest import mock

import flask
from google.api_core import exceptions
from google.cloud.workflows import executions_v1
import pytest

from .. import main

app = flask.Flask(__name__)
HEADERS = {
    "X-CloudScheduler-JobName": "test-job",
    "X-CloudScheduler-ScheduleTime": "2026-11-09T09:00:00.123456-08:00",
}
EXECUTION_NAME = "projects/p/locations/l/workflows/w/executions/e"


class FakeSnapshot:
    def __init__(self, data: dict[str, Any] | None) -> None:
        self._data = data
        self.exists = data is not None

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data or {})


class FakeDocument:
    def __init__(self, store: dict[str, dict[str, Any]], doc_id: str) -> None:
        self.store = store
        self.id = doc_id

    def get(self, transaction: object = None) -> FakeSnapshot:
        return FakeSnapshot(self.store.get(self.id))


class FakeDatabase:
    def __init__(self) -> None:
        self.store: dict[str, dict[str, Any]] = {}

    def collection(self, name: str) -> mock.MagicMock:
        collection = mock.MagicMock()
        collection.document.side_effect = lambda doc_id: FakeDocument(
            self.store, doc_id
        )
        return collection

    def transaction(self) -> mock.MagicMock:
        # firestore.transactional begins, commits, and retries the transaction.
        transaction = mock.MagicMock(_max_attempts=1, _id=b"test", _read_only=False)
        transaction.set.side_effect = lambda ref, data: self.store.__setitem__(
            ref.id, dict(data)
        )
        transaction.update.side_effect = lambda ref, data: self.store[ref.id].update(
            data
        )
        transaction.delete.side_effect = lambda ref: self.store.pop(ref.id, None)
        return transaction


@pytest.fixture
def db(monkeypatch: pytest.MonkeyPatch) -> FakeDatabase:
    database = FakeDatabase()
    monkeypatch.setattr(main, "db", database)
    return database


@pytest.fixture
def executions(monkeypatch: pytest.MonkeyPatch) -> mock.MagicMock:
    client = mock.MagicMock()
    client.create_execution.return_value = executions_v1.Execution(name=EXECUTION_NAME)
    monkeypatch.setattr(main, "executions_client", client)
    monkeypatch.setattr(main, "WORKFLOW_NAME", "projects/p/locations/l/workflows/w")
    return client


def call(headers: dict[str, str] | None = None) -> tuple[str, int]:
    with app.test_request_context("/", method="POST", headers=headers):
        return main.start_scheduled_run(flask.request)


def only_record(db: FakeDatabase) -> dict[str, Any]:
    assert len(db.store) == 1
    return next(iter(db.store.values()))


def test_first_delivery_starts_the_workflow(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    body, status = call(HEADERS)

    assert status == 200
    kwargs = executions.create_execution.call_args.kwargs
    assert kwargs["parent"] == "projects/p/locations/l/workflows/w"
    assert json.loads(kwargs["execution"].argument) == {
        "job_name": "test-job",
        "scheduled_minute": "2026-11-09T17:00Z",
    }
    record = only_record(db)
    assert record["status"] == "completed"
    assert record["execution_name"] == EXECUTION_NAME


def test_duplicate_delivery_is_skipped(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    call(HEADERS)

    body, status = call(HEADERS)

    assert (body, status) == ("Duplicate run skipped", 200)
    executions.create_execution.assert_called_once()


def test_schedule_time_with_and_without_offset_is_one_run(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    # A forced run before the job's first scheduled run sends the time without
    # Scheduler's per-job offset; later deliveries include it.
    call(
        dict(HEADERS, **{"X-CloudScheduler-ScheduleTime": "2026-11-09T09:00:00-08:00"})
    )

    body, status = call(HEADERS)

    assert (body, status) == ("Duplicate run skipped", 200)
    executions.create_execution.assert_called_once()


def test_invalid_schedule_time_is_rejected(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    body, status = call(dict(HEADERS, **{"X-CloudScheduler-ScheduleTime": "soon"}))

    assert status == 400
    executions.create_execution.assert_not_called()


def test_delivery_with_active_claim_returns_409(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    call(HEADERS)
    future = datetime.datetime.now(datetime.timezone.utc) + main.LEASE
    only_record(db).update(status="in_progress", lease_expires=future)

    _, status = call(HEADERS)

    assert status == 409
    executions.create_execution.assert_called_once()


def test_failed_start_releases_the_claim(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    executions.create_execution.side_effect = exceptions.ServiceUnavailable("down")

    with pytest.raises(exceptions.ServiceUnavailable):
        call(HEADERS)

    assert db.store == {}


def test_stale_attempt_does_not_complete_newer_claim(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    def slow_start(**kwargs: object) -> executions_v1.Execution:
        # While this attempt runs, its lease expires and a retry claims the run.
        only_record(db).update(attempt_id="newer-attempt")
        return executions_v1.Execution(name=EXECUTION_NAME)

    executions.create_execution.side_effect = slow_start

    call(HEADERS)

    assert only_record(db)["status"] == "in_progress"


def test_missing_headers_are_rejected(
    db: FakeDatabase, executions: mock.MagicMock
) -> None:
    body, status = call()

    assert status == 400
    assert body.startswith("error:")
    executions.create_execution.assert_not_called()


def test_function_requires_workflow_name() -> None:
    env = {k: v for k, v in os.environ.items() if k != "WORKFLOW_NAME"}
    result = subprocess.run(
        [sys.executable, "-c", "import main"],
        cwd=pathlib.Path(main.__file__).parent,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "KeyError: 'WORKFLOW_NAME'" in result.stderr


def test_rollback_failure_preserves_original_execution_error(
    db: FakeDatabase, executions: mock.MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    executions.create_execution.side_effect = exceptions.ServiceUnavailable(
        "workflows down"
    )
    monkeypatch.setattr(
        main, "finish_run", mock.MagicMock(side_effect=exceptions.Aborted("db busy"))
    )

    with pytest.raises(exceptions.ServiceUnavailable, match="workflows down"):
        call(HEADERS)
