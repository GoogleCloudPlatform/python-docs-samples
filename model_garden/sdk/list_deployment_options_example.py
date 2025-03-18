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

from typing import List

from google.cloud.aiplatform_v1beta1 import types


def list_deploy_options(model : str) -> List[types.PublisherModel.CallToAction.Deploy]:
    # [START generativeaionvertexai_modelgardensdk_list_deploy_options]
    from vertexai.preview import model_garden

    # TODO(developer): Update and un-comment below lines
    # model = "google/gemma3@gemma-3-1b-it"
    # hf_model = "meta-llama/Llama-3.3-70B-Instruct"

    # List the deployment options for a Model Garden model.
    model = model_garden.OpenModel(model)
    deploy_options = model.list_deploy_options()
    print(deploy_options)

    # List the deployment options for a Hugging Face model.
    # hf_model = model_garden.OpenModel(hf_model)
    # hf_deploy_options = hf_model.list_deploy_options()
    # print(hf_deploy_options)

    # [END generativeaionvertexai_modelgardensdk_list_deploy_options]

    return deploy_options


if __name__ == "__main__":
    list_deploy_options("google/gemma3@gemma-3-1b-it")
    list_deploy_options("meta-llama/Llama-3.3-70B-Instruct")
