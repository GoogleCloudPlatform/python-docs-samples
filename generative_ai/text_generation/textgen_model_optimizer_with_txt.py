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
import os

# Replace 'your-project-id' with a default value if needed
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")


def generate_from_text_input() -> str:
    # [START generativeaionvertexai_textgen_model_optimizer_with_txt]
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("model-optimizer-exp-04-09", generation_config=GenerationConfig(
        model_config=GenerationConfig.ModelConfig(
            # valid options are: PRIORITIZE_QUALITY, BALANCED, PRIORITIZE_COST
            feature_selection_preference=GenerationConfig.ModelConfig.FeatureSelectionPreference.PRIORITIZE_COST
        )
    ))

    response = model.generate_content(
        "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
    )

    print(response.text)
    # Example response:
    # **Emphasizing the Dried Aspect:**
    # * Everlasting Blooms
    # * Dried & Delightful
    # * The Petal Preserve
    # ...

    # [END generativeaionvertexai_textgen_model_optimizer_with_txt]
    return response.text


if __name__ == "__main__":
    generate_from_text_input()
