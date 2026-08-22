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

"""Pytest configuration and local fallback mocks for developer_knowledge_v1."""

import sys
from unittest.mock import MagicMock

try:
    from google.cloud import developer_knowledge_v1  # noqa: F401
except ImportError:
    mock_dk = MagicMock()

    class SearchDocumentChunksRequest:
        def __init__(self, query="", page_size=5, page_token="", filter=""):
            self.query = query
            self.page_size = page_size
            self.page_token = page_token
            self.filter = filter

    class GetDocumentRequest:
        def __init__(self, name=""):
            self.name = name

    class BatchGetDocumentsRequest:
        def __init__(self, names=None):
            self.names = names or []

    class AnswerQueryRequest:
        def __init__(self, query="", filter=""):
            self.query = query
            self.filter = filter

    class DocumentChunk:
        def __init__(
            self,
            parent="documents/docs.cloud.google.com/storage/docs/creating-buckets",
            id="chunk-1",
            content="To create a bucket, use the Google Cloud console or gcloud CLI.",
        ):
            self.parent = parent
            self.id = id
            self.content = content

    class Document:
        def __init__(
            self,
            name="documents/docs.cloud.google.com/storage/docs/creating-buckets",
            title="Creating Buckets",
            uri="docs.cloud.google.com/storage/docs/creating-buckets",
            data_source="docs.cloud.google.com",
            content_length_bytes=1024,
            content="# Creating Buckets...",
        ):
            self.name = name
            self.title = title
            self.uri = uri
            self.data_source = data_source
            self.content_length_bytes = content_length_bytes
            self.content = content

    class Answer:
        def __init__(
            self,
            answer_text=(
                "Use `gcloud storage buckets create` to create a new storage"
                " bucket."
            ),
            citations=None,
            references=None,
        ):
            self.answer_text = answer_text
            self.citations = citations or []
            self.references = references or []

    class SearchDocumentChunksResponse:
        def __init__(self, results=None):
            self.results = results or [
                DocumentChunk()
            ]

    class BatchGetDocumentsResponse:
        def __init__(self, documents=None):
            self.documents = documents or []

    class AnswerQueryResponse:
        def __init__(self, answer=None):
            self.answer = answer or Answer()

    class DeveloperKnowledgeClient:
        def search_document_chunks(self, request=None):
            return SearchDocumentChunksResponse()

        def get_document(self, request=None):
            name = (
                request.name
                if request and request.name
                else "documents/docs.cloud.google.com/storage/docs/creating-buckets"
            )
            return Document(name=name)

        def batch_get_documents(self, request=None):
            names = request.names if request and request.names else []
            docs = [Document(name=n, title=f"Doc {n}") for n in names]
            return BatchGetDocumentsResponse(documents=docs)

        def answer_query(self, request=None):
            return AnswerQueryResponse()

    mock_dk.DeveloperKnowledgeClient = DeveloperKnowledgeClient
    mock_dk.SearchDocumentChunksRequest = SearchDocumentChunksRequest
    mock_dk.GetDocumentRequest = GetDocumentRequest
    mock_dk.BatchGetDocumentsRequest = BatchGetDocumentsRequest
    mock_dk.AnswerQueryRequest = AnswerQueryRequest
    mock_dk.SearchDocumentChunksResponse = SearchDocumentChunksResponse
    mock_dk.BatchGetDocumentsResponse = BatchGetDocumentsResponse
    mock_dk.AnswerQueryResponse = AnswerQueryResponse
    mock_dk.Document = Document
    mock_dk.DocumentChunk = DocumentChunk

    mock_google = MagicMock()
    mock_cloud = MagicMock()
    mock_cloud.developer_knowledge_v1 = mock_dk
    mock_google.cloud = mock_cloud

    sys.modules["google"] = mock_google
    sys.modules["google.cloud"] = mock_cloud
    sys.modules["google.cloud.developer_knowledge_v1"] = mock_dk
