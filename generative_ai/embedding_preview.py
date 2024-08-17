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

# [START generativeaionvertexai_sdk_embedding]
from typing import List, Optional

from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_code_query(
    texts: List[str] = ["Retrieve a function that adds two numbers"],
    task: str = "CODE_RETRIEVAL_QUERY",
    model_name: str = "text-embedding-preview-0815",
    dimensionality: Optional[int] = 256,
) -> List[List[float]]:
    """Embeds code retrieval with a pre-trained, foundational model. Using this function to calculate the embedding for query."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)
    return [embedding.values for embedding in embeddings]


def embed_code_corpus(
    texts: List[str] = [
        "def func(a, b): return a + b",
        "def func(a, b): return a - b",
        "def func(a, b): return (a ** 2 + b ** 2) ** 0.5",
    ],
    task: str = "RETRIEVAL_DOCUMENT",
    model_name: str = "text-embedding-preview-0815",
    dimensionality: Optional[int] = 256,
) -> List[List[float]]:
    """Embeds code block with a pre-trained, foundational model. Using this function to calculate the embedding for corpus."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)
    return [embedding.values for embedding in embeddings]


# [END generativeaionvertexai_sdk_embedding]


if __name__ == "__main__":
    embed_code_query()
    embed_code_corpus()

