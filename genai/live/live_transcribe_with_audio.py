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


# Test file: https://storage.googleapis.com/generativeai-downloads/data/16000.wav
# Install helpers for converting files: pip install librosa soundfile

import asyncio


async def generate_content() -> list[str]:
    # [START googlegenaisdk_live_transcribe_with_audio]
    from google import genai
    from google.genai.types import (
        LiveConnectConfig,
        Modality,
        AudioTranscriptionConfig,
        Part,
        Content,
    )

    client = genai.Client()
    model = "gemini-2.0-flash-live-preview-04-09"
    config = LiveConnectConfig(
        response_modalities=[Modality.AUDIO],
        input_audio_transcription=AudioTranscriptionConfig(),
        output_audio_transcription=AudioTranscriptionConfig(),
    )

    async with client.aio.live.connect(model=model, config=config) as session:
        input_txt = "Hello? Gemini are you there?"
        print(f"> {input_txt}")

        await session.send_client_content(
            turns=Content(role="user", parts=[Part(text=input_txt)])
        )

        response = []

        async for message in session.receive():
            if message.server_content.model_turn:
                print("Model turn:", message.server_content.model_turn)
            if message.server_content.input_transcription:
                print(
                    "Input transcript:", message.server_content.input_transcription.text
                )
            if message.server_content.output_transcription:
                response.append(message.server_content.output_transcription.text)

        print("".join(response))

    # Example output:
    # >  Hello? Gemini are you there?
    # Yes, I'm here. What would you like to talk about?
    # [END googlegenaisdk_live_transcribe_with_audio]
    return response


if __name__ == "__main__":
    asyncio.run(generate_content())
