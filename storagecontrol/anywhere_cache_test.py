# Copyright 2026 Google LLC
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

import anywhere_cache_create
import anywhere_cache_disable
import anywhere_cache_get
import anywhere_cache_list
import anywhere_cache_pause
import anywhere_cache_resume
import anywhere_cache_update


def test_anywhere_cache_lifecycle(
    capsys: pytest.LogCaptureFixture, ubla_enabled_bucket: storage.Bucket
) -> None:
    bucket_name = ubla_enabled_bucket.name
    zone = "us-central1-a"
    anywhere_cache_id = f"projects/_/buckets/{bucket_name}/anywhereCaches/{zone}"

    # Test create
    anywhere_cache_create.create_anywhere_cache(bucket_name=bucket_name, zone=zone)
    out, _ = capsys.readouterr()
    assert anywhere_cache_id in out

    # Test get
    anywhere_cache_get.get_anywhere_cache(anywhere_cache_id=anywhere_cache_id)
    out, _ = capsys.readouterr()
    assert anywhere_cache_id in out
    assert "admit-on-second-miss" in out

    # Test list
    anywhere_cache_list.list_anywhere_caches(bucket_name=bucket_name)
    out, _ = capsys.readouterr()
    assert anywhere_cache_id in out

    # Test update
    anywhere_cache_update.update_anywhere_cache(
        anywhere_cache_id=anywhere_cache_id, admission_policy="admit-on-second-miss"
    )
    out, _ = capsys.readouterr()
    assert anywhere_cache_id in out
    assert "admit-on-second-miss" in out

    # Test pause
    anywhere_cache_pause.pause_anywhere_cache(anywhere_cache_id=anywhere_cache_id)
    out, _ = capsys.readouterr()
    assert anywhere_cache_id in out

    # Test resume
    anywhere_cache_resume.resume_anywhere_cache(anywhere_cache_id=anywhere_cache_id)
    out, _ = capsys.readouterr()
    assert anywhere_cache_id in out

    # Test disable
    anywhere_cache_disable.disable_anywhere_cache(anywhere_cache_id=anywhere_cache_id)
    out, _ = capsys.readouterr()
    assert anywhere_cache_id in out
