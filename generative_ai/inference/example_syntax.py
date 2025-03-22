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

import vertexai

from vertexai.language_models import TextEmbedding

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

vertexai.init(project=PROJECT_ID, location="us-central1")


def generate_response() -> TextEmbedding:
    # [START generativeaionvertexai_example_syntax]
    from vertexai.generative_models import GenerationConfig, GenerativeModel

    gemini_model = GenerativeModel("gemini-1.5-flash-002")
    generation_config = GenerationConfig(
        # See https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/content-generation-parameters
    )
    safety_settings = {
        # See https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters
    }
    model_response = gemini_model.generate_content(
        "...prompt content...",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    # [END generativeaionvertexai_example_syntax]
    # [START generativeaionvertexai_example_syntax_streaming]
    model_response = gemini_model.generate_content(
        "...prompt content...",
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    # [END generativeaionvertexai_example_syntax_streaming]

    return model_response


if __name__ == "__main__":
    generate_response()
