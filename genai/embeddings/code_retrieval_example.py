# Copyright 2026 Google LLC
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

# [START aiplatform_genai_embedding_code_retrieval]
import os

from google import genai

# TODO (Developer) set the following environment variables.
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION_ID = os.getenv("LOCATION_ID", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-embedding-001")

QUERY_LINES = ["Retrieve a function that adds two numbers"]
CODE_RETRIEVAL_QUERY = "CODE_RETRIEVAL_QUERY"
RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
SOURCE_CODE = [
    "def func(a, b): return a + b",
    "def func(a, b): return a - b",
    "def func(a, b): return (a ** 2 + b ** 2) ** 0.5",
]


def embed_test() -> (
    tuple[genai.types.EmbedContentResponse, genai.types.EmbedContentResponse]
):
    """Generates embeddings for source code indexing and code search queries using the Gemini API.

    Returns:
        tuple[genai.types.EmbedContentResponse, genai.types.EmbedContentResponse]: A tuple containing
        the final source code indexing response and search query embedding response.
    """
    client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION_ID)

    # Index Source Code
    for line in SOURCE_CODE:
        config = genai.types.EmbedContentConfig(task_type=RETRIEVAL_DOCUMENT)

        index_response = client.models.embed_content(
            model=MODEL_NAME, contents=line, config=config
        )

        print(
            f"Task: {RETRIEVAL_DOCUMENT} | "
            f"Vector length: {len(index_response.embeddings)} | "
            f"Preview: {index_response.embeddings[:3]}..."
        )

    # Embed Search Prompts
    for line in QUERY_LINES:
        config = genai.types.EmbedContentConfig(task_type=CODE_RETRIEVAL_QUERY)

        query_response = client.models.embed_content(
            model=MODEL_NAME, contents=line, config=config
        )

        print(
            f"Task: {CODE_RETRIEVAL_QUERY} | "
            f"Vector length: {len(query_response.embeddings)} | "
            f"Preview: {query_response.embeddings[:3]}..."
        )

    return index_response, query_response


# [END aiplatform_genai_embedding_code_retrieval]
