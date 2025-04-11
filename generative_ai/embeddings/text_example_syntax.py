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

import vertexai

from vertexai.language_models import TextEmbedding

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

vertexai.init(project=PROJECT_ID, location="us-central1")


def create_embeddings() -> TextEmbedding:
    # [START generativeaionvertexai_text_embedding_example_syntax]
    from vertexai.language_models import TextEmbeddingModel

    model = TextEmbeddingModel.from_pretrained("text-embedding-005")
    embeddings = model.get_embeddings(["Cars on a highway", "Traffic lights"])
    # [END generativeaionvertexai_text_embedding_example_syntax]
    return embeddings


if __name__ == "__main__":
    create_embeddings()
