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


async def generate_content(memory_corpus: str) -> list[str]:
    # [START googlegenaisdk_live_ground_ragengine_with_txt]
    from google import genai
    from google.genai.types import (Content, LiveConnectConfig, Modality, Part,
                                    Retrieval, Tool, VertexRagStore,
                                    VertexRagStoreRagResource)

    client = genai.Client()
    model_id = "gemini-2.0-flash-live-preview-04-09"
    rag_store = VertexRagStore(
        rag_resources=[
            VertexRagStoreRagResource(
                rag_corpus=memory_corpus  # Use memory corpus if you want to store context.
            )
        ],
        # Set `store_context` to true to allow Live API sink context into your memory corpus.
        store_context=True,
    )
    config = LiveConnectConfig(
        response_modalities=[Modality.TEXT],
        tools=[Tool(retrieval=Retrieval(vertex_rag_store=rag_store))],
    )

    async with client.aio.live.connect(model=model_id, config=config) as session:
        text_input = "What are newest gemini models?"
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
    # >  What are newest gemini models?
    # In December 2023, Google launched Gemini, their "most capable and general model". It's multimodal, meaning it understands and combines different types of information like text, code, audio, images, and video.
    # [END googlegenaisdk_live_ground_ragengine_with_txt]
    return response


if __name__ == "__main__":
    asyncio.run(generate_content("test_memory_corpus"))
