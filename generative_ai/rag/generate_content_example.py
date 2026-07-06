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

import os

from genai import types as genai_types

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_content_with_rag(
    corpus_name: str,
) -> genai_types.GenerateContentResponse:
    # [START generativeaionvertexai_rag_generate_content]

    import agentplatform

    from agentplatform import types
    from google import genai
    from google.genai import types as genai_types

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Initialize Agent Platform client once per session
    client = agentplatform.Client(project=PROJECT_ID, location="us-central1")

    rag_retrieval_tool = genai_types.Tool(
        retrieval=genai_types.Retrieval(
            vertex_rag_store=genai_types.VertexRagStore(
                rag_resources=[
                    genai_types.VertexRagStoreRagResource
                ],
                rag_retrieval_config=genai_types.RagRetrievalConfig(
                    top_k=10,
                    filter=genai_types.RagRetrievalConfigFilter(
                        vector_distance_threshold=0.5
                    ),
                ),
            ),
        )
    )

    # Create a GenAI SDK client to make a generate_content request
    genai_client = genai.Client(enterprise=True, project=PROJECT_ID, location="us-central1")

    response = genai_client.models.generate_content(
        model="gemini-2.5-pro",
        contents="Why is the sky blue?",
        config=genai_types.GenerateContentConfig(
            tools=[rag_retrieval_tool]
        )
    )
    print(response.text)
    # Example response:
    #   The sky appears blue due to a phenomenon called Rayleigh scattering.
    #   Sunlight, which contains all colors of the rainbow, is scattered
    #   by the tiny particles in the Earth's atmosphere....
    #   ...

    # [END generativeaionvertexai_rag_generate_content]

    return response


if __name__ == "__main__":
    generate_content_with_rag(
        "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"
    )
