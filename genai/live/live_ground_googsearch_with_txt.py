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


async def generate_content() -> list[str]:
    # [START googlegenaisdk_live_ground_googsearch_with_txt]
    from google import genai
    from google.genai.types import (
        AudioTranscriptionConfig,
        Content,
        GoogleSearch,
        LiveConnectConfig,
        Modality,
        Part,
        Tool,
    )

    client = genai.Client()
    model_id = "gemini-3.8-live"
    config = LiveConnectConfig(
        response_modalities=[Modality.AUDIO],
        output_audio_transcription=AudioTranscriptionConfig(),
        tools=[Tool(google_search=GoogleSearch())],
    )
    async with client.aio.live.connect(model=model_id, config=config) as session:
        text_input = "When did the last Brazil vs. Argentina soccer match happen?"
        print("> ", text_input, "\n")
        await session.send_client_content(
            turns=Content(role="user", parts=[Part(text=text_input)])
        )

        response = []

        async for chunk in session.receive():
            server_content = chunk.server_content
            if server_content and server_content.output_transcription:
                if server_content.output_transcription.text:
                    response.append(server_content.output_transcription.text)

    print("".join(response))
    # Example output:
    # > When did the last Brazil vs. Argentina soccer match happen?
    # The last Brazil vs. Argentina soccer match was on March 25, 2025, a 2026 World Cup qualifier, where Argentina defeated Brazil 4-1.
    # [END googlegenaisdk_live_ground_googsearch_with_txt]
    return True


if __name__ == "__main__":
    asyncio.run(generate_content())
