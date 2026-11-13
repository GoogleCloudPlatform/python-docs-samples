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
import os
import pathlib
import subprocess
import sys
from typing import Any
from unittest import mock

import flask
from google.api_core import exceptions
import pytest
import requests

from .. import main

app = flask.Flask(__name__)
ORDER_ID = "order-2001"
NOW = datetime.datetime.now(datetime.timezone.utc)


class FakeSnapshot:
    def __init__(self, data: dict[str, Any] | None) -> None:
        self._data = data
        self.exists = data is not None

    def to_dict(self) -> dict[str, Any] | None:
        return None if self._data is None else dict(self._data)


class FakeDocument:
    def __init__(self, store: dict[str, dict[str, Any]], doc_id: str) -> None:
        self.store = store
        self.id = doc_id

    def get(self, transaction: object = None) -> FakeSnapshot:
        return FakeSnapshot(self.store.get(self.id))


class FakeDatabase:
    """An in-memory stand-in for the orders collection."""

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
        transaction.update.side_effect = lambda ref, data: self.store[ref.id].update(
            data
        )
        return transaction


@pytest.fixture
def db(monkeypatch: pytest.MonkeyPatch) -> FakeDatabase:
    database = FakeDatabase()
    monkeypatch.setattr(main, "db", database)
    return database


@pytest.fixture
def refund(monkeypatch: pytest.MonkeyPatch) -> mock.MagicMock:
    refund_mock = mock.MagicMock(return_value=True)
    monkeypatch.setattr(main, "refund", refund_mock)
    return refund_mock


def create_order(db: FakeDatabase, **fields: object) -> dict[str, Any]:
    db.store[ORDER_ID] = {"order_state": "paid", "amount_cents": 4999, **fields}
    return db.store[ORDER_ID]


def call(body: dict[str, Any] | None = None) -> tuple[dict, int]:
    body = {"order_id": ORDER_ID} if body is None else body
    with app.test_request_context("/", method="POST", json=body):
        return main.refund_order(flask.request)


def test_paid_order_is_refunded_once(db: FakeDatabase, refund: mock.MagicMock) -> None:
    order = create_order(db)

    body, status = call()

    assert (status, body["status"], body["already_processed"]) == (
        200,
        "refunded",
        False,
    )
    refund.assert_called_once_with(ORDER_ID)
    assert order["order_state"] == "refunded"


@pytest.mark.parametrize("state", ["refunded", "cancelled"])
def test_finished_order_is_not_refunded_again(
    db: FakeDatabase, refund: mock.MagicMock, state: str
) -> None:
    create_order(db, order_state=state)

    body, status = call()

    assert (status, body["status"], body["already_processed"]) == (200, state, True)
    refund.assert_not_called()


@pytest.mark.parametrize("state", ["payment_in_progress", "refund_in_progress"])
def test_order_with_active_claim_returns_503(
    db: FakeDatabase, refund: mock.MagicMock, state: str
) -> None:
    create_order(
        db,
        order_state=state,
        attempt_id="other-attempt",
        lease_expires=NOW + main.LEASE,
    )

    _, status = call()

    assert status == 503
    refund.assert_not_called()


@pytest.mark.parametrize(
    "fields",
    [
        {
            "order_state": "refund_in_progress",
            "attempt_id": "crashed-attempt",
            "lease_expires": NOW - datetime.timedelta(seconds=1),
        },
        {"order_state": "refund_failed"},
    ],
    ids=["expired_claim", "failed_refund"],
)
def test_unfinished_refund_is_retried(
    db: FakeDatabase, refund: mock.MagicMock, fields: dict[str, Any]
) -> None:
    order = create_order(db, **fields)

    _, status = call()

    assert status == 200
    refund.assert_called_once()
    assert order["order_state"] == "refunded"


@pytest.mark.parametrize(
    "fields",
    [
        {"order_state": "payment_failed"},
        {
            "order_state": "payment_in_progress",
            "attempt_id": "crashed-attempt",
            "lease_expires": NOW - datetime.timedelta(seconds=1),
        },
    ],
    ids=["failed_payment", "expired_payment_claim"],
)
def test_uncertain_charge_is_refunded_if_it_happened(
    db: FakeDatabase, refund: mock.MagicMock, fields: dict[str, Any]
) -> None:
    order = create_order(db, **fields)
    # The provider reports whether the charge had gone through.
    refund.return_value = False

    body, status = call()

    assert (status, body["status"]) == (200, "cancelled")
    refund.assert_called_once_with(ORDER_ID)
    assert order["order_state"] == "cancelled"


def test_uncharged_order_is_cancelled_without_a_refund(
    db: FakeDatabase, refund: mock.MagicMock
) -> None:
    order = create_order(db, order_state="created")

    body, status = call()

    assert (status, body["status"]) == (200, "cancelled")
    refund.assert_not_called()
    assert order["order_state"] == "cancelled"


def test_ambiguous_refund_failure_is_retryable(
    db: FakeDatabase, refund: mock.MagicMock
) -> None:
    order = create_order(db)
    refund.side_effect = requests.Timeout("timed out")

    _, status = call()

    assert status == 503
    assert order["order_state"] == "refund_failed"


def test_stale_attempt_does_not_overwrite_newer_claim(
    db: FakeDatabase, refund: mock.MagicMock
) -> None:
    order = create_order(db)
    refund.side_effect = lambda *args: order.update(attempt_id="newer-attempt")

    call()

    assert order["order_state"] == "refund_in_progress"


@pytest.mark.parametrize(
    "body, expected_status",
    [({}, 400), ({"order_id": "missing-order"}, 404)],
)
def test_bad_requests(
    db: FakeDatabase,
    refund: mock.MagicMock,
    body: dict[str, Any],
    expected_status: int,
) -> None:
    _, status = call(body)

    assert status == expected_status
    refund.assert_not_called()


def contention_error() -> ValueError:
    """Builds the error Firestore raises when a transaction runs out of attempts."""
    try:
        raise ValueError("Failed to commit transaction") from exceptions.Aborted("busy")
    except ValueError as err:
        return err


def test_temporary_database_error_returns_503(
    db: FakeDatabase, refund: mock.MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    create_order(db)
    error = contention_error()
    monkeypatch.setattr(main, "claim_refund", mock.MagicMock(side_effect=error))

    _, status = call()

    assert status == 503
    refund.assert_not_called()


def test_permanent_database_error_is_not_retried(
    db: FakeDatabase, refund: mock.MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    create_order(db)
    error = exceptions.PermissionDenied("missing roles/datastore.user")
    monkeypatch.setattr(main, "claim_refund", mock.MagicMock(side_effect=error))

    with pytest.raises(exceptions.PermissionDenied):
        call()


def test_refund_is_keyed_by_the_charge(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "PAYMENT_PROVIDER_URL", "https://payments.example.com")
    monkeypatch.setattr(main.id_token, "fetch_id_token", lambda *args: "token")
    post = mock.MagicMock()
    post.return_value.json.return_value = {"refunded": True}
    monkeypatch.setattr(main.requests, "post", post)

    assert main.refund(ORDER_ID) is True

    assert post.call_args.args == ("https://payments.example.com/refunds",)
    assert post.call_args.kwargs["json"] == {"charge_key": ORDER_ID}
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer token"


def test_function_requires_payment_provider_url() -> None:
    env = {k: v for k, v in os.environ.items() if k != "PAYMENT_PROVIDER_URL"}
    result = subprocess.run(
        [sys.executable, "-c", "import main"],
        cwd=pathlib.Path(main.__file__).parent,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "KeyError: 'PAYMENT_PROVIDER_URL'" in result.stderr
