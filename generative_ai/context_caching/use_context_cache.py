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


def use_context_cache(project_id: str, cache_id: str) -> str:
    # [START generativeaionvertexai_gemini_use_context_cache]
    import vertexai

    from vertexai.preview.generative_models import GenerativeModel
    from vertexai.preview import caching

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # cache_id = "CACHE_ID"

    vertexai.init(project=project_id, location="us-central1")

    cached_content = caching.CachedContent(cached_content_name=cache_id)

    model = GenerativeModel.from_cached_content(cached_content=cached_content)

    response = model.generate_content("What are the papers about?")

    print(response.text)
    # [END generativeaionvertexai_gemini_use_context_cache]

    return response.text
