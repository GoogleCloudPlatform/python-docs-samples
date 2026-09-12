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

"""Unit tests for Vertex AI Search / Agent Search supportability code samples."""

import os
import unittest
from unittest import mock

from google.cloud import discoveryengine_v1 as discoveryengine
from google.longrunning import operations_pb2
from google.protobuf import any_pb2
from google.protobuf import struct_pb2
from google.rpc import status_pb2

import converse_conversation_sample
import create_document_metadata_sample
import enable_gemini_layout_parser_sample
import import_custom_chunks_sample
import poll_lro_robust_sample
import search_chunks_sample
import search_extractive_segments_sample
import update_data_store_gemini_parser_sample
import write_user_event_sample


class SupportabilitySamplesTest(unittest.TestCase):

  @mock.patch("google.cloud.discoveryengine_v1.SearchServiceClient")
  def test_search_with_extractive_segments(self, mock_client_cls):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_doc = discoveryengine.Document(
        id="doc-123",
        name="projects/p/locations/l/collections/c/dataStores/ds/branches/0/documents/doc-123",
        derived_struct_data={
            "title": "Alphabet 2024 Q4 Report",
            "link": "https://example.com/reports/2024_q4.pdf",
            "extractive_segments": [{
                "pageNumber": "12",
                "relevanceScore": 0.94,
                "content": "Cloud revenue increased 29% year over year.",
            }],
            "snippets": [{"snippet": "Cloud revenue <b>increased 29%</b>."}],
        },
    )

    mock_search_result = discoveryengine.SearchResponse.SearchResult(
        id="doc-123",
        document=mock_doc,
    )

    mock_response = discoveryengine.SearchResponse(
        results=[mock_search_result],
        attribution_token="test_attribution_token_123",
        total_size=1,
    )
    mock_client.search.return_value = mock_response

    response = (
        search_extractive_segments_sample.search_with_extractive_segments(
            project_id="test-project",
            location="global",
            engine_id="test-engine",
            search_query="Google Cloud revenue",
            data_store_ids=["chunked-ds", "unchunked-ds"],
        )
    )

    self.assertEqual(response, mock_response)
    mock_client.search.assert_called_once()
    call_args = mock_client.search.call_args[1]["request"]

    self.assertIn("engines/test-engine", call_args.serving_config)
    self.assertEqual(call_args.query, "Google Cloud revenue")
    extractive_spec = call_args.content_search_spec.extractive_content_spec
    self.assertEqual(extractive_spec.max_extractive_segment_count, 3)
    self.assertTrue(extractive_spec.return_extractive_segment_score)
    self.assertEqual(len(call_args.data_store_specs), 2)

  @mock.patch("google.cloud.discoveryengine_v1.UserEventServiceClient")
  def test_write_user_event_with_attribution_with_data_store(
      self, mock_client_cls
  ):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_doc_info = discoveryengine.DocumentInfo(
        name="projects/test-project/locations/global/collections/default_collection/dataStores/target-ds/branches/0/documents/doc_456"
    )
    mock_response = discoveryengine.UserEvent(
        event_type="view-item",
        user_pseudo_id="visitor_999",
        engine="projects/test-project/locations/global/collections/default_collection/engines/test-engine",
        data_store="projects/test-project/locations/global/collections/default_collection/dataStores/target-ds",
        attribution_token="search_token_abc",
        documents=[mock_doc_info],
    )
    mock_client.write_user_event.return_value = mock_response

    response = write_user_event_sample.write_user_event_with_attribution(
        project_id="test-project",
        location="global",
        engine_id="test-engine",
        user_pseudo_id="visitor_999",
        attribution_token="search_token_abc",
        document_id="doc_456",
        data_store_id="target-ds",
    )

    self.assertEqual(response, mock_response)
    mock_client.write_user_event.assert_called_once()
    req = mock_client.write_user_event.call_args[1]["request"]

    self.assertEqual(req.parent, "projects/test-project/locations/global")
    self.assertEqual(req.user_event.event_type, "view-item")
    self.assertEqual(req.user_event.attribution_token, "search_token_abc")
    self.assertEqual(req.user_event.user_pseudo_id, "visitor_999")
    self.assertIn("documents/doc_456", req.user_event.documents[0].name)
    self.assertIn("engines/test-engine", req.user_event.engine)
    self.assertIn("dataStores/target-ds", req.user_event.data_store)

  @mock.patch("google.cloud.discoveryengine_v1.UserEventServiceClient")
  def test_write_user_event_with_attribution_no_data_store(
      self, mock_client_cls
  ):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_doc_info = discoveryengine.DocumentInfo(id="doc_789")
    mock_response = discoveryengine.UserEvent(
        event_type="view-item",
        user_pseudo_id="visitor_111",
        engine="projects/test-project/locations/global/collections/default_collection/engines/test-engine",
        attribution_token="search_token_xyz",
        documents=[mock_doc_info],
    )
    mock_client.write_user_event.return_value = mock_response

    response = write_user_event_sample.write_user_event_with_attribution(
        project_id="test-project",
        location="global",
        engine_id="test-engine",
        user_pseudo_id="visitor_111",
        attribution_token="search_token_xyz",
        document_id="doc_789",
    )

    self.assertEqual(response, mock_response)
    mock_client.write_user_event.assert_called_once()
    req = mock_client.write_user_event.call_args[1]["request"]

    self.assertEqual(req.parent, "projects/test-project/locations/global")
    self.assertEqual(req.user_event.documents[0].id, "doc_789")
    self.assertFalse(req.user_event.data_store)

  @mock.patch(
      "google.cloud.discoveryengine_v1.ConversationalSearchServiceClient"
  )
  def test_converse_conversation_new_session(self, mock_client_cls):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_created_conv = discoveryengine.Conversation(
        name="projects/test-project/locations/global/collections/default_collection/dataStores/test-ds/conversations/conv-123"
    )
    mock_client.create_conversation.return_value = mock_created_conv

    mock_summary = discoveryengine.SearchResponse.Summary(
        summary_text="Vertex AI Search provides enterprise generative search."
    )
    mock_reply = discoveryengine.Reply(summary=mock_summary)
    mock_search_result = discoveryengine.SearchResponse.SearchResult(
        id="doc-1",
        document=discoveryengine.Document(
            id="doc-1",
            struct_data={
                "title": "VAIS Docs",
                "link": "https://cloud.google.com",
            },
        ),
    )
    mock_response = discoveryengine.ConverseConversationResponse(
        reply=mock_reply,
        conversation=mock_created_conv,
        search_results=[mock_search_result],
    )
    mock_client.converse_conversation.return_value = mock_response

    response = converse_conversation_sample.multi_turn_conversational_search(
        project_id="test-project",
        location="global",
        data_store_id="test-ds",
        query_text="What is Vertex AI Search?",
    )

    self.assertEqual(response, mock_response)
    mock_client.create_conversation.assert_called_once()
    mock_client.converse_conversation.assert_called_once()

  @mock.patch(
      "google.cloud.discoveryengine_v1.ConversationalSearchServiceClient"
  )
  def test_converse_conversation_existing_session(self, mock_client_cls):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_summary = discoveryengine.SearchResponse.Summary(
        summary_text="It also supports grounded citation parsing."
    )
    mock_reply = discoveryengine.Reply(summary=mock_summary)
    mock_response = discoveryengine.ConverseConversationResponse(
        reply=mock_reply,
        search_results=[],
    )
    mock_client.converse_conversation.return_value = mock_response

    response = converse_conversation_sample.multi_turn_conversational_search(
        project_id="test-project",
        location="global",
        data_store_id="test-ds",
        query_text="Tell me about citations.",
        conversation_id="conv-existing-999",
    )

    self.assertEqual(response, mock_response)
    mock_client.create_conversation.assert_not_called()
    mock_client.converse_conversation.assert_called_once()
    req = mock_client.converse_conversation.call_args[1]["request"]
    self.assertIn("conv-existing-999", req.name)

  @mock.patch("google.cloud.discoveryengine_v1.DocumentServiceClient")
  def test_create_structured_document_with_metadata(self, mock_client_cls):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_doc = discoveryengine.Document(
        id="doc-storage-01",
        name="projects/test-project/locations/global/collections/default_collection/dataStores/test-ds/branches/0/documents/doc-storage-01",
        struct_data={
            "title": "Cloud Storage Architecture",
            "url": "https://example.com/docs/gcs_storage_guide_v2",
            "category": "Storage",
            "rating": 4.9,
            "tags": ["gcs", "cloud", "infra"],
        },
    )
    mock_client.create_document.return_value = mock_doc

    response = (
        create_document_metadata_sample.create_structured_document_with_metadata(
            project_id="test-project",
            location="global",
            data_store_id="test-ds",
            document_id="doc-storage-01",
            title="Cloud Storage Architecture",
            uri="https://example.com/docs/gcs_storage_guide_v2",
            category="Storage",
            rating=4.9,
            tags=["gcs", "cloud", "infra"],
            content_text=(
                "Overview of Google Cloud Storage buckets and security."
            ),
        )
    )

    self.assertEqual(response, mock_doc)
    mock_client.create_document.assert_called_once()
    req = mock_client.create_document.call_args[1]["request"]
    self.assertIn("branches/0", req.parent)
    self.assertEqual(req.document_id, "doc-storage-01")
    self.assertEqual(
        req.document.struct_data.get("url"),
        "https://example.com/docs/gcs_storage_guide_v2",
    )
    self.assertEqual(req.document.content.mime_type, "text/plain")

  @mock.patch("google.cloud.discoveryengine_v1.DocumentServiceClient")
  def test_poll_long_running_operation_robust_success(self, mock_client_cls):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_op_running = operations_pb2.Operation(
        name="projects/p/locations/l/operations/op-123",
        done=False,
    )
    mock_metadata = any_pb2.Any(
        type_url="type.googleapis.com/google.cloud.discoveryengine.v1.ImportDocumentsMetadata"
    )
    mock_op_done = operations_pb2.Operation(
        name="projects/p/locations/l/operations/op-123",
        done=True,
        metadata=mock_metadata,
    )
    mock_client.transport.operations_client.get_operation.side_effect = [
        mock_op_running,
        mock_op_done,
    ]

    with mock.patch("time.sleep") as mock_sleep:
      op = poll_lro_robust_sample.poll_long_running_operation_robust(
          operation_name="projects/p/locations/l/operations/op-123",
          initial_delay_seconds=1.0,
          max_delay_seconds=5.0,
          timeout_seconds=30.0,
      )
      self.assertTrue(op.done)
      mock_sleep.assert_called_once()

  @mock.patch("google.cloud.discoveryengine_v1.DocumentServiceClient")
  def test_poll_long_running_operation_robust_error(self, mock_client_cls):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_op_failed = operations_pb2.Operation(
        name="projects/p/locations/l/operations/op-err",
        done=True,
        error=status_pb2.Status(code=3, message="Invalid GCS bucket uri"),
    )
    mock_client.transport.operations_client.get_operation.return_value = (
        mock_op_failed
    )

    with self.assertRaises(RuntimeError) as ctx:
      poll_lro_robust_sample.poll_long_running_operation_robust(
          operation_name="projects/p/locations/l/operations/op-err",
          timeout_seconds=30.0,
      )
    self.assertIn("Invalid GCS bucket uri", str(ctx.exception))

  @mock.patch("google.cloud.discoveryengine_v1.DocumentServiceClient")
  def test_poll_long_running_operation_robust_timeout(self, mock_client_cls):
    mock_client = mock.MagicMock()
    mock_client_cls.return_value = mock_client

    mock_op_running = operations_pb2.Operation(
        name="projects/p/locations/l/operations/op-timeout",
        done=False,
    )
    mock_client.transport.operations_client.get_operation.return_value = (
        mock_op_running
    )

    with mock.patch("time.time") as mock_time, mock.patch("time.sleep"):
      mock_time.side_effect = [0.0, 0.0, 10.0, 50.0]
      with self.assertRaises(TimeoutError):
        poll_lro_robust_sample.poll_long_running_operation_robust(
            operation_name="projects/p/locations/l/operations/op-timeout",
            timeout_seconds=20.0,
        )

  def test_create_data_store_with_gemini_parser(self):
    de = enable_gemini_layout_parser_sample.discoveryengine
    with mock.patch.object(de, "DataStoreServiceClient") as mock_client_cls:
      mock_client = mock.MagicMock()
      mock_client_cls.return_value = mock_client

      mock_ds = de.DataStore(
          name="projects/test-project/locations/global/collections/default_collection/dataStores/gemini-ds",
          display_name="Gemini Parsed DS",
      )
      mock_operation = mock.MagicMock()
      mock_operation.operation.name = (
          "projects/test-project/locations/global/operations/op-ds-create"
      )
      mock_operation.result.return_value = mock_ds
      mock_client.create_data_store.return_value = mock_operation

      response = enable_gemini_layout_parser_sample.create_data_store_with_gemini_parser(
          project_id="test-project",
          location="global",
          data_store_id="gemini-ds",
          display_name="Gemini Parsed DS",
          enable_table_annotation=True,
          enable_image_annotation=True,
      )

      self.assertEqual(response, mock_ds)
      mock_client.create_data_store.assert_called_once()
      req = mock_client.create_data_store.call_args[1]["request"]
      self.assertEqual(req.data_store_id, "gemini-ds")
      self.assertEqual(req.data_store.display_name, "Gemini Parsed DS")

      layout_cfg = (
          req.data_store.document_processing_config.default_parsing_config.layout_parsing_config
      )
      self.assertTrue(layout_cfg.enable_llm_layout_parsing)
      self.assertTrue(layout_cfg.enable_table_annotation)
      self.assertTrue(layout_cfg.enable_image_annotation)

      chunking_cfg = (
          req.data_store.document_processing_config.chunking_config.layout_based_chunking_config
      )
      self.assertEqual(chunking_cfg.chunk_size, 500)
      self.assertTrue(chunking_cfg.include_ancestor_headings)

  def test_update_data_store_gemini_parser(self):
    de = update_data_store_gemini_parser_sample.discoveryengine
    with mock.patch.object(de, "DataStoreServiceClient") as mock_client_cls:
      mock_client = mock.MagicMock()
      mock_client_cls.return_value = mock_client

      mock_ds = de.DataStore(
          name="projects/test-project/locations/global/collections/default_collection/dataStores/gemini-ds",
          display_name="Gemini Parsed DS",
      )
      mock_client.update_data_store.return_value = mock_ds

      response = (
          update_data_store_gemini_parser_sample.update_data_store_gemini_parser(
              project_id="test-project",
              location="global",
              data_store_id="gemini-ds",
              enable_table_annotation=True,
              enable_image_annotation=True,
          )
      )

      self.assertEqual(response, mock_ds)
      mock_client.update_data_store.assert_called_once()
      req = mock_client.update_data_store.call_args[1]["request"]
      self.assertIn("dataStores/gemini-ds", req.data_store.name)
      self.assertEqual(
          list(req.update_mask.paths), ["document_processing_config"]
      )
      layout_cfg = (
          req.data_store.document_processing_config.default_parsing_config.layout_parsing_config
      )
      self.assertTrue(layout_cfg.enable_llm_layout_parsing)
      self.assertTrue(layout_cfg.enable_table_annotation)
      self.assertTrue(layout_cfg.enable_image_annotation)

  def test_import_custom_chunk_documents(self):
    de = import_custom_chunks_sample.discoveryengine
    with mock.patch.object(de, "DocumentServiceClient") as mock_client_cls:
      mock_client = mock.MagicMock()
      mock_client_cls.return_value = mock_client

      mock_op = mock.MagicMock()
      mock_op.operation.name = "projects/test-project/locations/global/collections/default_collection/dataStores/test-ds/branches/0/operations/op-byoc-123"
      mock_client.import_documents.return_value = mock_op

      response = import_custom_chunks_sample.import_custom_chunk_documents(
          project_id="test-project",
          location="global",
          data_store_id="test-ds",
          gcs_uri="gs://my-bucket/custom_chunks/*.json",
      )

      self.assertEqual(response, mock_op)
      mock_client.import_documents.assert_called_once()
      req = mock_client.import_documents.call_args[1]["request"]
      self.assertIn("dataStores/test-ds/branches/0", req.parent)
      self.assertEqual(
          req.gcs_source.input_uris, ["gs://my-bucket/custom_chunks/*.json"]
      )
      self.assertEqual(req.gcs_source.data_schema, "custom")
      self.assertEqual(
          req.reconciliation_mode,
          de.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
      )

  def test_search_chunks_with_metadata(self):
    de = search_chunks_sample.discoveryengine
    with mock.patch.object(de, "SearchServiceClient") as mock_client_cls:
      mock_client = mock.MagicMock()
      mock_client_cls.return_value = mock_client

      doc_metadata = de.Chunk.DocumentMetadata(
          title="Discovery Engine Deep Dive",
          uri="https://cloud.google.com/generative-ai-app-builder/docs/parse-chunk-documents",
          struct_data={"category": "Enterprise Search", "rating": 4.9},
      )

      prev_chunk = de.Chunk(id="c1", content="Preceding context on indexing.")
      next_chunk = de.Chunk(id="c3", content="Succeeding context on ranking.")

      chunk_meta = de.Chunk.ChunkMetadata(
          previous_chunks=[prev_chunk],
          next_chunks=[next_chunk],
      )

      mock_chunk = de.Chunk(
          id="c2",
          name="projects/test-p/locations/global/collections/default_collection/dataStores/chunk-ds/branches/0/documents/doc1/chunks/c2",
          content=(
              "Main relevant chunk discussing layout-aware document chunking."
          ),
          relevance_score=0.965,
          document_metadata=doc_metadata,
          page_span=de.Chunk.PageSpan(page_start=5, page_end=6),
          chunk_metadata=chunk_meta,
      )

      mock_search_result = de.SearchResponse.SearchResult(
          id="doc1",
          chunk=mock_chunk,
      )

      mock_response = de.SearchResponse(
          results=[mock_search_result],
          attribution_token="test_attribution_token_chunk_999",
          total_size=1,
      )
      mock_client.search.return_value = mock_response

      response = search_chunks_sample.search_chunks_with_metadata(
          project_id="test-p",
          location="global",
          data_store_id="chunk-ds",
          search_query="how to use chunking",
          num_previous_chunks=1,
          num_next_chunks=1,
          filter_expr='category: ANY("Enterprise Search")',
      )

      self.assertEqual(response, mock_response)
      mock_client.search.assert_called_once()
      req = mock_client.search.call_args[1]["request"]
      self.assertEqual(req.query, "how to use chunking")
      self.assertEqual(req.filter, 'category: ANY("Enterprise Search")')
      self.assertEqual(
          req.content_search_spec.search_result_mode,
          de.SearchRequest.ContentSearchSpec.SearchResultMode.CHUNKS,
      )
      self.assertEqual(
          req.content_search_spec.chunk_spec.num_previous_chunks, 1
      )
      self.assertEqual(req.content_search_spec.chunk_spec.num_next_chunks, 1)


if __name__ == "__main__":
  unittest.main()
