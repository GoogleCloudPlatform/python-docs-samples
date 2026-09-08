# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Document metadata ingestion sample for Agent Search."""

# [START genappbuilder_create_document_metadata]
from typing import List, Optional

from google.cloud import discoveryengine_v1 as discoveryengine


def create_structured_document_with_metadata(
    project_id: str,
    location: str,
    data_store_id: str,
    document_id: str,
    title: str,
    uri: str,
    category: str,
    rating: float,
    tags: List[str],
    content_text: Optional[str] = None,
) -> discoveryengine.Document:
  """Creates a document with custom structured metadata and content.

  When ingesting documents into Agent Search, passing authoritative
  metadata in `struct_data` provides key benefits:
  1. Prevents URI corruption: LLM layout parsers often strip underscores
     from URLs during markdown translation. Explicitly passing `uri` in
     `struct_data` guarantees exact URL preservation for frontend rendering.
  2. Schema Alignment: Explicit metadata attributes (categories, numeric
     ratings, tags) enable exact filtering and faceting in search queries.
  3. Chunking Inheritance: When ingested into a data store with document
     chunking enabled, `struct_data` is preserved on the parent document. In
     chunk search results (`searchResultMode=CHUNKS`), access metadata via
     `result.chunk.document_metadata.struct_data`.

  Args:
      project_id: Google Cloud project ID or project number.
      location: Data store location (e.g., 'global', 'us', 'eu').
      data_store_id: Target data store ID.
      document_id: Unique document identifier.
      title: Title of the document.
      uri: Original document URL or Cloud Storage URI (exact string preserved).
      category: Document taxonomy/category for faceted filtering.
      rating: Numerical score/rating for numerical filtering.
      tags: List of string tags/keywords.
      content_text: Optional raw text body for full-text indexing.

  Returns:
      The created Document proto.
  """
  client = discoveryengine.DocumentServiceClient()

  # Document branch 0 is the default serving branch
  parent = (
      f"projects/{project_id}/locations/{location}/collections/default_collection"
      f"/dataStores/{data_store_id}/branches/0"
  )

  # Build structured metadata dictionary
  metadata = {
      "title": title,
      "url": uri,
      "category": category,
      "rating": rating,
      "tags": tags,
  }

  document = discoveryengine.Document(
      id=document_id,
      struct_data=metadata,
  )

  # Optional unstructured text content
  if content_text:
    document.content = discoveryengine.Document.Content(
        mime_type="text/plain",
        raw_bytes=content_text.encode("utf-8"),
    )

  request = discoveryengine.CreateDocumentRequest(
      parent=parent,
      document=document,
      document_id=document_id,
  )

  response = client.create_document(request=request)

  print(f"Created Document ID: {response.id}")
  print(f"  Name: {response.name}")
  print(f"  Metadata URL (exact): {response.struct_data.get('url')}")
  print(f"  Category: {response.struct_data.get('category')}")
  print(f"  Rating: {response.struct_data.get('rating')}")
  print(f"  Tags: {response.struct_data.get('tags')}")

  return response


# [END genappbuilder_create_document_metadata]
