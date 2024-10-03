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


def generate_text_with_grounding_vertex_ai_search(
    data_store_id: str,
) -> GenerationResponse:
    # [START generativeaionvertexai_gemini_grounding_with_vais]
    import vertexai

    from vertexai.preview.generative_models import (
        GenerationConfig,
        GenerativeModel,
        Tool,
        grounding,
    )

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # data_store_id = "your-data-store-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-001")

    tool = Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=data_store_id,
                project=PROJECT_ID,
                location="global",
            )
        )
    )

    prompt = "How do I make an appointment to renew my driver's license?"
    response = model.generate_content(
        prompt,
        tools=[tool],
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )

    print(response.text)

    # [END generativeaionvertexai_gemini_grounding_with_vais]
    return response


if __name__ == "__main__":
    generate_text_with_grounding_vertex_ai_search("data-store_1234567890123")
