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

from typing import List

from google.cloud.aiplatform_v1beta1.types.cached_content import CachedContent

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_content_caches() -> List[CachedContent]:
    # [START generativeaionvertexai_gemini_get_list_of_context_caches]
    import json

    import vertexai

    from vertexai.preview import caching

    # TODO(developer): Update & uncomment line below
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    cached_content_list = caching.CachedContent.list()
    # Access individual properties of a CachedContent object
    for cc in cached_content_list:
        print(
            f"Cached content '{cc.display_name}' for model '{cc.model_name}' expires at {cc.expire_time}."
        )
        # Example response:
        # Cached content 'scientific-articles' for model '.../gemini-1.5-pro-001' expires at 2024-09-23 18:01:47.242036+00:00.

    # or convert the ContentCache object to a dictionary:
    for cc in cached_content_list:
        print(json.dumps(cc.to_dict(), indent=2))
        # Example response:
        #  {
        #      "name": "projects/[PROJECT_NUMBER]/locations/us-central1/cachedContents/4101407070023057408",
        #      "model": "projects/[PROJECT_ID]/locations/us-central1/publishers/google/models/gemini-1.5-pro-001",
        #      "createTime": "2024-09-16T12:41:09.998635Z",
        #      "updateTime": "2024-09-16T12:41:09.998635Z",
        #      "expireTime": "2024-09-16T13:41:09.989729Z",
        #      "displayName": "scientific-articles"
        #      "usageMetadata": {
        #          "totalTokenCount": 43130,
        #          "textCount": 153,
        #          "imageCount": 167
        #      }
        #  }

    # [END generativeaionvertexai_gemini_get_list_of_context_caches]
    return cached_content_list


if __name__ == "__main__":
    list_content_caches()
