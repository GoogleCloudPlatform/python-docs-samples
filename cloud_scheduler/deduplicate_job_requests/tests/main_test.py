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
from typing import Any
from unittest import mock

import flask
import pytest

from .. import main

app = flask.Flask(__name__)

HEADERS = {
    "X-CloudScheduler-JobName": "test-job",
    "X-CloudScheduler-ScheduleTime": "2026-11-06T19:29:01.336893-08:00",
}


class FakeSnapshot:
    def __init__(self, data: dict[str, Any] | None) -> None:
        self._data = data
        self.exists = data is not None

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data or {})


class FakeDocument:
    """A Firestore document reference backed by a dictionary."""

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


@pytest.fixture(autouse=True)
def fake_db(monkeypatch: pytest.MonkeyPatch) -> FakeDatabase:
    database = FakeDatabase()
    monkeypatch.setattr(main, "db", database)
    return database


def call_function(headers: dict[str, str] | None = None) -> tuple[str, int]:
    with app.test_request_context("/", method="POST", headers=headers):
        return main.handle_scheduled_job(flask.request)


def only_record(fake_db: FakeDatabase) -> dict[str, Any]:
    assert len(fake_db.store) == 1
    return next(iter(fake_db.store.values()))


def test_first_delivery_runs_the_work(fake_db: FakeDatabase) -> None:
    with mock.patch.object(main, "run_job_logic") as run_job_logic:
        body, status = call_function(HEADERS)

    assert (body, status) == ("Run processed", 200)
    run_job_logic.assert_called_once()
    record = only_record(fake_db)
    assert record["status"] == "completed"
    assert record["expire_at"] > record["lease_expires"]


def test_duplicate_after_completion_is_skipped(fake_db: FakeDatabase) -> None:
    call_function(HEADERS)

    with mock.patch.object(main, "run_job_logic") as run_job_logic:
        body, status = call_function(HEADERS)

    assert (body, status) == ("Duplicate run skipped", 200)
    run_job_logic.assert_not_called()


def test_attempt_with_active_lease_returns_409(fake_db: FakeDatabase) -> None:
    with mock.patch.object(main, "run_job_logic", side_effect=lambda: None):
        # Simulate another attempt that holds the lease.
        future = datetime.datetime.now(datetime.timezone.utc) + main.LEASE
        call_function(HEADERS)
        record = only_record(fake_db)
        record.update(status="in_progress", lease_expires=future)

        body, status = call_function(HEADERS)

    assert (body, status) == ("Run in progress", 409)


def test_expired_lease_from_crashed_attempt_is_reclaimed(
    fake_db: FakeDatabase,
) -> None:
    call_function(HEADERS)
    past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=1)
    only_record(fake_db).update(status="in_progress", lease_expires=past)

    with mock.patch.object(main, "run_job_logic") as run_job_logic:
        body, status = call_function(HEADERS)

    assert (body, status) == ("Run processed", 200)
    run_job_logic.assert_called_once()
    assert only_record(fake_db)["status"] == "completed"


def test_failed_work_releases_the_claim(fake_db: FakeDatabase) -> None:
    with mock.patch.object(main, "run_job_logic", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError):
            call_function(HEADERS)

    assert fake_db.store == {}
    body, status = call_function(HEADERS)
    assert (body, status) == ("Run processed", 200)


def test_stale_attempt_does_not_release_newer_claim(fake_db: FakeDatabase) -> None:
    def slow_failing_work() -> None:
        # While this attempt runs, its lease expires and a retry claims the run.
        only_record(fake_db).update(attempt_id="newer-attempt")
        raise RuntimeError("boom")

    with mock.patch.object(main, "run_job_logic", side_effect=slow_failing_work):
        with pytest.raises(RuntimeError):
            call_function(HEADERS)

    record = only_record(fake_db)
    assert record["attempt_id"] == "newer-attempt"
    assert record["status"] == "in_progress"


def test_stale_attempt_does_not_complete_newer_claim(fake_db: FakeDatabase) -> None:
    def slow_work() -> None:
        only_record(fake_db).update(attempt_id="newer-attempt")

    with mock.patch.object(main, "run_job_logic", side_effect=slow_work):
        call_function(HEADERS)

    assert only_record(fake_db)["status"] == "in_progress"


def test_different_schedule_times_are_different_runs(fake_db: FakeDatabase) -> None:
    next_run = dict(
        HEADERS, **{"X-CloudScheduler-ScheduleTime": "2026-11-06T19:30:01-08:00"}
    )

    call_function(HEADERS)
    body, status = call_function(next_run)

    assert (body, status) == ("Run processed", 200)
    assert len(fake_db.store) == 2


def test_missing_scheduler_headers_are_rejected() -> None:
    body, status = call_function()

    assert status == 400
    assert body.startswith("error:")
