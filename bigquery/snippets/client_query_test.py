# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

import client_query  # type: ignore

if typing.TYPE_CHECKING:
    import pytest


def test_client_query(capsys: "pytest.CaptureFixture[str]") -> None:
    client_query.client_query()
    out, _ = capsys.readouterr()
    assert "The query data:" in out
    assert "name=James, count=272793" in out


def test_client_query_job_optional(
    capsys: "pytest.CaptureFixture[str]", monkeypatch: "pytest.MonkeyPatch"
) -> None:
    monkeypatch.setenv("QUERY_PREVIEW_ENABLED", "true")

    client_query.client_query()
    out, _ = capsys.readouterr()
    assert "The query data:" in out
    assert "name=James, count=272793" in out
