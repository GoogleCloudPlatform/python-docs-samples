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
import os

import vertexai


async def generate_content() -> list[str]:
    # [START googlegenaisdk_live_ground_ragengine_with_txt]
    from google import genai
    from google.genai.types import (
        Content,
        LiveConnectConfig,
        HttpOptions,
        Modality,
        Part,
        Tool,
        Retrieval,
        VertexRagStore,
        VertexRagStoreRagResource,
    )

    # from vertexai import rag
    # vertexai.init(project=os.environ["GOOGLE_CLOUD_PROJECT"], location=os.environ["GOOGLE_CLOUD_LOCATION"])

    client = genai.Client()
    # model_id = "gemini-live-2.5-flash"
    model_id = "gemini-2.0-flash-live-preview-04-09"

    # rag_store = VertexRagStore(
    #    rag_resources=[
    #        VertexRagStoreRagResource(
    #            rag_corpus=  # Use memory corpus if you want to store context. #todo ask Sampath should I create it?
    #        )
    #    ],
    #    # Set `store_context` to true to allow Live API sink context into your memory corpus.
    #    store_context=True
    # )
    # config = LiveConnectConfig(response_modalities=[Modality.TEXT],
    #                             tools=[Tool(
    #                                 retrieval=Retrieval(
    #                                     vertex_rag_store=rag_store))])
    config = LiveConnectConfig(response_modalities=[Modality.TEXT])

    async with client.aio.live.connect(model=model_id, config=config) as session:
        text_input = "What year did Mariusz Pudzianowski win World's Strongest Man?"
        print("> ", text_input, "\n")

        await session.send_client_content(
            turns=Content(role="user", parts=[Part(text=text_input)])
        )

        response = []

        async for message in session.receive():
            if message.text:
                response.append(message.text)
                continue

    print("".join(response))
    # Example output:
    # >  What year did Mariusz Pudzianowski win World's Strongest Man?
    # Mariusz Pudzianowski won World's Strongest Man in 2002, 2003, 2005, 2007, and 2008.
    # [END googlegenaisdk_live_ground_ragengine_with_txt]
    return response


if __name__ == "__main__":
    asyncio.run(generate_content())
