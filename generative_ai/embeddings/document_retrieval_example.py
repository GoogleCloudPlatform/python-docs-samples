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

# [START generativeaionvertexai_embedding]
from __future__ import annotations

from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_text() -> list[list[float]]:
    """Embeds texts with a pre-trained, foundational model.

    Returns:
        A list of lists containing the embedding vectors for each input text
    """

    # A list of texts to be embedded.
    texts = ["banana muffins? ", "banana bread? banana muffins?"]
    # The dimensionality of the output embeddings.
    dimensionality = 256
    # The task type for embedding. Check the available tasks in the model's documentation.
    task = "RETRIEVAL_DOCUMENT"

    model = TextEmbeddingModel.from_pretrained("text-embedding-005")
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)

    print(embeddings)
    # Example response:
    # [[0.006135190837085247, -0.01462465338408947, 0.004978656303137541, ...], [0.1234434666, ...]],
    return [embedding.values for embedding in embeddings]


# [END generativeaionvertexai_embedding]


if __name__ == "__main__":
    embed_text()
