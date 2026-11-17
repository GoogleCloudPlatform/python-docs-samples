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
    # [START googlegenaisdk_live_txt_with_audio]
    import io

    import librosa
    import requests
    import soundfile as sf
    from google import genai
    from google.genai.types import (
        ActivityEnd,
        ActivityStart,
        AudioTranscriptionConfig,
        AutomaticActivityDetection,
        Blob,
        LiveConnectConfig,
        Modality,
        RealtimeInputConfig,
    )

    client = genai.Client()
    model = "gemini-3.8-live"
    config = LiveConnectConfig(
        response_modalities=[Modality.AUDIO],
        output_audio_transcription=AudioTranscriptionConfig(),
        # Mark the start and end of the audio yourself, because the audio file
        # doesn't end with the silence that automatic activity detection needs.
        realtime_input_config=RealtimeInputConfig(
            automatic_activity_detection=AutomaticActivityDetection(disabled=True)
        ),
    )

    async with client.aio.live.connect(model=model, config=config) as session:
        audio_url = (
            "https://storage.googleapis.com/generativeai-downloads/data/16000.wav"
        )
        response = requests.get(audio_url)
        response.raise_for_status()
        buffer = io.BytesIO(response.content)
        y, sr = librosa.load(buffer, sr=16000)
        sf.write(buffer, y, sr, format="RAW", subtype="PCM_16")
        buffer.seek(0)
        audio_bytes = buffer.read()

        # If you've pre-converted to sample.pcm using ffmpeg, use this instead:
        # audio_bytes = Path("sample.pcm").read_bytes()

        print("> Answer to this audio url", audio_url, "\n")

        await session.send_realtime_input(activity_start=ActivityStart())
        await session.send_realtime_input(
            audio=Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
        )
        await session.send_realtime_input(activity_end=ActivityEnd())

        response = []

        async for message in session.receive():
            server_content = message.server_content
            if server_content and server_content.output_transcription:
                if server_content.output_transcription.text:
                    response.append(server_content.output_transcription.text)

        print("".join(response))
    # Example output:
    # > Answer to this audio url https://storage.googleapis.com/generativeai-downloads/data/16000.wav
    # Yes, I can hear you. How can I help you today?
    # [END googlegenaisdk_live_txt_with_audio]
    return response


if __name__ == "__main__":
    asyncio.run(generate_content())
