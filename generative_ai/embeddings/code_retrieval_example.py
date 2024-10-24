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

from __future__ import annotations

# [START generativeaionvertexai_embedding_code_retrieval]
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

MODEL_NAME = "text-embedding-005"
DIMENSIONALITY = 256


def embed_text(
    texts: list[str] = ["Retrieve a function that adds two numbers"],
    task: str = "CODE_RETRIEVAL_QUERY",
    model_name: str = "text-embedding-005",
    dimensionality: int | None = 256,
) -> list[list[float]]:
    """Embeds texts with a pre-trained, foundational model."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)
    # Example response:
    # [[0.025890009477734566, -0.05553026497364044, 0.006374752148985863,...],
    return [embedding.values for embedding in embeddings]


if __name__ == "__main__":
    # Embeds code block with a pre-trained, foundational model.
    # Using this function to calculate the embedding for corpus.
    texts = ["Retrieve a function that adds two numbers"]
    task = "CODE_RETRIEVAL_QUERY"
    code_block_embeddings = embed_text(
        texts=texts, task=task, model_name=MODEL_NAME, dimensionality=DIMENSIONALITY
    )

    # Embeds code retrieval with a pre-trained, foundational model.
    # Using this function to calculate the embedding for query.
    texts = [
        "def func(a, b): return a + b",
        "def func(a, b): return a - b",
        "def func(a, b): return (a ** 2 + b ** 2) ** 0.5",
    ]
    task = "RETRIEVAL_DOCUMENT"
    code_query_embeddings = embed_text(
        texts=texts, task=task, model_name=MODEL_NAME, dimensionality=DIMENSIONALITY
    )

# [END generativeaionvertexai_embedding_code_retrieval]
