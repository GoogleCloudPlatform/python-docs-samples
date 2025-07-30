# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os

import base64
import json
import numpy as np

from websockets.asyncio.client import connect
from scipy.io import wavfile


def get_bearer_token() -> str:
    import google.auth
    from google.auth.transport.requests import Request

    creds, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_req = Request()
    creds.refresh(auth_req)
    bearer_token = creds.token
    return bearer_token


# get bearer token
bearer_token = get_bearer_token()






# Set model generation_config
CONFIG = {"response_modalities": ["AUDIO"]}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {bearer_token[0]}",
}


async def main() -> None:
    # Connect to the server
    async with connect(SERVICE_URL, additional_headers=headers) as ws:

        # Setup the session
        async def setup() -> None:
            await ws.send(
                json.dumps(
                    {
                        "setup": {
                            "model": "gemini-live-2.5-flash",
                            "generation_config": CONFIG,
                        }
                    }
                )
            )

            # Receive setup response
            raw_response = await ws.recv(decode=False)
            setup_response = json.loads(raw_response.decode("ascii"))
            print(f"Connected: {setup_response}")
            return

        # Send text message
        async def send() -> bool:
            text_input = input("Input > ")
            if text_input.lower() in ("q", "quit", "exit"):
                return False

            msg = {
                "client_content": {
                    "turns": [{"role": "user", "parts": [{"text": text_input}]}],
                    "turn_complete": True,
                }
            }

            await ws.send(json.dumps(msg))
            return True

        # Receive server response
        async def receive() -> None:
            responses = []

            # Receive chucks of server response
            async for raw_response in ws:
                response = json.loads(raw_response.decode())
                server_content = response.pop("serverContent", None)
                if server_content is None:
                    break

                model_turn = server_content.pop("modelTurn", None)
                if model_turn is not None:
                    parts = model_turn.pop("parts", None)
                    if parts is not None:
                        for part in parts:
                            pcm_data = base64.b64decode(part["inlineData"]["data"])
                            responses.append(np.frombuffer(pcm_data, dtype=np.int16))

                # End of turn
                turn_complete = server_content.pop("turnComplete", None)
                if turn_complete:
                    break

            # Play the returned audio message
            display(Markdown("**Response >**"))
            display(Audio(np.concatenate(responses), rate=24000, autoplay=True))
            return

        await setup()

        while True:
            if not await send():
                break
            await receive()
