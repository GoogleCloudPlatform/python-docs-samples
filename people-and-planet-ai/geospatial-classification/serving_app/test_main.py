# Copyright 2022 Google LLC
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

from __future__ import annotations

from collections.abc import Generator
import sys
import types

from flask.testing import FlaskClient
import pytest

import main


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    main.app.config.update(TESTING=True)
    with main.app.test_client() as test_client:
        yield test_client


def test_predict_uses_trusted_model_dir_from_environment(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[dict, str]] = []

    def fake_run(data: dict, model_dir: str) -> dict:
        calls.append((data, model_dir))
        return {"predictions": [[0.42]]}

    monkeypatch.setenv("MODEL_DIR", "gs://trusted-bucket/model_output")
    monkeypatch.setitem(sys.modules, "predict", types.SimpleNamespace(run=fake_run))

    response = client.post(
        "/predict",
        json={
            "bucket": "attacker-bucket/evil-prefix",
            "data": {
                "band_1": [[1, 2, 3]],
                "band_2": [[4, 5, 6]],
                "band_3": [[7, 8, 9]],
            },
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "method": "predict",
        "model_dir": "gs://trusted-bucket/model_output",
        "predictions": {"predictions": [[0.42]]},
    }
    assert calls == [
        (
            {
                "band_1": [[1, 2, 3]],
                "band_2": [[4, 5, 6]],
                "band_3": [[7, 8, 9]],
            },
            "gs://trusted-bucket/model_output",
        )
    ]


def test_predict_returns_error_when_trusted_model_dir_is_missing(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("MODEL_DIR", raising=False)
    monkeypatch.setitem(
        sys.modules,
        "predict",
        types.SimpleNamespace(run=lambda data, model_dir: {"predictions": [[0.42]]}),
    )

    response = client.post(
        "/predict",
        json={
            "bucket": "attacker-bucket/evil-prefix",
            "data": {
                "band_1": [[1, 2, 3]],
                "band_2": [[4, 5, 6]],
                "band_3": [[7, 8, 9]],
            },
        },
    )

    assert response.status_code == 500
    assert response.get_json() == {
        "error": "RuntimeError: MODEL_DIR must be set to a trusted model location."
    }
