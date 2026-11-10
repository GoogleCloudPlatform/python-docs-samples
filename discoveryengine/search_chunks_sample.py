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

"""Search chunks and parent metadata sample for Agent Search."""

# [START genappbuilder_search_chunks]
from typing import Optional

from google.cloud import discoveryengine_v1 as discoveryengine


def search_chunks_with_metadata(
    project_id: str,
    location: str,
    data_store_id: str,
    search_query: str,
    num_previous_chunks: int = 1,
    num_next_chunks: int = 1,
    filter_expr: Optional[str] = None,
    page_size: int = 5,
) -> discoveryengine.SearchResponse:
  """Searches a chunk-enabled data store and parses chunk content and parent metadata.

  When searching a data store with document chunking enabled:
  1. Search results populate `result.chunk` rather than `result.document`.
  2. Parent document metadata (such as `title`, preserved `uri`, or custom
     `struct_data`) must be retrieved via `result.chunk.document_metadata`.
  3. `chunk_spec` enables windowing with adjacent chunks (`previous_chunks`,
     `next_chunks`) to provide broader context to downstream LLM prompts without
     losing fine-grained relevance.

  Args:
      project_id: Google Cloud project ID or project number.
      location: Data store location (e.g., 'global', 'us', 'eu').
      data_store_id: Target data store ID.
      search_query: The search query string.
      num_previous_chunks: Number of preceding adjacent chunks to return (0-5).
      num_next_chunks: Number of succeeding adjacent chunks to return (0-5).
      filter_expr: Optional filter expression targeting parent structured
        metadata.
      page_size: Number of chunk results to return per page.

  Returns:
      The SearchResponse proto.
  """
  client = discoveryengine.SearchServiceClient()

  serving_config = (
      f"projects/{project_id}/locations/{location}/collections/default_collection"
      f"/dataStores/{data_store_id}/servingConfigs/default_search"
  )

  # Configure search request for chunk retrieval with adjacent chunk context
  content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
      search_result_mode=discoveryengine.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS,
      chunk_spec=discoveryengine.SearchRequest.ContentSearchSpec.ChunkSpec(
          num_previous_chunks=num_previous_chunks,
          num_next_chunks=num_next_chunks,
      ),
  )

  request = discoveryengine.SearchRequest(
      serving_config=serving_config,
      query=search_query,
      page_size=page_size,
      content_search_spec=content_search_spec,
      filter=filter_expr,
  )

  response = client.search(request=request)

  print(f"Search query: '{search_query}'")
  print(f"Total results: {len(response.results)}")
  print(f"Attribution Token: {response.attribution_token}")

  for idx, result in enumerate(response.results, start=1):
    chunk = result.chunk
    doc_metadata = chunk.document_metadata if chunk else None

    print(f"\n--- Result #{idx} ---")
    if not chunk:
      print("  (Result did not contain chunk data)")
      continue

    print(f"  Chunk ID: {chunk.id}")
    print(f"  Relevance Score: {chunk.relevance_score:.4f}")

    # Parent document metadata
    if doc_metadata:
      print(f"  Parent Title: {doc_metadata.title}")
      print(f"  Parent URI: {doc_metadata.uri}")
      if doc_metadata.struct_data:
        print(f"  Parent Structured Data: {dict(doc_metadata.struct_data)}")

    # Page span
    if chunk.page_span:
      print(
          f"  Page Span: {chunk.page_span.page_start} -"
          f" {chunk.page_span.page_end}"
      )

    # Primary chunk text content
    content_preview = (
        chunk.content[:150].replace("\n", " ") if chunk.content else ""
    )
    print(f"  Chunk Content: {content_preview}...")

    # Adjacent chunks for expanded LLM context
    if chunk.chunk_metadata:
      prev_count = len(chunk.chunk_metadata.previous_chunks)
      next_count = len(chunk.chunk_metadata.next_chunks)
      print(
          f"  Adjacent Context: {prev_count} previous chunk(s), {next_count}"
          " next chunk(s)"
      )

  return response


# [END genappbuilder_search_chunks]
