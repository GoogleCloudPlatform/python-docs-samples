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


from vertexai.generative_models import GenerationResponse


def generate_text_with_grounding_web(project_id: str) -> GenerationResponse:
    # [START generativeaionvertexai_gemini_grounding_with_web]
    import vertexai

    from vertexai.generative_models import (
        GenerationConfig,
        GenerativeModel,
        Tool,
        grounding,
    )

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-001")

    # Use Google Search for grounding
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

    prompt = "When is the next total solar eclipse in US?"
    response = model.generate_content(
        prompt,
        tools=[tool],
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )

    print(response)

    # [END generativeaionvertexai_gemini_grounding_with_web]
    return response


def generate_text_with_grounding_vertex_ai_search(
    project_id: str, data_store_path: str
) -> GenerationResponse:
    # [START generativeaionvertexai_gemini_grounding_with_vais]
    import vertexai

    from vertexai.preview.generative_models import grounding
    from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # data_store_path = "projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{data_store_id}"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-001")

    tool = Tool.from_retrieval(
        grounding.Retrieval(grounding.VertexAISearch(datastore=data_store_path))
    )

    prompt = "How do I make an appointment to renew my driver's license?"
    response = model.generate_content(
        prompt,
        tools=[tool],
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )

    print(response)

    # [END generativeaionvertexai_gemini_grounding_with_vais]
    return response
