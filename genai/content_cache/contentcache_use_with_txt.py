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


def generate_content(cache_name: str) -> str:
    # [START googlegenaisdk_contentcache_use_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    # Use content cache to generate text response
    # E.g cache_name = 'projects/111111111111/locations/us-central1/cachedContents/1111111111111111111'
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents="Summarize the pdfs",
        config=GenerateContentConfig(
            cached_content=cache_name,
        ),
    )
    print(response.text)
    # Example response
    #   The Gemini family of multimodal models from Google DeepMind demonstrates remarkable capabilities across various
    #   modalities, including image, audio, video, and text....
    # [END googlegenaisdk_contentcache_use_with_txt]
    return response.text


if __name__ == "__main__":
    cache_name = input("Cache Name: ")
    generate_content(cache_name)
