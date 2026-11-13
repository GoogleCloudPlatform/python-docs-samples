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


def make_db(fault_orders: set[str]) -> mock.MagicMock:
    database = mock.MagicMock()

    def document(doc_id: str) -> mock.MagicMock:
        doc = mock.MagicMock()
        doc.get.return_value.exists = doc_id in fault_orders
        return doc

    database.collection.return_value.document.side_effect = document
    return database


def call(body: dict[str, Any] | None) -> tuple[dict[str, Any], int]:
    with app.test_request_context("/", method="POST", json=body):
        return main.fulfill(flask.request)


def test_order_is_fulfilled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "db", make_db(set()))

    body, status = call({"order_id": "order-1"})

    assert (status, body["status"]) == (200, "fulfilled")


def test_simulated_fault_fails_permanently(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "db", make_db({"order-1"}))

    _, status = call({"order_id": "order-1"})

    assert status == 422


def test_missing_order_id_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "db", make_db(set()))

    _, status = call({})

    assert status == 400
