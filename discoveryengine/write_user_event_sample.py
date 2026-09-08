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

"""User event recording with search attribution sample for Agent Search."""

# [START genappbuilder_write_user_event]
import time
from typing import Optional

from google.cloud import discoveryengine_v1 as discoveryengine
from google.protobuf import timestamp_pb2


def write_user_event_with_attribution(
    project_id: str,
    location: str,
    engine_id: str,
    user_pseudo_id: str,
    attribution_token: str,
    document_id: str,
    event_type: str = "view-item",
    data_store_id: Optional[str] = None,
) -> discoveryengine.UserEvent:
  """Records a real-time user event scoped to an engine with search attribution.

  To ensure analytics pipelines correctly attribute click events with preceding
  search queries and maintain accurate Click-Through Rate (CTR) analytics:
  1. Ingest events at the Location level:
     `projects/{project}/locations/{location}`
  2. Populate the `engine` resource field on the `UserEvent` proto.
  3. Pass the exact `attribution_token` from the corresponding `SearchResponse`.
  4. Populate the `documents` list with the clicked document ID.

  Args:
      project_id: Google Cloud project ID or project number.
      location: Engine location (e.g., 'global', 'us', 'eu').
      engine_id: Search engine (app) ID.
      user_pseudo_id: Uniquely pseudonymized visitor/session identifier.
      attribution_token: Token received from the preceding search response.
      document_id: ID of the document viewed or clicked.
      event_type: Event type (e.g., 'view-item', 'search', 'view-category').
      data_store_id: Optional specific data store ID associated with the doc.

  Returns:
      The recorded UserEvent.
  """
  client = discoveryengine.UserEventServiceClient()

  # CRITICAL: Always use the Location-level parent for Engine-scoped events
  parent = f"projects/{project_id}/locations/{location}"

  engine_path = (
      f"projects/{project_id}/locations/{location}/collections/default_collection"
      f"/engines/{engine_id}"
  )

  # Set accurate UTC event timestamp
  current_time = time.time()
  event_time = timestamp_pb2.Timestamp(
      seconds=int(current_time),
      nanos=int((current_time - int(current_time)) * 1e9),
  )

  # Build DocumentInfo reference for the clicked/viewed item
  if document_id.startswith("projects/"):
    document_info = discoveryengine.DocumentInfo(name=document_id)
  elif data_store_id:
    doc_name = (
        f"projects/{project_id}/locations/{location}/collections/default_collection"
        f"/dataStores/{data_store_id}/branches/0/documents/{document_id}"
    )
    document_info = discoveryengine.DocumentInfo(name=doc_name)
  else:
    document_info = discoveryengine.DocumentInfo(id=document_id)

  user_event = discoveryengine.UserEvent(
      event_type=event_type,
      user_pseudo_id=user_pseudo_id,
      engine=engine_path,
      attribution_token=attribution_token,
      documents=[document_info],
      event_time=event_time,
      user_info=discoveryengine.UserInfo(
          user_id=f"user_{user_pseudo_id}",
          user_agent=(
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          ),
      ),
      page_info=discoveryengine.PageInfo(
          uri="https://example.com/search/results",
          pageview_id="pageview_12345",
      ),
  )

  if data_store_id:
    user_event.data_store = (
        f"projects/{project_id}/locations/{location}/collections/default_collection"
        f"/dataStores/{data_store_id}"
    )

  request = discoveryengine.WriteUserEventRequest(
      parent=parent,
      user_event=user_event,
  )

  response = client.write_user_event(request=request)

  print(f"Recorded User Event '{response.event_type}':")
  print(f"  User Pseudo ID: {response.user_pseudo_id}")
  print(f"  Engine: {response.engine}")
  print(f"  Attribution Token: {response.attribution_token}")
  print(f"  Documents: {[doc.id or doc.name for doc in response.documents]}")
  print(f"  Event Time: {response.event_time}")

  return response


# [END genappbuilder_write_user_event]
