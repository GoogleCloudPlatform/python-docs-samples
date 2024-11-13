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


def create_context_cache() -> str:
    # [START generativeaionvertexai_gemini_create_context_cache]
    import vertexai
    import datetime

    from vertexai.generative_models import Part
    from vertexai.preview import caching

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    system_instruction = """
    You are an expert researcher. You always stick to the facts in the sources provided, and never make up new facts.
    Now look at these research papers, and answer the following questions.
    """

    contents = [
        Part.from_uri(
            "gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf",
            mime_type="application/pdf",
        ),
        Part.from_uri(
            "gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
            mime_type="application/pdf",
        ),
    ]

    cached_content = caching.CachedContent.create(
        model_name="gemini-1.5-pro-002",
        system_instruction=system_instruction,
        contents=contents,
        ttl=datetime.timedelta(minutes=60),
        display_name="example-cache",
    )

    print(cached_content.name)
    # Example response:
    # 1234567890
    # [END generativeaionvertexai_gemini_create_context_cache]

    return cached_content.name


if __name__ == "__main__":
    create_context_cache()
