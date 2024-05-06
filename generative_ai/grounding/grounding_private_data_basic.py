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


def generate_content(
    PROJECT_ID: str, REGION: str, MODEL_ID: str, DATASTORE: str
) -> object:
    # [START generativeaionvertexai_grounding_private_data_basic]
    import vertexai
    from vertexai.generative_models import GenerativeModel, Tool
    from vertexai.preview import generative_models as preview_generative_models

    vertexai.init(project=PROJECT_ID, location=REGION)

    gemini_model = GenerativeModel(MODEL_ID)
    vertex_search_tool = Tool.from_retrieval(
        retrieval=preview_generative_models.grounding.Retrieval(
            source=preview_generative_models.grounding.VertexAISearch(
                datastore=DATASTORE
            ),
        )
    )

    model_response = gemini_model.generate_content(
        "How to make appointment to renew driving license?", tools=[vertex_search_tool]
    )
    # [END generativeaionvertexai_grounding_private_data_basic]
    print(model_response)
