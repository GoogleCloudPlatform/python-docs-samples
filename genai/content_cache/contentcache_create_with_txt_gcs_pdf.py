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


def create_content_cache() -> str:
    # [START googlegenaisdk_contentcache_create_with_txt_gcs_pdf]
    from google import genai
    from google.genai.types import Content, CreateCachedContentConfig, HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    system_instruction = """
    You are an expert researcher. You always stick to the facts in the sources provided, and never make up new facts.
    Now look at these research papers, and answer the following questions.
    """

    contents = [
        Content(
            role="user",
            parts=[
                Part.from_uri(
                    file_uri="gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf",
                    mime_type="application/pdf",
                ),
                Part.from_uri(
                    file_uri="gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
                    mime_type="application/pdf",
                ),
            ],
        )
    ]

    content_cache = client.caches.create(
        model="gemini-2.5-flash-preview-05-20",
        config=CreateCachedContentConfig(
            contents=contents,
            system_instruction=system_instruction,
            display_name="example-cache",
            ttl="86400s",
        ),
    )

    print(content_cache.name)
    print(content_cache.usage_metadata)
    # Example response:
    #   projects/111111111111/locations/us-central1/cachedContents/1111111111111111111
    #   CachedContentUsageMetadata(audio_duration_seconds=None, image_count=167,
    #       text_count=153, total_token_count=43130, video_duration_seconds=None)
    # [END googlegenaisdk_contentcache_create_with_txt_gcs_pdf]
    return content_cache.name


if __name__ == "__main__":
    create_content_cache()
