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


def get_bearer_token() -> str:
    import google.auth
    from google.auth.transport.requests import Request

    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_req = Request()
    creds.refresh(auth_req)
    bearer_token = creds.token
    return bearer_token


# get bearer token
BEARER_TOKEN = get_bearer_token()


async def generate_content() -> str:
    """
    Connects to the Gemini API via WebSocket, sends a text prompt,
    and returns the aggregated text response.
    """
    # [START googlegenaisdk_live_websocket_textgen_with_audio]
    import base64
    import json

    from websockets.asyncio.client import connect
    from scipy.io import wavfile

    def read_wavefile(filepath: str) -> tuple[str, str]:
        # Read the .wav file using scipy.io.wavfile.read
        rate, data = wavfile.read(filepath)
        # Convert the NumPy array of audio samples back to raw bytes
        raw_audio_bytes = data.tobytes()
        # Encode the raw bytes to a base64 string.
        # The result needs to be decoded from bytes to a UTF-8 string
        base64_encoded_data = base64.b64encode(raw_audio_bytes).decode("ascii")
        mime_type = f"audio/pcm;rate={rate}"
        return base64_encoded_data, mime_type

    # Configuration Constants
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us-central1"
    GEMINI_MODEL_NAME = "gemini-2.0-flash-live-preview-04-09"
    # To generate a bearer token in CLI, use:
    #   $ gcloud auth application-default print-access-token
    # It's recommended to fetch this token dynamically rather than hardcoding.
    # BEARER_TOKEN = "ya29.a0AW4XtxhRb1s51TxLPnj..."

    # Websocket Configuration
    WEBSOCKET_HOST = "us-central1-aiplatform.googleapis.com"
    WEBSOCKET_SERVICE_URL = f"wss://{WEBSOCKET_HOST}/ws/google.cloud.aiplatform.v1.LlmBidiService/BidiGenerateContent"

    # Websocket Authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }

    # Model Configuration
    model_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{GEMINI_MODEL_NAME}"
    model_generation_config = {"response_modalities": ["TEXT"]}

    async with connect(WEBSOCKET_SERVICE_URL, additional_headers=headers) as websocket_session:
        # 1. Send setup configuration
        websocket_config = {
            "setup": {
                "model": model_path,
                "generation_config": model_generation_config,
            }
        }
        await websocket_session.send(json.dumps(websocket_config))

        # 2. Receive setup response
        raw_setup_response = await websocket_session.recv()
        setup_response = json.loads(
            raw_setup_response.decode("utf-8")
            if isinstance(raw_setup_response, bytes)
            else raw_setup_response
        )
        print(f"Setup Response: {setup_response}")
        # Example response: {'setupComplete': {}}
        if "setupComplete" not in setup_response:
            print(f"Setup failed: {setup_response}")
            return "Error: WebSocket setup failed."

        # 3. Send audio message
        encoded_audio_message, mime_type = read_wavefile(
            "hello_gemini_are_you_there.wav"
        )
        # Example audio message:  "Hello? Gemini are you there?"

        user_message = {
            "client_content": {
                "turns": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "inlineData": {
                                    "mimeType": mime_type,  # Example value: "audio/pcm;rate=24000"
                                    "data": encoded_audio_message,  # Example value: "AQD//wAAAAAAA....."
                                }
                            }
                        ],
                    }
                ],
                "turn_complete": True,
            }
        }
        await websocket_session.send(json.dumps(user_message))

        # 4. Receive model response
        aggregated_response_parts = []
        async for raw_response_chunk in websocket_session:
            response_chunk = json.loads(raw_response_chunk.decode("utf-8"))

            server_content = response_chunk.get("serverContent")
            if not server_content:
                # This might indicate an error or an unexpected message format
                print(f"Received non-serverContent message or empty content: {response_chunk}")
                break

            # Collect text responses
            model_turn = server_content.get("modelTurn")
            if model_turn and "parts" in model_turn and model_turn["parts"]:
                aggregated_response_parts.append(model_turn["parts"][0].get("text", ""))

            # End of response
            if server_content.get("turnComplete"):
                break

        final_response_text = "".join(aggregated_response_parts)
        print(f"Response: {final_response_text}")
        # Example response:
        #     Setup Response: {'setupComplete': {}}
        #     Response: Hey there. What's on your mind today?
    # [END googlegenaisdk_live_websocket_textgen_with_audio]
    return final_response_text


if __name__ == "__main__":
    asyncio.run(generate_content())
