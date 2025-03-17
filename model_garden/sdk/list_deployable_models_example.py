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

from typing import List


def list_deployable_models(list_hugging_face_models : bool = False, model_filter : str = "") -> List[str]:
    # [START generativeaionvertexai_modelgardensdk_list_deployable_models]

    from vertexai.preview import model_garden

    # TODO(developer): Update and un-comment below lines
    # list_hugging_face_model_only = False
    # model_filter = "gemma"

    # List deployable models, optionally list Hugging Face models only or filter by model name.
    deployable_models = model_garden.list_deployable_models(list_hf_models=list_hugging_face_models, model_filter=model_filter)
    print(deployable_models)
    # Example response:
    # ['google/gemma2@gemma-2-27b','google/gemma2@gemma-2-27b-it', ...]

    # [END generativeaionvertexai_modelgardensdk_list_deployable_models]

    return deployable_models


if __name__ == "__main__":
    list_deployable_models()
    list_deployable_models(True, model_filter="gemma")
