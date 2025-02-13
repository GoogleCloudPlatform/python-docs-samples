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


def list_context_caches() -> str:
    # [START googlegenaisdk_contentcache_list]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    content_cache_list = client.caches.list()

    # Access individual properties of a ContentCache object(s)
    for content_cache in content_cache_list:
        print(f"Cache `{content_cache.name}` for model `{content_cache.model}`")
        print(f"Last updated at: {content_cache.update_time}")
        print(f"Expires at: {content_cache.expire_time}")

    # Example response:
    # * Cache `projects/111111111111/locations/us-central1/cachedContents/1111111111111111111` for
    #       model `projects/111111111111/locations/us-central1/publishers/google/models/gemini-XXX-pro-XXX`
    # * Last updated at: 2025-02-13 14:46:42.620490+00:00
    # * CachedContentUsageMetadata(audio_duration_seconds=None, image_count=167, text_count=153, total_token_count=43130, video_duration_seconds=None)
    # ...
    # [END googlegenaisdk_contentcache_list]
    return [content_cache.name for content_cache in content_cache_list]


if __name__ == "__main__":
    list_context_caches()
