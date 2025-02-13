# Copyright 2025 Google LLC
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


def update_content_cache(cache_name: str) -> str:
    # [START googlegenaisdk_contentcache_update]
    from datetime import datetime as dt
    from datetime import timezone as tz
    from datetime import timedelta

    from google import genai
    from google.genai.types import HttpOptions, UpdateCachedContentConfig

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Get content cache by name
    # cache_name = "projects/111111111111/locations/us-central1/cachedContents/1111111111111111111"
    content_cache = client.caches.get(name=cache_name)
    print("Expire time", content_cache.expire_time)
    # Example response
    #   Expire time 2025-02-20 15:50:18.434482+00:00

    # Update expire time using TTL
    content_cache = client.caches.update(
        name=cache_name, config=UpdateCachedContentConfig(ttl="36000s")
    )
    time_diff = content_cache.expire_time - dt.now(tz.utc)
    print("Expire time(after update):", content_cache.expire_time)
    print("Expire time(in seconds):", time_diff.seconds)
    # Example response
    #   Expire time(after update): 2025-02-14 01:51:42.571696+00:00
    #   Expire time(in seconds): 35999

    # Update expire time using specific time stamp
    next_week_utc = dt.now(tz.utc) + timedelta(days=7)
    content_cache = client.caches.update(
        name=cache_name, config=UpdateCachedContentConfig(expireTime=next_week_utc)
    )
    print("Expire time(after update):", content_cache.expire_time)
    # Example response
    #   Expire time(after update): 2025-02-20 15:51:42.614968+00:00
    # [END googlegenaisdk_contentcache_update]
    return cache_name


if __name__ == "__main__":
    cache_name = input("Cache Name: ")
    update_content_cache(cache_name)
