# Copyright 2026 Google LLC
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

# [START aiplatform_genai_multimodal_embedding_image_video_text]

import os

from google import genai

# Environment configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
LOCATION_ID = "global"

EMBEDDING_MODEL = "gemini-embedding-2"
IMAGE_URI = "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png"
VIDEO_URI = "gs://cloud-samples-data/vertex-ai-vision/highway_vehicles.mp4"
CONTEXTUAL_TEXT = "Cars on Highway"


def get_image_video_text_embeddings() -> genai.types.EmbedContentResponse:
    """Generates multimodal embeddings from image, video, and text using the google-genai SDK."""

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION_ID,
    )

    image_part = genai.types.Part.from_uri(
        file_uri=IMAGE_URI,
        mime_type="image/png",
    )

    video_part = genai.types.Part.from_uri(
        file_uri=VIDEO_URI,
        mime_type="video/mp4",
    )

    content = genai.types.Content(
        parts=[image_part, video_part, genai.types.Part.from_text(text=CONTEXTUAL_TEXT)]
    )

    # Joint/Interleaved Multimodal Embedding (Image + Video + Text in same vector space)
    response = client.models.embed_content(model=EMBEDDING_MODEL, contents=content)

    if response.embeddings:

        vector = response.embeddings[0].values

        print(f"Embeddings ({len(vector)} dims): {vector[:3]}...")

    print(response)

    return response


# [END aiplatform_genai_multimodal_embedding_image_video_text]
