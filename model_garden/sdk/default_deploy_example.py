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

"""Google Cloud Vertex AI sample for deploying a model in Model Garden
    using the default configurations.
"""
import os

from google.cloud import aiplatform


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def default_deploy(model : str) -> aiplatform.Endpoint:
    # [START generativeaionvertexai_modelgardensdk_default_deploy]

    import vertexai
    from vertexai.preview import model_garden

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # model= "google/gemma3@gemma-3-1b-it"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    open_model = model_garden.OpenModel(model)
    endpoint = open_model.deploy()

    # Optional. Run predictions on the deployed endoint.
    # endpoint.predict(instances=[{"prompt": "What is Generative AI?"}])

    # [END generativeaionvertexai_modelgardensdk_default_deploy]

    return endpoint


if __name__ == "__main__":
    default_deploy("google/gemma3@gemma-3-1b-it")
