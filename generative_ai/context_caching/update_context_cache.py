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
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def update_context_cache(cache_id: str) -> str:
    # [START generativeaionvertexai_gemini_update_context_cache]
    import vertexai
    from datetime import datetime as dt
    from datetime import timezone as tz
    from datetime import timedelta

    from vertexai.preview import caching

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # cache_id = "your-cache-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    cached_content = caching.CachedContent(cached_content_name=cache_id)

    # Option1: Update the context cache using TTL (Time to live)
    cached_content.update(ttl=timedelta(hours=3))
    cached_content.refresh()

    # Option2: Update the context cache using specific time
    next_week_utc = dt.now(tz.utc) + timedelta(days=7)
    cached_content.update(expire_time=next_week_utc)
    cached_content.refresh()

    print(cached_content.expire_time)
    # Example response:
    # 2024-09-11 17:16:45.864520+00:00
    # [END generativeaionvertexai_gemini_update_context_cache]
    return cached_content.expire_time


if __name__ == "__main__":
    update_context_cache("1234567890")
