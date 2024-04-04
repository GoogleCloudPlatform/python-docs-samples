# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import storage

import pytest

import quickstart


def test_storage_control_quickstart(
    capsys: pytest.LogCaptureFixture, gcs_bucket: storage.Bucket
) -> None:
    bucket_name = gcs_bucket.name
    quickstart.storage_control_quickstart(bucket_name=bucket_name)

    out, _ = capsys.readouterr()
    layout_name = f"projects/_/buckets/{bucket_name}/storageLayout"
    assert layout_name in out
