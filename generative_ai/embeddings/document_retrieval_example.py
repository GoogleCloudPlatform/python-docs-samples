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
    """Calculates embeddings for the given text inputs.

    Returns:
        A list of lists containing the embedding vectors for each input text.
    """

    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    inputs = [
        # Option1: Use TextEmbeddingInput object as embedding input
        TextEmbeddingInput(
            text=(
                "You'll find some apps on your Home screens, and all your apps in All Apps. "
                "You can open apps, switch between apps, and find 2 apps at once."
            ),
            title="Find, open & close apps on a Pixel phone",
            # The task type for embedding. Check the available tasks in the model's documentation.
            task_type="RETRIEVAL_DOCUMENT"
        ),
        # Option2: Use plain text as embedding input
        (
            "You can download no-charge and paid apps from Google Play on your Android phone or tablet. "
            "We recommend that you get apps from Google Play, but you can also get them from other sources."
        )
    ]

    # The dimensionality of the output embeddings.
    dimensionality = 128
    embeddings = model.get_embeddings(inputs, output_dimensionality=dimensionality)

    for embedding in embeddings:
        print(embedding)
        # Example response:
        # TextEmbedding(values=[0.06830032169818878, 0.03944097459316254, ...], 'statistics': { ... }, ...)

    return [embedding.values for embedding in embeddings]


# [END generativeaionvertexai_embedding]


if __name__ == "__main__":
    embed_text()
