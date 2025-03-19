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

"""Google Cloud Vertex AI sample for listing verified deploy
    options for models in Model Garden.
"""
import os
from typing import List

from google.cloud.aiplatform_v1beta1 import types


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_deploy_options(model : str) -> List[types.PublisherModel.CallToAction.Deploy]:
    # [START aiplatform_modelgarden_models_deployables_options_list]

    import vertexai
    from vertexai.preview import model_garden

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # model = "google/gemma3@gemma-3-1b-it"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # For Hugging Face modelsm the format is the Hugging Face model name, as in
    # "meta-llama/Llama-3.3-70B-Instruct".
    # Go to https://console.cloud.google.com/vertex-ai/model-garden to find all deployable
    # model names.

    model = model_garden.OpenModel(model)
    deploy_options = model.list_deploy_options()
    print(deploy_options)
    # Example response:
    # [
    #   dedicated_resources {
    #     machine_spec {
    #       machine_type: "g2-standard-12"
    #       accelerator_type: NVIDIA_L4
    #       accelerator_count: 1
    #     }
    #   }
    #   container_spec {
    #     ...
    #   }
    #   ...
    # ]

    # [END aiplatform_modelgarden_models_deployables_options_list]

    return deploy_options


if __name__ == "__main__":
    list_deploy_options("google/gemma3@gemma-3-1b-it")
