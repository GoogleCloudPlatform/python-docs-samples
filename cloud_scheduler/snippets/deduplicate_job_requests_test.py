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
from typing import Iterator
from unittest import mock
import uuid

import flask
import pytest

import deduplicate_job_requests

SCHEDULE_TIME_UTC = "2026-10-16T12:00:00Z"
SCHEDULE_TIME_OFFSET = "2026-10-16T05:00:00-07:00"


@pytest.fixture
def app() -> flask.Flask:
    return flask.Flask(__name__)


@pytest.fixture
def job_name() -> Iterator[str]:
    name = f"test-job-{uuid.uuid4().hex[:12]}"
    yield name
    dedup_key = f"{name}:{SCHEDULE_TIME_UTC}"
    deduplicate_job_requests.db.collection("scheduler_dedup").document(
        dedup_key
    ).delete()


def test_missing_or_invalid_headers(app: flask.Flask) -> None:
    with app.test_request_context("/"):
        body, status = deduplicate_job_requests.handle_scheduled_job(
            flask.request
        )
        assert status == 400
        assert "Missing" in body

    with app.test_request_context(
        "/",
        headers={
            "X-CloudScheduler-JobName": "../invalid/job",
            "X-CloudScheduler-ScheduleTime": SCHEDULE_TIME_UTC,
        },
    ):
        body, status = deduplicate_job_requests.handle_scheduled_job(
            flask.request
        )
        assert status == 400
        assert "Invalid X-CloudScheduler-JobName" in body

    with app.test_request_context(
        "/",
        headers={
            "X-CloudScheduler-JobName": "valid-job",
            "X-CloudScheduler-ScheduleTime": "2026-10-16T12:00:00",
        },
    ):
        body, status = deduplicate_job_requests.handle_scheduled_job(
            flask.request
        )
        assert status == 400
        assert "timezone" in body


def test_first_and_duplicate_completed_request(
    app: flask.Flask, job_name: str
) -> None:
    # First attempt succeeds and marks the record COMPLETED.
    with app.test_request_context(
        "/",
        headers={
            "X-CloudScheduler-JobName": job_name,
            "X-CloudScheduler-ScheduleTime": SCHEDULE_TIME_UTC,
        },
    ):
        body, status = deduplicate_job_requests.handle_scheduled_job(
            flask.request
        )
        assert status == 200
        assert body == "Job completed"

    # Retried attempt with an equivalent RFC 3339 offset maps to the same UTC
    # key and is ignored with 200 OK.
    with app.test_request_context(
        "/",
        headers={
            "X-CloudScheduler-JobName": job_name,
            "X-CloudScheduler-ScheduleTime": SCHEDULE_TIME_OFFSET,
        },
    ):
        body, status = deduplicate_job_requests.handle_scheduled_job(
            flask.request
        )
        assert status == 200
        assert body == "Duplicate job request ignored"


def test_in_progress_request_returns_409(
    app: flask.Flask, job_name: str
) -> None:
    dedup_key = f"{job_name}:{SCHEDULE_TIME_UTC}"
    now = datetime.datetime.now(datetime.timezone.utc)
    deduplicate_job_requests.db.collection("scheduler_dedup").document(
        dedup_key
    ).create(
        {
            "job_name": job_name,
            "schedule_time": SCHEDULE_TIME_UTC,
            "status": "IN_PROGRESS",
            "created_at": now,
            "expires_at": now + deduplicate_job_requests.LOCK_TTL,
        }
    )

    with app.test_request_context(
        "/",
        headers={
            "X-CloudScheduler-JobName": job_name,
            "X-CloudScheduler-ScheduleTime": SCHEDULE_TIME_UTC,
        },
    ):
        body, status = deduplicate_job_requests.handle_scheduled_job(
            flask.request
        )
        assert status == 409
        assert body == "Job execution already in progress"


def test_failed_execution_releases_lock_for_retry(
    app: flask.Flask, job_name: str
) -> None:
    headers = {
        "X-CloudScheduler-JobName": job_name,
        "X-CloudScheduler-ScheduleTime": SCHEDULE_TIME_UTC,
    }

    # If run_job_logic raises an exception, the lock document is deleted.
    with mock.patch.object(
        deduplicate_job_requests,
        "run_job_logic",
        side_effect=RuntimeError("Transient failure"),
    ):
        with app.test_request_context("/", headers=headers):
            with pytest.raises(RuntimeError, match="Transient failure"):
                deduplicate_job_requests.handle_scheduled_job(flask.request)

    # A subsequent retry can acquire the lock and complete the job.
    with app.test_request_context("/", headers=headers):
        body, status = deduplicate_job_requests.handle_scheduled_job(
            flask.request
        )
        assert status == 200
        assert body == "Job completed"
