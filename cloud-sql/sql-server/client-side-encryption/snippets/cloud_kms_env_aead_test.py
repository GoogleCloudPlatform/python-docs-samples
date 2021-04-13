# Copyright 2021 Google LLC
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

import os

import pytest

from snippets.cloud_kms_env_aead import init_tink_env_aead


@pytest.fixture(name="kms_uri")
def setup() -> str:
    kms_uri = "gcp-kms://" + os.environ["CLOUD_KMS_KEY"]

    yield kms_uri


def test_cloud_kms_env_aead(
        capsys: pytest.CaptureFixture, kms_uri: str) -> None:
    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

    # Create env_aead primitive
    init_tink_env_aead(kms_uri, credentials)

    captured = capsys.readouterr().out
    assert f"Created envelope AEAD Primitive using KMS URI: {kms_uri}" in captured
