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


async def generate_content() -> str:
    # [START googlegenaisdk_textgen_async_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    model_id = "gemini-2.5-flash-preview-05-20"

    response = await client.aio.models.generate_content(
        model=model_id,
        contents="Compose a song about the adventures of a time-traveling squirrel.",
        config=GenerateContentConfig(
            response_modalities=["TEXT"],
        ),
    )

    print(response.text)
    # Example response:
    # (Verse 1)
    # Sammy the squirrel, a furry little friend
    # Had a knack for adventure, beyond all comprehend

    # [END googlegenaisdk_textgen_async_with_txt]
    return response.text


if __name__ == "__main__":
    asyncio.run(generate_content())
