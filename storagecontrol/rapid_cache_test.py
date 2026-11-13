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

import concurrent.futures
import contextlib

import create_rapid_cache
import disable_rapid_cache
import get_rapid_cache
from google.cloud import storage
from google.cloud import storage_control_v2
import list_rapid_caches
import pytest
import update_rapid_cache

# The disable operation only completes once the cache has been fully removed,
# which can take more than an hour. The cache reaches the "disabled" state
# within seconds, so the test bounds the wait on the operation and then
# checks the cache state.
_DISABLE_TIMEOUT_SECONDS = 600


def test_rapid_cache_create_get_list_update_disable(
    capsys: pytest.CaptureFixture[str],
    regional_hns_enabled_bucket: storage.Bucket,
    rapid_cache_zone: str,
    rapid_cache_id: str,
) -> None:
    bucket_name = regional_hns_enabled_bucket.name
    cache_id = rapid_cache_id
    cache_name = storage_control_v2.StorageControlClient.rapid_cache_path(
        project="_", bucket=bucket_name, rapid_cache=cache_id
    )

    # Test create Rapid Cache
    create_rapid_cache.create_rapid_cache(
        bucket_name=bucket_name, zone=rapid_cache_zone
    )
    out, _ = capsys.readouterr()
    assert f"Created Rapid Cache: {cache_name}" in out
    assert "State: running" in out
    assert "Cache type: rapid-cache-ultra" in out

    # Test get Rapid Cache
    get_rapid_cache.get_rapid_cache(bucket_name=bucket_name, cache_id=cache_id)
    out, _ = capsys.readouterr()
    assert f"Got Rapid Cache: {cache_name}" in out
    assert f"Zone: {rapid_cache_zone}" in out
    assert "State: running" in out
    assert "Cache type: rapid-cache-ultra" in out

    # Test list Rapid Caches
    list_rapid_caches.list_rapid_caches(bucket_name=bucket_name)
    out, _ = capsys.readouterr()
    assert cache_name in out

    # Test update Rapid Cache
    update_rapid_cache.update_rapid_cache(
        bucket_name=bucket_name, cache_id=cache_id, ttl_seconds=172800
    )
    out, _ = capsys.readouterr()
    assert f"Updated Rapid Cache: {cache_name}" in out
    assert "TTL: 172800 seconds" in out

    # Test disable Rapid Cache. The wait on the operation is bounded by the
    # native operation timeout; if it expires, the cache state is checked.
    with contextlib.suppress(concurrent.futures.TimeoutError):
        disable_rapid_cache.disable_rapid_cache(
            bucket_name=bucket_name,
            cache_id=cache_id,
            timeout=_DISABLE_TIMEOUT_SECONDS,
        )
    capsys.readouterr()
    get_rapid_cache.get_rapid_cache(bucket_name=bucket_name, cache_id=cache_id)
    out, _ = capsys.readouterr()
    assert "State: disabled" in out
