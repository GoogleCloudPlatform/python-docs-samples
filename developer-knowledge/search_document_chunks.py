# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START developerknowledge_search_document_chunks]
from google.cloud import developer_knowledge_v1


def search_document_chunks(
    query: str = "How to create a Cloud Storage bucket",
    page_size: int = 5,
) -> developer_knowledge_v1.SearchDocumentChunksResponse:
    """Searches developer documentation chunks for a given query.

    Args:
        query: The natural language search query.
        page_size: The maximum number of document chunks to return.

    Returns:
        The SearchDocumentChunksResponse containing relevant document chunks.
    """
    client = developer_knowledge_v1.DeveloperKnowledgeClient()

    request = developer_knowledge_v1.SearchDocumentChunksRequest(
        query=query,
        page_size=page_size,
    )

    response = client.search_document_chunks(request=request)

    for chunk in response.results:
        print(f"Parent Document: {chunk.parent}")
        print(f"Chunk ID: {chunk.id}")
        print(f"Content: {chunk.content[:100]}...\n")

    return response


# [END developerknowledge_search_document_chunks]

if __name__ == "__main__":
    search_document_chunks()
