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

from vertexai import rag

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def create_corpus_vertex_ai_search(
    vertex_ai_search_engine_name: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
) -> rag.RagCorpus:
    # [START generativeaionvertexai_rag_create_corpus_vertex_ai_search]

    from vertexai import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # vertex_ai_search_engine_name = "projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/engines/{ENGINE_ID}"
    # display_name = "test_corpus"
    # description = "Corpus Description"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Configure Search
    vertex_ai_search_config = rag.VertexAiSearchConfig(
        serving_config=f"{vertex_ai_search_engine_name}/servingConfigs/default_search",
    )

    corpus = rag.create_corpus(
        display_name=display_name,
        description=description,
        vertex_ai_search_config=vertex_ai_search_config,
    )
    print(corpus)
    # Example response:
    # RagCorpus(name='projects/1234567890/locations/us-central1/ragCorpora/1234567890',
    # display_name='test_corpus', description='Corpus Description'.
    # ...

    # [END generativeaionvertexai_rag_create_corpus_vertex_ai_search]
    return corpus


if __name__ == "__main__":
    create_corpus_vertex_ai_search(
        vertex_ai_search_engine_name="projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/engines/{ENGINE_ID}",
        display_name="test_corpus",
        description="Corpus Description",
    )
