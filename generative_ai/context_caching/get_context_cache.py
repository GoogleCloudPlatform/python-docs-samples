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


def get_context_cache(cache_id: str) -> str:
    # [START generativeaionvertexai_gemini_get_context_cache]
    import vertexai

    from vertexai.preview import caching

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # cache_id = "your-cache-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    cached_content = caching.CachedContent(cached_content_name=cache_id)

    print(cached_content.resource_name)
    # Example response:
    # projects/[PROJECT_ID]/locations/us-central1/cachedContents/1234567890
    # [END generativeaionvertexai_gemini_get_context_cache]
    return cached_content.resource_name


if __name__ == "__main__":
    get_context_cache("1234567890")
