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
from __future__ import annotations

import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_context_caches() -> list[str]:
    # [START generativeaionvertexai_context_caching_list]
    import vertexai

    from vertexai.preview import caching

    # TODO(developer): Update & uncomment line below
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    cache_list = caching.CachedContent.list()
    # Access individual properties of a CachedContent object
    for cached_content in cache_list:
        print(f"Cache '{cached_content.name}' for model '{cached_content.model_name}'")
        print(f"Last updated at: {cached_content.update_time}")
        print(f"Expires at: {cached_content.expire_time}")
        # Example response:
        # Cached content 'example-cache' for model '.../gemini-1.5-pro-001'
        # Last updated at: 2024-09-16T12:41:09.998635Z
        # Expires at: 2024-09-16T13:41:09.989729Z
    # [END generativeaionvertexai_context_caching_list]
    return [cached_content.name for cached_content in cache_list]


if __name__ == "__main__":
    list_context_caches()
