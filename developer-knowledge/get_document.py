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

# [START developerknowledge_get_document]
from google.cloud import developer_knowledge_v1


def get_document(
    name: str = "documents/docs.cloud.google.com/storage/docs/creating-buckets",
) -> developer_knowledge_v1.Document:
    """Retrieves a single developer documentation page by its resource name.

    Args:
        name: The resource name of the document in format
            'documents/{uri_without_scheme}'.

    Returns:
        The Document containing the full Markdown content and metadata.
    """
    client = developer_knowledge_v1.DeveloperKnowledgeClient()

    request = developer_knowledge_v1.GetDocumentRequest(
        name=name,
    )

    document = client.get_document(request=request)

    print(f"Title: {document.title}")
    print(f"URI: {document.uri}")
    print(f"Data Source: {document.data_source}")
    print(f"Content Length: {document.content_length_bytes} bytes")
    print(f"Content Preview: {document.content[:150]}...\n")

    return document


# [END developerknowledge_get_document]

if __name__ == "__main__":
    get_document()
