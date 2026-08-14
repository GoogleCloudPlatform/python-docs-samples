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

# [START aiplatform_genai_embeddings_specify_lower_dimension]
import os

from google import genai

# TODO (Developer) Set environment variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = "global"

# Supported dimensions: 128, 256, 512, 1408 (or up to 3072 for gemini-embedding-2)
EMBEDDING_DIMENSION = 128
IMAGE_URI = "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png"
EMBEDDING_MODEL = "gemini-embedding-2"
CONTEXTUAL_TEXT = "Colosseum"


def generate_embeddings_with_lower_dimension() -> genai.types.EmbedContentResponse:
    """Generates multimodal embeddings (image + text) with custom lower dimensionality

    using the modern google-genai SDK.
    """

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION_ID,
    )

    image_part = genai.types.Part.from_uri(
        file_uri=IMAGE_URI,
        mime_type="image/png",
    )

    text_part = genai.types.Part.from_text(text=CONTEXTUAL_TEXT)

    contents = genai.types.Content(parts=[image_part, text_part])

    config = genai.types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSION)

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[contents],
        config=config,
    )

    embeddings = response.embeddings[0].values

    print(f"Embeddings (dim={len(embeddings)}): {embeddings[:3]}...")

    return response


# [END aiplatform_genai_embeddings_specify_lower_dimension]
