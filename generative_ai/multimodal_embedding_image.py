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


def get_image_embeddings() -> MultiModalEmbeddingResponse:
    """Example of how to generate multimodal embeddings from image and text.

    Read more @ https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-multimodal-embeddings#low-dimension
    """
    # [START aiplatform_sdk_multimodal_embedding_image]
    import vertexai
    from vertexai.vision_models import Image, MultiModalEmbeddingModel

    # TODO(developer): Update project
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    image = Image.load_from_file(
        "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png"
    )

    embeddings = model.get_embeddings(
        image=image,
        contextual_text="Colosseum",
        dimension=1408,
    )
    print(f"Image Embedding: {embeddings.image_embedding}")
    print(f"Text Embedding: {embeddings.text_embedding}")
    # [END aiplatform_sdk_multimodal_embedding_image]

    return embeddings


if __name__ == "__main__":
    get_image_embeddings()
