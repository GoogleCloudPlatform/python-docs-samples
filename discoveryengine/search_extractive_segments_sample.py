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

"""Search with extractive segments sample for Agent Search."""

# [START genappbuilder_search_extractive_segments]
from typing import List, Optional

from google.cloud import discoveryengine_v1 as discoveryengine


def search_with_extractive_segments(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
    data_store_ids: Optional[List[str]] = None,
) -> discoveryengine.SearchResponse:
  """Performs a search query using extractive segments across one or more data stores.

  Using Extractive Segments (`max_extractive_segment_count`) enables
  multi-datastore
  blended search across chunked and unchunked data stores uniformly.
  Extractive Segments work across all data store configurations and are
  array-order
  independent, returning exact source passages from indexed documents.

  Args:
      project_id: Google Cloud project ID or project number.
      location: Data store location (e.g., 'global', 'us', 'eu').
      engine_id: Search engine (app) ID.
      search_query: The search text query.
      data_store_ids: Optional list of specific data store IDs to blend.

  Returns:
      SearchResponse containing results with extractive segments.
  """
  client = discoveryengine.SearchServiceClient()

  serving_config = (
      f"projects/{project_id}/locations/{location}/collections/default_collection"
      f"/engines/{engine_id}/servingConfigs/default_search"
  )

  # Configure Extractive Content Spec for segments
  content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
      extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
          max_extractive_segment_count=3,
          return_extractive_segment_score=True,
          num_previous_segments=1,
          num_next_segments=1,
      ),
      snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
          return_snippet=True
      ),
  )

  # Optional multi-datastore scoping
  data_store_specs = []
  if data_store_ids:
    for ds_id in data_store_ids:
      ds_path = (
          f"projects/{project_id}/locations/{location}"
          f"/collections/default_collection/dataStores/{ds_id}"
      )
      data_store_specs.append(
          discoveryengine.SearchRequest.DataStoreSpec(data_store=ds_path)
      )

  request = discoveryengine.SearchRequest(
      serving_config=serving_config,
      query=search_query,
      page_size=10,
      content_search_spec=content_search_spec,
      data_store_specs=data_store_specs if data_store_specs else None,
  )

  response = client.search(request=request)

  print(f"Search Results for query '{search_query}':")
  print(f"Attribution Token: {response.attribution_token}")
  print(f"Total Results: {response.total_size}")

  for result in response.results:
    doc = result.document
    print(f"\n- Document ID: {doc.id}")
    print(f"  Name: {doc.name}")

    derived_data = doc.derived_struct_data
    raw_data = doc.struct_data

    # Retrieve title and URI from derived metadata or raw document struct_data
    title = "No Title"
    link = "No Link"
    if derived_data:
      title = derived_data.get("title") or title
      link = derived_data.get("link") or derived_data.get("url") or link
    if raw_data:
      if title == "No Title":
        title = raw_data.get("title") or title
      if link == "No Link":
        link = raw_data.get("link") or raw_data.get("url") or link

    print(f"  Title: {title}")
    print(f"  Link: {link}")

    # Extract Extractive Segments
    if derived_data and "extractive_segments" in derived_data:
      segments = derived_data.get("extractive_segments", [])
      for idx, segment in enumerate(segments, 1):
        page_number = segment.get("pageNumber", "N/A")
        relevance_score = segment.get("relevanceScore", "N/A")
        content = segment.get("content", "")
        print(
            f"  [Segment {idx}] (Page: {page_number}, Score:"
            f" {relevance_score}):"
        )
        print(f"    {content.strip()}")

    # Extract HTML snippets with highlighting
    if derived_data and "snippets" in derived_data:
      snippets = derived_data.get("snippets", [])
      for idx, snippet_entry in enumerate(snippets, 1):
        snippet_text = snippet_entry.get("snippet", "")
        print(f"  [Snippet {idx}]: {snippet_text.strip()}")

  return response


# [END genappbuilder_search_extractive_segments]
