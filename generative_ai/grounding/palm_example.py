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

from typing import Optional

from vertexai.language_models import TextGenerationResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def grounding(
    data_store_location: Optional[str] = None,
    data_store_id: Optional[str] = None,
) -> TextGenerationResponse:
    """Grounding example with a Large Language Model"""
    # [START generativeaionvertexai_grounding]
    import vertexai

    from vertexai.language_models import GroundingSource, TextGenerationModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": 0.1,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 20,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")

    # TODO(developer): Update and un-comment below lines
    # data_store_id = "datastore_123456789012345"
    # data_store_location = "global"
    if data_store_id and data_store_location:
        # Use Vertex AI Search data store
        grounding_source = GroundingSource.VertexAISearch(
            data_store_id=data_store_id, location=data_store_location
        )
    else:
        # Use Google Search for grounding (Private Preview)
        grounding_source = GroundingSource.WebSearch()

    response = model.predict(
        "What are the price, available colors, and storage size options of a Pixel Tablet?",
        grounding_source=grounding_source,
        **parameters,
    )
    print(f"Response from Model: {response.text}")
    print(f"Grounding Metadata: {response.grounding_metadata}")
    # [END generativeaionvertexai_grounding]

    return response


if __name__ == "__main__":
    grounding(data_store_id="data-store_1234567890123", data_store_location="global")
