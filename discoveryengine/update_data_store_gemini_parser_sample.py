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

"""Gemini Advanced Layout Parser update sample for Agent Search."""

# [START genappbuilder_update_data_store_gemini_parser]
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1beta as discoveryengine
from google.protobuf import field_mask_pb2

FieldMask = field_mask_pb2.FieldMask


def update_data_store_gemini_parser(
    project_id: str,
    location: str,
    data_store_id: str,
    enable_table_annotation: bool = True,
    enable_image_annotation: bool = True,
) -> discoveryengine.DataStore:
  """Updates an existing DataStore to enable Gemini Advanced Layout Parsing.

  Updating DocumentProcessingConfig modifies how subsequent document imports
  are parsed and chunked. Previously ingested documents are not automatically
  re-parsed; to apply Gemini layout parsing to existing documents, re-import
  them after updating the config.

  Args:
      project_id: Google Cloud project ID.
      location: DataStore location (e.g., 'global', 'us', 'eu').
      data_store_id: Unique identifier of the existing DataStore.
      enable_table_annotation: Whether to generate LLM descriptions for tables.
      enable_image_annotation: Whether to generate LLM descriptions for images.

  Returns:
      The updated DataStore resource.
  """
  client_options = (
      ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
      if location != "global"
      else None
  )
  client = discoveryengine.DataStoreServiceClient(client_options=client_options)

  data_store_name = (
      f"projects/{project_id}/locations/{location}/collections/default_collection/"
      f"dataStores/{data_store_id}"
  )

  # 1. Build LayoutParsingConfig with Gemini enhancement
  layout_parsing_config = discoveryengine.DocumentProcessingConfig.ParsingConfig.LayoutParsingConfig(
      enable_llm_layout_parsing=True,
      enable_table_annotation=enable_table_annotation,
      enable_image_annotation=enable_image_annotation,
  )

  parsing_config = discoveryengine.DocumentProcessingConfig.ParsingConfig(
      layout_parsing_config=layout_parsing_config
  )

  # 2. Build updated DocumentProcessingConfig
  doc_processing_config = discoveryengine.DocumentProcessingConfig(
      default_parsing_config=parsing_config,
  )

  # 3. Construct DataStore with field mask for document_processing_config
  data_store = discoveryengine.DataStore(
      name=data_store_name,
      document_processing_config=doc_processing_config,
  )
  field_mask = FieldMask(paths=["document_processing_config"])

  request = discoveryengine.UpdateDataStoreRequest(
      data_store=data_store,
      update_mask=field_mask,
  )

  updated_data_store = client.update_data_store(request=request)
  print("Successfully updated DataStore to Gemini Parser:")
  print(f"  Name: {updated_data_store.name}")
  print("  Default Parser: LayoutParser (Gemini LLM-enhanced)")

  return updated_data_store


# [END genappbuilder_update_data_store_gemini_parser]
