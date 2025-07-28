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


async def generate_content() -> list[str]:
    # [START googlegenaisdk_live_audio_with_txt]
    import numpy as np
    from IPython.display import Audio, display
    from google import genai
    from google.genai.types import (
        Content,
        LiveConnectConfig,
        Modality,
        Part,
        SpeechConfig,
        VoiceConfig,
        PrebuiltVoiceConfig,
    )

    client = genai.Client()
    voice_name = "Aoede"
    model = "gemini-2.0-flash-live-preview-04-09"

    config = LiveConnectConfig(
        response_modalities=[Modality.AUDIO],
        speech_config=SpeechConfig(
            voice_config=VoiceConfig(
                prebuilt_voice_config=PrebuiltVoiceConfig(
                    voice_name=voice_name,
                )
            ),
        ),
    )

    async with client.aio.live.connect(
        model=model,
        config=config,
    ) as session:
        text_input = "Hello? Gemini are you there?"
        print("> ", text_input, "\n")

        await session.send_client_content(
            turns=Content(role="user", parts=[Part(text=text_input)])
        )

        audio_data = []
        async for message in session.receive():
            if (
                message.server_content.model_turn
                and message.server_content.model_turn.parts
            ):
                for part in message.server_content.model_turn.parts:
                    if part.inline_data:
                        audio_data.append(
                            np.frombuffer(part.inline_data.data, dtype=np.int16)
                        )

        if audio_data:
            print("Received audio answer: ")
            display(Audio(np.concatenate(audio_data), rate=24000, autoplay=True))

    # Example output:
    # >  Hello? Gemini are you there?
    # Received audio answer:
    # <IPython.lib.display.Audio object>
    # [STOP googlegenaisdk_live_audio_with_txt]
    return []


if __name__ == "__main__":
    asyncio.run(generate_content())
