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
    # [START googlegenaisdk_live_with_txt]
    from google import genai
    from google.genai.types import (
        Content,
        LiveConnectConfig,
        HttpOptions,
        Modality,
        Part,
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1beta1"))
    model_id = "gemini-2.0-flash-live-preview-04-09"

    async with client.aio.live.connect(
        model=model_id,
        config=LiveConnectConfig(response_modalities=[Modality.TEXT]),
    ) as session:
        text_input = "Hello? Gemini, are you there?"
        print("> ", text_input, "\n")
        await session.send_client_content(
            turns=Content(role="user", parts=[Part(text=text_input)])
        )

        response = []

        async for message in session.receive():
            if message.text:
                response.append(message.text)

        print("".join(response))
    # Example output:
    # >  Hello? Gemini, are you there?
    # Yes, I'm here. What would you like to talk about?
    # [END googlegenaisdk_live_with_txt]
    return response


if __name__ == "__main__":
    asyncio.run(generate_content())
