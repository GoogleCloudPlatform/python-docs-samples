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

from typing import Optional

from google.cloud.aiplatform_v1beta1 import RagCorpus

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def create_corpus(
    display_name: Optional[str] = None,
    description: Optional[str] = None,
) -> RagCorpus:
    # [START generativeaionvertexai_rag_create_corpus]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # display_name = "test_corpus"
    # description = "Corpus Description"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Configure embedding model
    embedding_model_config = rag.EmbeddingModelConfig(
        publisher_model="publishers/google/models/text-embedding-004"
    )

    corpus = rag.create_corpus(
        display_name=display_name,
        description=description,
        embedding_model_config=embedding_model_config,
    )
    print(corpus)
    # Example response:
    # RagCorpus(name='projects/1234567890/locations/us-central1/ragCorpora/1234567890',
    # display_name='test_corpus', description='Corpus Description', embedding_model_config=...
    # ...

    # [END generativeaionvertexai_rag_create_corpus]
    return corpus


if __name__ == "__main__":
    create_corpus(display_name="test_corpus", description="Corpus Description")
