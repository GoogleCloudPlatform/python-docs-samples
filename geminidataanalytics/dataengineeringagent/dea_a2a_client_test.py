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

"""Unit tests for the Data Engineering Agent A2A client."""

import unittest
from unittest import mock

import dea_a2a_client


class DeaA2AClientTest(unittest.IsolatedAsyncioTestCase):

  @mock.patch("dea_a2a_client.default")
  @mock.patch("dea_a2a_client.auth_requests.Request")
  def test_get_bearer_token_success(self, unused_auth_request, mock_default):
    mock_creds = mock.MagicMock()
    mock_creds.token = "test-token"
    mock_default.return_value = (mock_creds, "test-project")
    token = dea_a2a_client.get_bearer_token()
    self.assertEqual(token, "test-token")
    mock_creds.refresh.assert_called_once()

  @mock.patch("dea_a2a_client.default")
  def test_get_bearer_token_failure(self, mock_default):
    mock_default.side_effect = Exception("Auth failed")
    token = dea_a2a_client.get_bearer_token()
    self.assertIsNone(token)

  @mock.patch("dea_a2a_client.a2a_client.A2ACardResolver")
  @mock.patch("dea_a2a_client.a2a_client.create_client")
  @mock.patch("httpx.AsyncClient")
  @mock.patch("dea_a2a_client.pb_json_format.MessageToDict")
  async def test_multi_turn_and_retry(
      self,
      mock_message_to_dict,
      mock_httpx_cls,
      mock_create_client,
      mock_resolver_cls,
  ):
    mock_message_to_dict.side_effect = lambda x, **kwargs: x

    mock_card = mock.MagicMock()
    mock_card.name = "DEA"
    mock_interface = mock.MagicMock()
    mock_card.supported_interfaces = [mock_interface]

    mock_resolver = mock_resolver_cls.return_value
    mock_resolver.get_agent_card = mock.AsyncMock(return_value=mock_card)

    mock_client = mock.MagicMock()
    mock_client.close = mock.AsyncMock()
    mock_create_client.return_value = mock_client

    # 3. Define Response Behavior
    # Turn 1: Returns DEADLINE_EXCEEDED and a token
    token_v1 = "token-v1"
    response1 = {
        "task": {
            "id": "t1",
            "metadata": {
                dea_a2a_client.CONVERSATION_TOKEN_EXT_URI: {
                    "conversationToken": token_v1
                },
                dea_a2a_client.FINISH_REASON_EXT_URI: {
                    "finishReason": "DEADLINE_EXCEEDED"
                },
            },
            "history": [
                {"role": "agent", "content": {"text": "Part 1 of response"}}
            ],
        }
    }

    # Turn 2 (Retry of Turn 1): Returns FINISHED
    response2 = {
        "task": {
            "id": "t2",
            "metadata": {
                dea_a2a_client.CONVERSATION_TOKEN_EXT_URI: {
                    "conversationToken": "token-v2"
                },
                dea_a2a_client.FINISH_REASON_EXT_URI: {
                    "finishReason": "FINISHED"
                },
            },
            "history": [
                {"role": "agent", "content": {"text": "Part 2 of response"}}
            ],
        }
    }

    class AsyncIter:

      def __init__(self, items):
        self.items = items

      def __aiter__(self):
        return self

      async def __anext__(self):
        if not self.items:
          raise StopAsyncIteration
        return self.items.pop(0)

    mock_client.send_message.side_effect = [
        AsyncIter([response1]),
        AsyncIter([response2]),
    ]

    token = "fake-token"
    gcp_res_id = "projects/tp/locations/tl/repositories/tr/workspaces/default"
    result_token = await dea_a2a_client.interact_with_data_engineering_agent(
        auth_token=token,
        gcp_resource_id=gcp_res_id,
        message="Initial Query",
    )

    self.assertEqual(result_token, "token-v2")

    # Verify Authorization header was passed in httpx client initialization
    mock_httpx_cls.assert_called_once()
    called_headers = mock_httpx_cls.call_args[1].get("headers")
    self.assertEqual(called_headers, {"Authorization": f"Bearer {token}"})

  @mock.patch("dea_a2a_client.a2a_client.A2ACardResolver")
  @mock.patch("dea_a2a_client.a2a_client.create_client")
  @mock.patch("httpx.AsyncClient")
  @mock.patch("dea_a2a_client.pb_json_format.MessageToDict")
  async def test_session_persistence(
      self,
      mock_message_to_dict,
      unused_httpx,
      mock_create_client,
      mock_resolver_cls,
  ):
    mock_message_to_dict.side_effect = lambda x, **kwargs: x

    mock_client = mock.MagicMock()
    mock_client.close = mock.AsyncMock()
    mock_create_client.return_value = mock_client

    mock_card = mock.MagicMock()
    mock_card.supported_interfaces = [mock.MagicMock()]
    mock_resolver_cls.return_value.get_agent_card = mock.AsyncMock(
        return_value=mock_card
    )

    response = {"message": {"role": "agent", "content": {"text": "response"}}}

    class AsyncIter:

      def __init__(self, item):
        self.item = item
        self.used = False

      def __aiter__(self):
        return self

      async def __anext__(self):
        if self.used:
          raise StopAsyncIteration
        self.used = True
        return self.item

    mock_client.send_message.return_value = AsyncIter(response)

    token = "fake-token"
    gcp_resource_id = "projects/p/locations/l/repositories/r/workspaces/w"
    existing_token = "old-token"
    await dea_a2a_client.interact_with_data_engineering_agent(
        auth_token=token,
        gcp_resource_id=gcp_resource_id,
        message="query",
        conversation_token=existing_token,
    )
    call_request = mock_client.send_message.call_args[0][0]
    self.assertEqual(
        call_request.metadata[dea_a2a_client.CONVERSATION_TOKEN_EXT_URI],
        existing_token,
    )

  @mock.patch("dea_a2a_client.a2a_client.A2ACardResolver")
  @mock.patch("dea_a2a_client.a2a_client.create_client")
  @mock.patch("httpx.AsyncClient")
  @mock.patch("dea_a2a_client.pb_json_format.MessageToDict")
  async def test_retry_limit_exceeded(
      self,
      mock_message_to_dict,
      unused_httpx,
      mock_create_client,
      mock_resolver_cls,
  ):
    mock_message_to_dict.side_effect = lambda x, **kwargs: x

    mock_card = mock.MagicMock()
    mock_card.supported_interfaces = [mock.MagicMock()]
    mock_resolver_cls.return_value.get_agent_card = mock.AsyncMock(
        return_value=mock_card
    )

    mock_client = mock.MagicMock()
    mock_client.close = mock.AsyncMock()
    mock_create_client.return_value = mock_client
    response = {
        "task": {
            "id": "t1",
            "metadata": {
                dea_a2a_client.FINISH_REASON_EXT_URI: {
                    "finishReason": "DEADLINE_EXCEEDED"
                },
            },
            "history": [{"role": "agent", "content": {"text": "Waiting..."}}],
        }
    }

    class AsyncIter:

      def __init__(self, item):
        self.item = item
        self.used = False

      def __aiter__(self):
        return self

      async def __anext__(self):
        if self.used:
          raise StopAsyncIteration
        self.used = True
        return self.item

    mock_client.send_message.side_effect = lambda *args, **kwargs: AsyncIter(response)

    token = "fake-token"
    gcp_res_id = "projects/tp/locations/tl/repositories/tr/workspaces/default"
    result_token = await dea_a2a_client.interact_with_data_engineering_agent(
        auth_token=token,
        gcp_resource_id=gcp_res_id,
        message="Initial Query",
        max_retries=2,
    )

    self.assertIsNone(result_token)
    self.assertEqual(mock_client.send_message.call_count, 3)


if __name__ == "__main__":
  unittest.main()
