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

from vertexai.vision_models import MultiModalEmbeddingResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_embeddings_with_lower_dimension() -> MultiModalEmbeddingResponse:
    """Example of how to use lower dimensions when creating multimodal embeddings.

    Read more @ https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings#low-dimension

    Returns:
        The multimodal embedding response.
    """
    # [START generativeaionvertexai_embeddings_specify_lower_dimension]
    import vertexai

    from vertexai.vision_models import Image, MultiModalEmbeddingModel

    # TODO(developer): Update & uncomment line below
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # TODO(developer): Try different dimenions: 128, 256, 512, 1408
    embedding_dimension = 128

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
    image = Image.load_from_file(
        "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png"
    )

    embeddings = model.get_embeddings(
        image=image,
        contextual_text="Colosseum",
        dimension=embedding_dimension,
    )

    print(f"Image Embedding: {embeddings.image_embedding}")
    print(f"Text Embedding: {embeddings.text_embedding}")

    # Example response:
    # Image Embedding: [0.0622573346, -0.0406507477, 0.0260440577, ...]
    # Text Embedding: [0.27469793, -0.146258667, 0.0222803634, ...]
    # [END generativeaionvertexai_embeddings_specify_lower_dimension]
    return embeddings


if __name__ == "__main__":
    generate_embeddings_with_lower_dimension()
