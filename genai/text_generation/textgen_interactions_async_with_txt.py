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


async def create_interaction() -> str:
    # [START googlegenaisdk_interactions_textgen_async_with_txt]
    from google import genai

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    interaction = await client.aio.interactions.create(
        model=model_id,
        input="Compose a song about the adventures of a time-traveling squirrel.",
        response_modalities=["TEXT"],
    )

    print(interaction.output_text)
    # Example response:
    # (Verse 1)
    # Sammy the squirrel, a furry little friend
    # Had a knack for adventure, beyond all comprehend

    # [END googlegenaisdk_interactions_textgen_async_with_txt]
    return interaction.output_text


if __name__ == "__main__":
    asyncio.run(create_interaction())
