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
from typing import Any

import google.auth

import authenticate_service_account

if typing.TYPE_CHECKING:
    import pytest


def mock_credentials(*args: Any, **kwargs: Any) -> google.auth.credentials.Credentials:
    credentials, _ = google.auth.default(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    return credentials


def test_main(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.setattr(
        "google.oauth2.service_account.Credentials.from_service_account_file",
        mock_credentials,
    )
    client = authenticate_service_account.main()
    assert client is not None
