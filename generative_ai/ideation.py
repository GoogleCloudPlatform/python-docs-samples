# Copyright 2023 Google LLC
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


def interview(
    temperature: float,
    project_id: str,
    location: str,
) -> str:
    """Ideation example with a Large Language Model"""
    # [START aiplatform_sdk_ideation]
    import vertexai

    from vertexai.language_models import TextGenerationModel

    # TODO(developer): Update values for project_id, location & temperature
    vertexai.init(project=project_id, location=location)
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        "Give me ten interview questions for the role of program manager.",
        **parameters,
    )
    print(f"Response from Model: {response.text}")

    return response.text


# [END aiplatform_sdk_ideation]
