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

"""Google Cloud Vertex AI sample for listing deployable models in
    Model Garden.
"""
import os
from typing import List


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_deployable_models() -> List[str]:
    # [START aiplatform_modelgarden_models_deployables_list]

    import vertexai
    from vertexai.preview import model_garden

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # List deployable models, optionally list Hugging Face models only or filter by model name.
    deployable_models = model_garden.list_deployable_models(list_hf_models=False, model_filter="gemma")
    print(deployable_models)
    # Example response:
    # ['google/gemma2@gemma-2-27b','google/gemma2@gemma-2-27b-it', ...]

    # [END aiplatform_modelgarden_models_deployables_list]

    return deployable_models


if __name__ == "__main__":
    list_deployable_models()
