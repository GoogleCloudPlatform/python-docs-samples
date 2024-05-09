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


def streaming_prediction(
    project_id: str,
    location: str,
) -> str:
    """Streaming Text Example with a Large Language Model."""
    # [START aiplatform_streaming_text]
    import vertexai
    from vertexai import language_models

    # TODO(developer): update project_id & location
    vertexai.init(project=project_id, location=location)

    text_generation_model = language_models.TextGenerationModel.from_pretrained(
        "text-bison"
    )
    parameters = {
        # Temperature controls the degree of randomness in token selection.
        "temperature": 0.2,
        # Token limit determines the maximum amount of text output.
        "max_output_tokens": 256,
        # Tokens are selected from most probable to least until the
        # sum of their probabilities equals the top_p value.
        "top_p": 0.8,
        # A top_k of 1 means the selected token is the most probable among
        # all tokens.
        "top_k": 40,
    }

    responses = text_generation_model.predict_streaming(
        prompt="Give me ten interview questions for the role of program manager.",
        **parameters,
    )

    results = []
    for response in responses:
        print(response)
        results.append(str(response))
    results = "\n".join(results)
    print(results)
    # [END aiplatform_streaming_text]
    return results


if __name__ == "__main__":
    streaming_prediction()
