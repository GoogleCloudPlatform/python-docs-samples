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

"""Multi-turn conversational search sample for Agent Search."""

# [START genappbuilder_converse_conversation]
from typing import Optional

from google.cloud import discoveryengine_v1 as discoveryengine


def multi_turn_conversational_search(
    project_id: str,
    location: str,
    data_store_id: str,
    query_text: str,
    conversation_id: Optional[str] = None,
    user_pseudo_id: str = "user_pseudo_id_12345",
) -> discoveryengine.ConverseConversationResponse:
  """Performs a multi-turn conversational search with session management and citation parsing.

  Multi-turn conversational search maintains conversational context across
  user interactions:
  1. Create a Conversation session with
     `ConversationalSearchServiceClient.create_conversation()`.
  2. Pass the conversation `name` in subsequent `ConverseConversationRequest`
     calls.
  3. Parse citations and search results to display grounded source references.

  Args:
      project_id: Google Cloud project ID or project number.
      location: Data store location (e.g., 'global', 'us', 'eu').
      data_store_id: Data store ID.
      query_text: Natural language user question or follow-up query.
      conversation_id: Optional existing conversation ID to continue a session.
      user_pseudo_id: Unique visitor/user identifier.

  Returns:
      ConverseConversationResponse containing the answer and grounded citations.
  """
  client = discoveryengine.ConversationalSearchServiceClient()

  parent = (
      f"projects/{project_id}/locations/{location}/collections/default_collection"
      f"/dataStores/{data_store_id}"
  )

  serving_config = f"{parent}/servingConfigs/default_search"

  # Step 1: Create a new Conversation session if not provided
  if not conversation_id:
    conversation = discoveryengine.Conversation(
        user_pseudo_id=user_pseudo_id,
        state=discoveryengine.Conversation.State.IN_PROGRESS,
    )
    created_conversation = client.create_conversation(
        parent=parent,
        conversation=conversation,
    )
    conversation_name = created_conversation.name
    print(f"Created new conversation session: {conversation_name}")
  else:
    conversation_name = (
        f"{parent}/conversations/{conversation_id}"
        if not conversation_id.startswith("projects/")
        else conversation_id
    )
    print(f"Continuing existing conversation session: {conversation_name}")

  # Step 2: Send query in the conversation
  query_input = discoveryengine.TextInput(input=query_text)

  summary_spec = discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
      include_citations=True
  )

  request = discoveryengine.ConverseConversationRequest(
      name=conversation_name,
      query=query_input,
      serving_config=serving_config,
      summary_spec=summary_spec,
  )

  response = client.converse_conversation(request=request)

  reply_text = ""
  if response.reply:
    if (
        hasattr(response.reply, "summary")
        and response.reply.summary
        and response.reply.summary.summary_text
    ):
      reply_text = response.reply.summary.summary_text
    elif hasattr(response.reply, "reply") and response.reply.reply:
      reply_text = response.reply.reply

  print(f"\nUser Query: {query_text}")
  print(f"AI Generated Reply: {reply_text}")

  # Step 3: Parse and display source citations and grounding results
  print("\nGrounding Citations & Sources:")
  for idx, search_result in enumerate(response.search_results, 1):
    doc = search_result.document
    print(f"  [{idx}] Document ID: {doc.id}")
    struct_data = doc.derived_struct_data or doc.struct_data
    if struct_data:
      title = struct_data.get("title", "No Title")
      link = struct_data.get("link", "No Link")
      print(f"      Title: {title}")
      print(f"      URI: {link}")

  return response


# [END genappbuilder_converse_conversation]
