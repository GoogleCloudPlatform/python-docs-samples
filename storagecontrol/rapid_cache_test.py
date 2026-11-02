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

import time

from google.cloud import storage
from google.cloud import storage_control_v2
import pytest

import create_rapid_cache
import disable_rapid_cache
import get_rapid_cache
import list_rapid_caches
import update_rapid_cache

# Poll for up to 2 minutes for the cache to reach the "disabled" state.
_DISABLE_POLL_ATTEMPTS = 12
_DISABLE_POLL_INTERVAL_SECONDS = 10


def test_rapid_cache_create_get_list_update_disable(
    capsys: pytest.CaptureFixture[str],
    regional_hns_enabled_bucket: storage.Bucket,
    rapid_cache_zone: str,
) -> None:
    bucket_name = regional_hns_enabled_bucket.name

    # Test create Rapid Cache
    create_rapid_cache.create_rapid_cache(
        bucket_name=bucket_name, zone=rapid_cache_zone
    )
    out, _ = capsys.readouterr()
    prefix = "Created Rapid Cache: "
    assert prefix in out
    cache_name = out.split(prefix, 1)[1].split()[0]
    cache_id = storage_control_v2.StorageControlClient.parse_rapid_cache_path(
        cache_name
    )["rapid_cache"]
    assert cache_id

    try:
        # Test get Rapid Cache
        get_rapid_cache.get_rapid_cache(bucket_name=bucket_name, cache_id=cache_id)
        out, _ = capsys.readouterr()
        assert cache_name in out
        assert f"Zone: {rapid_cache_zone}" in out

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
    finally:
        # Disable the Rapid Cache. This also cleans up the cache so that the
        # bucket can be deleted once the cache has been fully removed.
        disable_rapid_cache.disable_rapid_cache(
            bucket_name=bucket_name, cache_id=cache_id
        )
        disable_out, _ = capsys.readouterr()

    # Test disable Rapid Cache
    assert f"Disabling Rapid Cache: {cache_name}" in disable_out

    # The cache moves to the "disabled" state shortly after the request.
    for _ in range(_DISABLE_POLL_ATTEMPTS):
        get_rapid_cache.get_rapid_cache(bucket_name=bucket_name, cache_id=cache_id)
        out, _ = capsys.readouterr()
        if "State: disabled" in out:
            break
        time.sleep(_DISABLE_POLL_INTERVAL_SECONDS)
    assert "State: disabled" in out
