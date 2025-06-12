# Copyright 2025 Google LLC
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


# TODO: Migrate model_optimizer samples to /model_optimizer
#       and deprecate following sample
def generate_content() -> str:
    # [START googlegenaisdk_model_optimizer_textgen_with_txt]
    from google import genai
    from google.genai.types import (
        FeatureSelectionPreference,
        GenerateContentConfig,
        HttpOptions,
        ModelSelectionConfig
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1beta1"))
    response = client.models.generate_content(
        model="model-optimizer-exp-04-09",
        contents="How does AI work?",
        config=GenerateContentConfig(
            model_selection_config=ModelSelectionConfig(
                feature_selection_preference=FeatureSelectionPreference.BALANCED  # Options: PRIORITIZE_QUALITY, BALANCED, PRIORITIZE_COST
            ),
        ),
    )
    print(response.text)
    # Example response:
    # Okay, let's break down how AI works. It's a broad field, so I'll focus on the ...
    #
    # Here's a simplified overview:
    # ...
    # [END googlegenaisdk_model_optimizer_textgen_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
