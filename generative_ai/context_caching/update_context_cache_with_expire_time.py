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

from google.cloud.aiplatform_v1beta1.types.cached_content import CachedContent

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def update_context_cache_with_expire_time(cache_id: str) -> CachedContent:
    # [START generativeaionvertexai_gemini_update_context_cache_with_expire_time]
    import vertexai
    # from datetime import datetime as dt, timezone as tz
    import datetime as dt

    from vertexai.preview import caching

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # cache_id = "your-cache-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    cached_content = caching.CachedContent(cached_content_name=cache_id)

    # Update the expiration to a specific time in the future
    next_year_utc = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=365)
    cached_content.update(expire_time=next_year_utc)
    cached_content.refresh()

    print("Expire time:", cached_content.expire_time)
    # Example output:
    # Expire time: 2025-09-25 17:16:45.864520+00:00
    # [END generativeaionvertexai_gemini_update_context_cache_with_expire_time]
    return cached_content


if __name__ == "__main__":
    update_context_cache_with_expire_time("1234567890")
