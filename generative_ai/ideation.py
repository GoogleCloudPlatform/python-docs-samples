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

# [START generativeai_sdk_ideation]
from vertexai.preview.language_models import TextGenerationModel


def interview(temperature=.2):
    """Ideation example with a Large Language Model"""
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        'Give me ten interview questions for the role of program manager.',
        temperature=temperature,
        max_output_tokens=256,
        top_k=40,
        top_p=.8,
    )
    print(f"Response from Model: {response.text}")
# [END generativeai_sdk_ideation]

    return response


if __name__ == "__main__":
    interview()
