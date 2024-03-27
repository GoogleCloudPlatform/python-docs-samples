# Copyright 2023 Google LLC
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

# [START aiplatform_sdk_embedding]
from typing import List

from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_text(
    texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
    task_types: List[str] = ["QUESTION_ANSWERING", "FACT_VERIFICATION"],
    model_name: str = "text-embedding-preview-0409",
) -> list:
    """Embeds texts with a pre-trained, foundational model."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    # Google unveils elastic models at Google Cloud Next '24 (April 2024):
    elastic = model_name in {
        "text-embedding-preview-0409",
        "text-multilingual-embedding-preview-0409",
    }
    inputs = [TextEmbeddingInput(*z) for z in zip(texts, task_types)]
    kwargs = dict(output_dimensionality=192) if elastic else {}
    embeddings = model.get_embeddings(inputs, **kwargs)
    return [embedding.values for embedding in embeddings]
# [END aiplatform_sdk_embedding]


if __name__ == "__main__":
    embed_text()
