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

# [START googlegenaisdk_multimodal_embedding_image]
from google import genai
from google.genai import types


def embed_content() -> types.EmbedContentResponse:
    client = genai.Client()

    content = types.Content(
        parts=[
            types.Part.from_uri(
                file_uri="gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png",
                mime_type="image/png",
            ),
            types.Part.from_text(text="Colosseum"),
        ],
    )

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=[content],
        config=types.EmbedContentConfig(
            output_dimensionality=1408,
        ),
    )
    print(response)
    # Example response:
    # embeddings=[ContentEmbedding(values=[-0.0123147098, 0.0727171078, ...])]
    return response


# [END googlegenaisdk_multimodal_embedding_image]
