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

# [START aiplatform_sdk_grounding]
from typing import Optional

import vertexai
from vertexai.language_models import (
    GroundingSource,
    TextGenerationModel,
    TextGenerationResponse,
)


def grounding(
    project_id: str,
    location: str,
    data_store_location: Optional[str],
    data_store_id: Optional[str],
) -> TextGenerationResponse:
    """Grounding example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")

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
    # [END aiplatform_sdk_grounding]

    return response


if __name__ == "__main__":
    grounding()
