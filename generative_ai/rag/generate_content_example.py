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

from vertexai.generative_models import GenerationResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_content_with_rag(
    corpus_name: str,
) -> GenerationResponse:
    # [START generativeaionvertexai_rag_generate_content]

    from vertexai import rag
    from vertexai.generative_models import GenerativeModel, Tool
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[
                    rag.RagResource(
                        rag_corpus=corpus_name,
                        # Optional: supply IDs from `rag.list_files()`.
                        # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                    )
                ],
                rag_retrieval_config=rag.RagRetrievalConfig(
                    top_k=10,
                    filter=rag.utils.resources.Filter(vector_distance_threshold=0.5),
                ),
            ),
        )
    )

    rag_model = GenerativeModel(
        model_name="gemini-2.0-flash-001", tools=[rag_retrieval_tool]
    )
    response = rag_model.generate_content("Why is the sky blue?")
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
