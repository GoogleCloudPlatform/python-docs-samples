#!/usr/bin/env python

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

"""Example A2A client for the Data Engineering Agent.

This script demonstrates how to interact with the Data Engineering Agent (DEA)
using the A2A Python SDK. It handles Agent Card resolution, multi-turn
conversations using conversation tokens persisted to a local file, and
automatic retries on deadline exceeded.

The script is compatible with DEA v0.3 protocol flavor.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import re
from typing import Any, Dict, List, Optional
import uuid

from a2a import client as a2a_client
from a2a import types as a2a_types
from a2a.client import service_parameters as a2a_service_params
from a2a.utils import constants as a2a_constants
from google.auth import default
from google.auth.transport import requests as auth_requests
from google.protobuf import json_format as pb_json_format
import httpx

import logging


# --- Constants ---

DEA_EXT_PREFIX = "https://geminidataanalytics.googleapis.com/a2a/extensions"
GCP_RESOURCE_EXT_URI = f"{DEA_EXT_PREFIX}/gcpresource/v1"
CONVERSATION_TOKEN_EXT_URI = f"{DEA_EXT_PREFIX}/conversationtoken/v1"
FINISH_REASON_EXT_URI = f"{DEA_EXT_PREFIX}/finishreason/v1"
INSTRUCTION_EXT_URI = f"{DEA_EXT_PREFIX}/instruction/v1"
MESSAGE_LEVEL_EXT_URI = f"{DEA_EXT_PREFIX}/messagelevel/v1"

AGENT_NAME = "dataengineeringagent"
AGENT_BASE_URL_TEMPLATE = (
    "https://geminidataanalytics.googleapis.com/v1/a2a/projects/"
    "{project_id}/locations/{location}/agents/{agent_name}"
)


# --- Helper Functions ---


async def force_alt_sse(request: httpx.Request) -> None:
  """HTTP request hook that dynamically forces GFE SSE transcoding for streams."""
  if request.url.path.endswith((":stream", ":subscribe")):
    request.url = request.url.copy_merge_params({"alt": "sse"})


def get_bearer_token() -> Optional[str]:
  """Fetches a Google Cloud bearer token using Application Default Credentials (ADC)."""
  try:
    credentials, _ = default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_request = auth_requests.Request()
    credentials.refresh(auth_request)
    return credentials.token
  except Exception as e:  # pylint: disable=broad-exception-caught
    logging.error("Error getting credentials: %s", e)
    logging.info(
        "Please ensure you have authenticated with 'gcloud auth"
        " application-default login'."
    )
    return None


def load_instructions(paths: List[str]) -> List[Dict[str, str]]:
  """Reads instructions from files or directories."""
  instructions = []
  for path_str in paths:
    path = pathlib.Path(path_str)
    if not path.exists():
      raise FileNotFoundError(f"Instruction path does not exist: {path_str}")
    if path.is_file():
      instructions.append(
          {"name": path.name, "definition": path.read_text(encoding="utf-8")}
      )
    elif path.is_dir():
      for file_path in path.iterdir():
        if file_path.is_file():
          instructions.append({
              "name": file_path.name,
              "definition": file_path.read_text(encoding="utf-8"),
          })
  return instructions


# --- Core Interaction Snippet ---


# [START geminidataanalytics_a2a_client]
async def interact_with_data_engineering_agent(
    auth_token: str,
    gcp_resource_id: str,
    message: str,
    conversation_token: Optional[str] = None,
    instructions: Optional[List[Dict[str, str]]] = None,
) -> str:
  """Sends a query to the Data Engineering Agent via the A2A protocol.

  This function implements the complete client communication lifecycle:
  1. Resolves the Agent Card to discover endpoint protocols.
  2. Establishes the A2A client session over HTTP/SSE.
  3. Attaches required metadata extensions (GCP Resource ID, Conversation Token,
     instructions).
  4. Invokes the agent and streams responses.
  5. Handles DEADLINE_EXCEEDED finish reason by auto-resuming the turn.

  Args:
      auth_token: A Google Cloud access token for authentication.
      gcp_resource_id: The target GCP resource ID, formatted as
        'projects/{project}/locations/{location}/...'
      message: The natural language query to send to the agent.
      conversation_token: Optional conversation token to resume an existing
        session.
      instructions: Optional custom agent instructions.

  Returns:
      The updated conversation token for subsequent turns.
  """
  # Extract project_id and location from gcp_resource_id
  match = re.search(r"projects/([^/]+)/locations/([^/]+)", gcp_resource_id)
  if not match:
    raise ValueError(
        f"Invalid gcp_resource_id format: {gcp_resource_id}. "
        "Expected 'projects/{project}/locations/{location}/...'"
    )
  project_id, location = match.groups()
  agent_base_url = AGENT_BASE_URL_TEMPLATE.format(
      project_id=project_id,
      location=location,
      agent_name=AGENT_NAME,
  )

  headers = {"Authorization": f"Bearer {auth_token}"}
  async with httpx.AsyncClient(
      headers=headers,
      timeout=600.0,
      event_hooks={"request": [force_alt_sse]},
  ) as httpx_client:

    # Resolve the Agent Card from the endpoint
    resolver = a2a_client.A2ACardResolver(
        httpx_client=httpx_client, base_url=agent_base_url
    )
    agent_card = await resolver.get_agent_card(relative_card_path="v1/card")

    # Create the A2A protocol client
    config = a2a_client.ClientConfig(
        supported_protocol_bindings=[a2a_constants.TransportProtocol.HTTP_JSON],
        streaming=True,
        httpx_client=httpx_client,
    )
    client = await a2a_client.create_client(
        agent=agent_card, client_config=config
    )

    try:
      # Helper to build request metadata
      def build_metadata(token_val: Optional[str]) -> Dict[str, Any]:
        meta = {GCP_RESOURCE_EXT_URI: {"gcpResourceId": gcp_resource_id}}
        if token_val:
          meta[CONVERSATION_TOKEN_EXT_URI] = token_val
        if instructions:
          meta[INSTRUCTION_EXT_URI] = {"agentInstructions": instructions}
        return meta

      context_id = str(uuid.uuid4())
      current_token = conversation_token
      query_to_send = message
      is_retry = False

      while True:
        if is_retry:
          logging.info("Resuming session due to deadline exceeded...")

        user_message = a2a_types.Message(
            message_id=str(uuid.uuid4()),
            role=a2a_types.Role.ROLE_USER,
            parts=[a2a_types.Part(text=query_to_send)],
            context_id=context_id,
        )

        request = a2a_types.SendMessageRequest(
            message=user_message,
            metadata=build_metadata(current_token),
        )

        extensions = [
            MESSAGE_LEVEL_EXT_URI,
            INSTRUCTION_EXT_URI,
            GCP_RESOURCE_EXT_URI,
            CONVERSATION_TOKEN_EXT_URI,
            FINISH_REASON_EXT_URI,
        ]

        service_params = a2a_service_params.ServiceParametersFactory.create(
            [a2a_service_params.with_a2a_extensions(extensions)]
        )
        context = a2a_client.ClientCallContext(
            service_parameters=service_params, timeout=600.0
        )

        finish_reason: Optional[str] = None
        responses = client.send_message(request, context=context)

        async for response_obj in responses:
          # Process and print outcomes to console
          # (teaches user how to handle output)
          print(response_obj)
          event = pb_json_format.MessageToDict(
              response_obj, preserving_proto_field_name=True
          )
          events = event if isinstance(event, list) else [event]
          for e in events:
            # Extract metadata from different possible A2A event layers
            meta = None
            if "task" in e:
              meta = e["task"].get("metadata", {})
            elif "status_update" in e:
              meta = e["status_update"].get("metadata", {})
            elif "message" in e:
              meta = e["message"].get("metadata", {})

            if meta:
              # Update conversation token
              token_val = meta.get(CONVERSATION_TOKEN_EXT_URI)
              if token_val:
                extracted_token = (
                    token_val.get("conversationToken")
                    if isinstance(token_val, dict)
                    else token_val
                )
                if extracted_token:
                  current_token = extracted_token
              # Extract finish reason
              reason_val = meta.get(FINISH_REASON_EXT_URI)
              if reason_val:
                finish_reason = (
                    reason_val.get("finishReason")
                    if isinstance(reason_val, dict)
                    else reason_val
                )

        # Handle deadline exceeded by repeating the turn
        if finish_reason == "DEADLINE_EXCEEDED":
          logging.warning("Agent execution hit deadline. Resuming...")
          query_to_send = "Please continue."
          is_retry = True
        else:
          break

      return current_token

    finally:
      await client.close()
# [END geminidataanalytics_a2a_client]


# --- Main CLI Entrypoint ---


async def main() -> None:
  parser = argparse.ArgumentParser(
      description="Data Engineering Agent A2A Client"
  )
  parser.add_argument(
      "--gcp_resource_id", required=True, help="Target GCP resource ID."
  )
  parser.add_argument("--message", required=True, help="The message to send.")
  parser.add_argument(
      "--conversation_token_path",
      help="Local file to persist conversation token.",
  )
  parser.add_argument(
      "--instruction_path",
      action="append",
      help="Path to instruction files/dirs.",
  )

  args = parser.parse_args()
  logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

  token = os.getenv("GOOGLE_ACCESS_TOKEN") or get_bearer_token()
  if not token:
    logging.error("Authentication failed. No Google access token found.")
    return

  conversation_token = None
  if args.conversation_token_path:
    token_file = pathlib.Path(args.conversation_token_path)
    if token_file.exists():
      conversation_token = token_file.read_text(encoding="utf-8").strip()

  try:
    instructions = load_instructions(args.instruction_path or [])
    new_token = await interact_with_data_engineering_agent(
        auth_token=token,
        gcp_resource_id=args.gcp_resource_id,
        message=args.message,
        conversation_token=conversation_token,
        instructions=instructions,
    )

    if args.conversation_token_path and new_token:
      pathlib.Path(args.conversation_token_path).write_text(
          new_token, encoding="utf-8"
      )

  except Exception as e:  # pylint: disable=broad-exception-caught
    logging.exception("Operation failed: %s", e)


if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    pass
