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


async def generate_content() -> None:
    # [START googlegenaisdk_live_audiogen_with_txt]
    import numpy as np
    import scipy.io.wavfile as wavfile
    from google import genai
    from google.genai.types import (Content, LiveConnectConfig, Modality, Part,
                                    PrebuiltVoiceConfig, SpeechConfig,
                                    VoiceConfig)

    client = genai.Client()
    model = "gemini-2.0-flash-live-preview-04-09"
    # For more Voice options, check https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash#live-api-native-audio
    voice_name = "Aoede"

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

        audio_data_chunks = []
        async for message in session.receive():
            if (
                message.server_content.model_turn
                and message.server_content.model_turn.parts
            ):
                for part in message.server_content.model_turn.parts:
                    if part.inline_data:
                        audio_data_chunks.append(
                            np.frombuffer(part.inline_data.data, dtype=np.int16)
                        )

        if audio_data_chunks:
            print("Received audio answer. Saving to local file...")
            full_audio_array = np.concatenate(audio_data_chunks)

            output_filename = "gemini_response.wav"
            sample_rate = 24000

            wavfile.write(output_filename, sample_rate, full_audio_array)
            print(f"Audio saved to {output_filename}")

    # Example output:
    # >  Hello? Gemini are you there?
    # Received audio answer. Saving to local file...
    # Audio saved to gemini_response.wav
    # [END googlegenaisdk_live_audiogen_with_txt]
    return True


if __name__ == "__main__":
    asyncio.run(generate_content())
