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

from typing import Tuple

from agentplatform import types
from google.genai import types as genai_types

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
MODEL_ID = os.getenv("MODEL_ID")


def quickstart(
    display_name: str,
    gcs_path: str,
) -> Tuple[types.RagCorpus, genai_types.GenerateContentResponse]:
    # [START generativeaionvertexai_rag_quickstart]
    import agentplatform

    from agentplatform import types
    from google import genai
    from google.genai import types as genai_types


    # Create a RAG Corpus, Import Files, and Generate a response

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # MODEL_ID = "gemini-3.5-flash"
    # display_name = "test_corpus"
    # gcs_path = "gs://my_bucket/my_files_dir/*"
    # google_drive_path ="https://drive.google.com/file/d/123"

    # Initialize Agent Platform client once per session
    client = agentplatform.Client(project=PROJECT_ID, location="us-east4")

    # Configure embedding model, for example "text-embedding-005".
    embedding_model_config = types.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=types.RagEmbeddingModelConfigVertexPredictionEndpoint(
            endpoint="publishers/google/models/text-embedding-005"
        ),
    )

    # Create RagCorpus
    rag_corpus = client.rag.create_corpus(
        rag_corpus=types.RagCorpus(
            display_name=display_name,
            rag_vector_db_config=types.RagVectorDbConfig(
                rag_embedding_model_config=embedding_model_config
            )
        )
    )

    # Import Files to the RagCorpus
    client.rag.import_files(
        name=rag_corpus.name,
        import_config=types.ImportRagFilesConfig(
            gcs_source=genai_types.GcsSource(uris=[gcs_path]),
            rag_file_transformation_config=types.RagFileTransformationConfig(
                rag_file_chunking_config=types.RagFileChunkingConfig(
                    chunk_size=512,
                    chunk_overlap=100,
                )
            ), # optional
            max_embedding_requests_per_min=1000, # optional
        )
    )

    # Direct context retrieval
    rag_retrieval_config = genai_types.RagRetrievalConfig(
        top_k=3,  # Optional
        filter=genai_types.RagRetrievalConfigFilter(
            vector_distance_threshold=0.5
        ),  # Optional
    )
    response = client.rag.retrieve_contexts(
        vertex_rag_store=genai_types.VertexRagStore(
            rag_resources=[
                genai_types.VertexRagStoreRagResource(
                    rag_corpus=rag_corpus.name,
                )
            ],
        ),
        query=types.RagQuery(
            text="What is RAG and why it is helpful?",
            rag_retrieval_config=rag_retrieval_config,   
        )
    )
    print(response)

    # Enhance generation
    # Create a RAG retrieval tool
    rag_retrieval_tool = genai_types.Tool(
        retrieval=genai_types.Retrieval(
            vertex_rag_store=genai_types.VertexRagStore(
                rag_resources=[
                    genai_types.VertexRagStoreRagResource(
                        rag_corpus=rag_corpus.name,
                        # Optional: supply IDs from `rag.list_files()`.
                        # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                    )
                ],
                rag_retrieval_config=rag_retrieval_config,
            ),
        )
    )

    # Call generate_content with the tool using the GenAI SDK

    # Create a GenAI SDK client
    genai_client = genai.Client(enterprise=True, project=PROJECT_ID, location="us-east4")


    response = genai_client.models.generate_content(
        model=MODEL_ID,
        contents="What is RAG and why it is helpful?",
        config=genai_types.GenerateContentConfig(
            tools=[rag_retrieval_tool]
        )
    )
    print(response.text)
    # Example response:
    #   RAG stands for Retrieval-Augmented Generation.
    #   It's a technique used in AI to enhance the quality of responses
    # ...

    # [END generativeaionvertexai_rag_quickstart]
    return rag_corpus, response


if __name__ == "__main__":
    gdrive_path = "https://drive.google.com/file/1234567890"
    gcloud_path = "gs://your-bucket-name/file.txt"
    quickstart(
        display_name="test_corpus",
        paths=[gdrive_path, gcloud_path],
    )
