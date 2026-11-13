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

from typing import Any
from unittest import mock

import flask
import pytest

from .. import main

app = flask.Flask(__name__)


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

    def delete(self) -> None:
        self.store.pop(self.id, None)


class FakeDatabase:
    def __init__(self) -> None:
        self.collections: dict[str, dict[str, dict[str, Any]]] = {}

    def collection(self, name: str) -> mock.MagicMock:
        store = self.collections.setdefault(name, {})
        collection = mock.MagicMock()
        collection.document.side_effect = lambda doc_id: FakeDocument(store, doc_id)
        return collection

    def transaction(self) -> mock.MagicMock:
        transaction = mock.MagicMock(_max_attempts=1, _id=b"test", _read_only=False)
        transaction.set.side_effect = lambda ref, data: ref.store.__setitem__(
            ref.id, dict(data)
        )

        def update(ref: FakeDocument, data: dict[str, Any]) -> None:
            record = ref.store[ref.id]
            for key, value in data.items():
                if hasattr(value, "value"):
                    record[key] = record.get(key, 0) + value.value
                else:
                    record[key] = value

        transaction.update.side_effect = update
        return transaction


@pytest.fixture
def db(monkeypatch: pytest.MonkeyPatch) -> FakeDatabase:
    database = FakeDatabase()
    monkeypatch.setattr(main, "db", database)
    monkeypatch.setattr(
        main, "charges", database.collection("payment_provider_charges")
    )
    return database


def post(
    path: str,
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[dict[str, Any], int]:
    with app.test_request_context(path, method="POST", json=body, headers=headers):
        return main.payment_provider(flask.request)


def test_charges_once_per_idempotency_key(db: FakeDatabase) -> None:
    headers = {"Idempotency-Key": "order-1"}
    first, status1 = post(
        "/charges", {"order_id": "order-1", "amount_cents": 500}, headers
    )
    second, status2 = post(
        "/charges", {"order_id": "order-1", "amount_cents": 500}, headers
    )

    assert (status1, status2) == (200, 200)
    assert first["charge_id"] == second["charge_id"]
    assert db.collections["payment_provider_charges"]["order-1"]["requests"] == 2


def test_refund_reverses_existing_charge_once(db: FakeDatabase) -> None:
    post(
        "/charges",
        {"order_id": "order-1", "amount_cents": 500},
        {"Idempotency-Key": "order-1"},
    )

    first, status1 = post("/refunds", {"charge_key": "order-1"})
    second, status2 = post("/refunds", {"charge_key": "order-1"})

    assert (status1, first["refunded"]) == (200, True)
    assert (status2, second["refunded"]) == (200, True)
    assert db.collections["payment_provider_charges"]["order-1"]["status"] == "refunded"


def test_refund_before_charge_voids_the_key(db: FakeDatabase) -> None:
    refund_body, refund_status = post("/refunds", {"charge_key": "order-2"})
    _, charge_status = post(
        "/charges",
        {"order_id": "order-2", "amount_cents": 500},
        {"Idempotency-Key": "order-2"},
    )

    assert (refund_status, refund_body["refunded"]) == (200, False)
    assert charge_status == 409


def test_simulated_fault_runs_once_after_charging(db: FakeDatabase) -> None:
    db.collection("payment_provider_faults").store = {}
    db.collections["payment_provider_faults"]["order-3"] = {"mode": "fail_after_charge"}
    headers = {"Idempotency-Key": "order-3"}

    _, first_status = post(
        "/charges", {"order_id": "order-3", "amount_cents": 500}, headers
    )
    _, retry_status = post(
        "/charges", {"order_id": "order-3", "amount_cents": 500}, headers
    )

    assert (first_status, retry_status) == (504, 200)
    assert db.collections["payment_provider_charges"]["order-3"]["status"] == "charged"


@pytest.mark.parametrize("path, body", [("/charges", {}), ("/refunds", {})])
def test_missing_keys_are_rejected(
    db: FakeDatabase, path: str, body: dict[str, Any]
) -> None:
    _, status = post(path, body)

    assert status == 400
