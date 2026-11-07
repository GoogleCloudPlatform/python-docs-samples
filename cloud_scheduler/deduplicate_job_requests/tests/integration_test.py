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

"""Integration tests that run the handler against a real Firestore database.

These tests are skipped unless RUN_INTEGRATION_TESTS is "true". They need a
Firestore database in Native mode; set FIRESTORE_DATABASE to use a named
database instead of "(default)".
"""

import datetime
import hashlib
import os
from typing import Iterator
from unittest import mock
import uuid

import flask
from google.cloud import firestore
import pytest

from .. import main

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION_TESTS") != "true",
    reason="Set RUN_INTEGRATION_TESTS=true to run integration tests.",
)

app = flask.Flask(__name__)


def run_ref(headers: dict[str, str]) -> firestore.DocumentReference:
    """Returns the record that the handler keeps for a run."""
    key = (
        f"{headers['X-CloudScheduler-JobName']}/"
        f"{headers['X-CloudScheduler-ScheduleTime']}"
    )
    run_id = hashlib.sha256(key.encode()).hexdigest()
    return main.db.collection("scheduler_runs").document(run_id)


@pytest.fixture
def headers(monkeypatch: pytest.MonkeyPatch) -> Iterator[dict[str, str]]:
    """Uses a real database and a unique run, and deletes the run's record."""
    database = firestore.Client(
        database=os.environ.get("FIRESTORE_DATABASE", "(default)")
    )
    monkeypatch.setattr(main, "db", database)
    run_headers = {
        "X-CloudScheduler-JobName": f"test-job-{uuid.uuid4().hex[:12]}",
        "X-CloudScheduler-ScheduleTime": "2026-11-06T19:29:01.336893-08:00",
    }
    yield run_headers
    run_ref(run_headers).delete()


def call_function(headers: dict[str, str]) -> tuple[str, int]:
    with app.test_request_context("/", method="POST", headers=headers):
        return main.handle_scheduled_job(flask.request)


def test_duplicate_delivery_is_skipped(headers: dict[str, str]) -> None:
    assert call_function(headers) == ("Run processed", 200)
    assert call_function(headers) == ("Duplicate run skipped", 200)
    assert run_ref(headers).get().to_dict()["status"] == "completed"


def test_failed_work_releases_the_claim(headers: dict[str, str]) -> None:
    with mock.patch.object(main, "run_job_logic", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError):
            call_function(headers)

    assert not run_ref(headers).get().exists
    assert call_function(headers) == ("Run processed", 200)


def test_active_and_expired_leases(headers: dict[str, str]) -> None:
    now = datetime.datetime.now(datetime.timezone.utc)
    run_ref(headers).set({"status": "in_progress", "lease_expires": now + main.LEASE})
    assert call_function(headers) == ("Run in progress", 409)

    expired = now - datetime.timedelta(seconds=1)
    run_ref(headers).set({"status": "in_progress", "lease_expires": expired})
    assert call_function(headers) == ("Run processed", 200)
