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

from agentplatform import types
from typing import Optional

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

def create_corpus_vector_search(
    vector_search_index_name: str,
    vector_search_index_endpoint_name: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
) -> types.RagCorpus:
    # [START generativeaionvertexai_rag_create_corpus_vector_search]

    import agentplatform
    from agentplatform import types

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # vector_search_index_name = "projects/{PROJECT_ID}/locations/{LOCATION}/indexes/{INDEX_ID}"
    # vector_search_index_endpoint_name = "projects/{PROJECT_ID}/locations/{LOCATION}/indexEndpoints/{INDEX_ENDPOINT_ID}"
    # display_name = "test_corpus"
    # description = "Corpus Description"

    # Initialize Agent Platform client once per session
    client = agentplatform.Client(project=PROJECT_ID, location="us-central1")

    # Configure embedding model (Optional)
    embedding_model_config = types.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=types.RagEmbeddingModelConfigVertexPredictionEndpoint(
            endpoint="publishers/google/models/text-embedding-005"
        )
    )

    # Configure Vector DB
    vector_db = types.RagVectorDbConfigVertexVectorSearch(
        index=vector_search_index_name,
        index_endpoint=vector_search_index_endpoint_name
    )

    corpus = client.rag.create_corpus(
        rag_corpus=types.RagCorpus(
            display_name=display_name,
            description=description,
            rag_vector_db_config=types.RagVectorDbConfig(
                rag_embedding_model_config=embedding_model_config,
                vertex_vector_search=vector_db,
            ),
        )
    )
    print(corpus)
    # Example response:
    # RagCorpus(name='projects/1234567890/locations/us-central1/ragCorpora/1234567890',
    # display_name='test_corpus', description='Corpus Description', embedding_model_config=...
    # ...

    # [END generativeaionvertexai_rag_create_corpus_vector_search]
    return corpus


if __name__ == "__main__":
    create_corpus_vector_search(
        vector_search_index_name="projects/{PROJECT_ID}/locations/{LOCATION}/indexes/{INDEX_ID}",
        vector_search_index_endpoint_name="projects/{PROJECT_ID}/locations/{LOCATION}/indexEndpoints/{INDEX_ENDPOINT_ID}",
        display_name="test_corpus",
        description="Corpus Description",
    )
