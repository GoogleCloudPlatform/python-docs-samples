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

"""Gemini Advanced Layout Parser creation sample for Agent Search."""

# [START genappbuilder_enable_gemini_layout_parser]
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1beta as discoveryengine


def create_data_store_with_gemini_parser(
    project_id: str,
    location: str,
    data_store_id: str,
    display_name: str,
    enable_table_annotation: bool = True,
    enable_image_annotation: bool = True,
) -> discoveryengine.DataStore:
  """Creates a DataStore configured with Gemini Advanced Layout Parser (Pre-GA / Preview).

  Gemini layout parsing ('enable_llm_layout_parsing=True') uses Gemini
  multimodal
  models to provide superior table extraction, reading order analysis, and
  optical
  character recognition on PDFs. When combined with 'LayoutBasedChunkingConfig',
  it ensures structural elements like tables, lists, and sections are parsed
  cleanly
  for downstream RAG and answer generation.

  Args:
      project_id: Google Cloud project ID.
      location: DataStore location (e.g., 'global', 'us', 'eu').
      data_store_id: Unique identifier for the DataStore.
      display_name: Human-readable display name for the DataStore.
      enable_table_annotation: Whether to generate LLM descriptions for
        extracted tables.
      enable_image_annotation: Whether to generate LLM descriptions for
        extracted images.

  Returns:
      The created DataStore object (or the Long-Running Operation result).
  """
  client_options = (
      ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
      if location != "global"
      else None
  )
  client = discoveryengine.DataStoreServiceClient(client_options=client_options)

  parent = f"projects/{project_id}/locations/{location}/collections/default_collection"

  # 1. Configure Layout Parsing with Gemini LLM Enhancement
  layout_parsing_config = discoveryengine.DocumentProcessingConfig.ParsingConfig.LayoutParsingConfig(
      enable_llm_layout_parsing=True,  # Enables Gemini LLM-based layout parsing
      enable_table_annotation=enable_table_annotation,
      enable_image_annotation=enable_image_annotation,
  )

  parsing_config = discoveryengine.DocumentProcessingConfig.ParsingConfig(
      layout_parsing_config=layout_parsing_config
  )

  # 2. Configure Layout-Based Chunking for RAG
  chunking_config = discoveryengine.DocumentProcessingConfig.ChunkingConfig(
      layout_based_chunking_config=discoveryengine.DocumentProcessingConfig.ChunkingConfig.LayoutBasedChunkingConfig(
          chunk_size=500,
          include_ancestor_headings=True,
      )
  )

  # 3. Assemble DocumentProcessingConfig
  doc_processing_config = discoveryengine.DocumentProcessingConfig(
      default_parsing_config=parsing_config,
      chunking_config=chunking_config,
  )

  # 4. Construct DataStore
  data_store = discoveryengine.DataStore(
      display_name=display_name,
      industry_vertical=discoveryengine.IndustryVertical.GENERIC,
      solution_types=[discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH],
      content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED,
      document_processing_config=doc_processing_config,
  )

  request = discoveryengine.CreateDataStoreRequest(
      parent=parent,
      data_store=data_store,
      data_store_id=data_store_id,
  )

  operation = client.create_data_store(request=request)
  print(f"Waiting for DataStore creation operation: {operation.operation.name}")
  created_data_store = operation.result()

  print("Successfully created DataStore with Gemini Layout Parser:")
  print(f"  Name: {created_data_store.name}")
  print(f"  Display Name: {created_data_store.display_name}")

  return created_data_store


# [END genappbuilder_enable_gemini_layout_parser]
