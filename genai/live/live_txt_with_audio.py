# Copyright 2024 Google LLC
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


# Test file: https://storage.googleapis.com/generativeai-downloads/data/16000.wav
# Install helpers for converting files: pip install librosa soundfile

import asyncio
import io
from pathlib import Path

import requests
from google import genai
from google.genai import types
import os
import soundfile as sf
import librosa


audio_url = "https://storage.googleapis.com/generativeai-downloads/data/16000.wav"

client = genai.Client()

# config = {"response_modalities": ["TEXT"]}
config = types.LiveConnectConfig(response_modalities=[types.Modality.TEXT])
# model = "gemini-live-2.5-flash-preview-native-audio"
model = "gemini-2.0-flash-live-preview-04-09"

# model = "gemini-live-2.5-flash"

# def generate_content() -> str:
#     from google import genai
#     # [START googlegenaisdk_thinking_textgen_with_txt]
#     # client = genai.Client(
#     #     vertexai=True, project='cloud-ai-devrel-softserve', location='us-central1'
#     # )
#     # response = client.models.generate_content(
#     #     model="gemini-2.5-pro",
#     #     contents="solve x^2 + 4x + 4 = 0",
#     # )
#
#     client = genai.Client(
#         vertexai=True,
#         project=os.environ["GOOGLE_CLOUD_PROJECT"],
#         location=os.environ["GOOGLE_CLOUD_LOCATION"],
#     )
#     # model = "gemini-live-2.5-flash"
#     model = "gemini-live-2.5-flash-preview-native-audio"
#     config = {"response_modalities": ["TEXT"]}
#     response = client.models.generate_content(
#         model=model,
#         contents="solve x^2 + 4x + 4 = 0",
#     )
#     print(response.text)
# generate_content()


async def main():
    # config = {"response_modalities": ["TEXT"]}

    # async with client.aio.live.connect(model=model, config=config) as session:
    async with client.aio.live.connect(model=model) as session:
        # TODO after the meeting add confing to the meeting
        try:
            # audio_url = "https://storage.googleapis.com/generativeai-downloads/data/16000.wav"
            # response = requests.get(audio_url)
            # response.raise_for_status()
            # buffer = io.BytesIO(response.content)
            # y, sr = librosa.load(buffer, sr=16000)
            # sf.write(buffer, y, sr, format="RAW", subtype="PCM_16")
            # buffer.seek(0)
            # audio_bytes = buffer.read()

            buffer = io.BytesIO()
            y, sr = librosa.load("hello_gemini_are_you_there.wav", sr=16000)
            sf.write(buffer, y, sr, format="RAW", subtype="PCM_16")
            buffer.seek(0)
            audio_bytes = buffer.read()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching audio from URL: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        # If you've pre-converted to sample.pcm using ffmpeg, use this instead:
        # audio_bytes = Path("sample.pcm").read_bytes()
        await session.send_realtime_input(
            audio=types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
        )

        async for response in session.receive():
            if response.text is not None:
                print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
