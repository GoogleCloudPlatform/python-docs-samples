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

# [START developerknowledge_batch_get_documents]
from typing import List, Optional
from google.cloud import developer_knowledge_v1


def batch_get_documents(
    names: Optional[List[str]] = None,
) -> developer_knowledge_v1.BatchGetDocumentsResponse:
    """Retrieves multiple developer documentation pages in a single request.

    Args:
        names: A list of resource names in format 'documents/{uri_without_scheme}'.

    Returns:
        The BatchGetDocumentsResponse containing the retrieved documents.
    """
    if names is None:
        names = [
            "documents/docs.cloud.google.com/storage/docs/creating-buckets",
            "documents/docs.cloud.google.com/storage/docs/deleting-buckets",
        ]

    client = developer_knowledge_v1.DeveloperKnowledgeClient()

    request = developer_knowledge_v1.BatchGetDocumentsRequest(
        names=names,
    )

    response = client.batch_get_documents(request=request)

    for doc in response.documents:
        print(f"Title: {doc.title}")
        print(f"URI: {doc.uri}")
        print(f"Content Length: {doc.content_length_bytes} bytes\n")

    return response


# [END developerknowledge_batch_get_documents]

if __name__ == "__main__":
    batch_get_documents()
