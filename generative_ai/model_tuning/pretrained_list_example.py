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

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_tuned_models() -> None:
    """List tuned models."""
    # [START generativeaionvertexai_sdk_list_tuned_models]
    import vertexai

    from vertexai.language_models import TextGenerationModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = TextGenerationModel.from_pretrained("text-bison@002")
    tuned_model_names = model.list_tuned_model_names()
    print(tuned_model_names)
    # Example response:
    # ['projects/1234567890/locations/us-central1/models/1234567889012345',
    # ...]

    # [END generativeaionvertexai_sdk_list_tuned_models]

    return tuned_model_names


if __name__ == "__main__":
    list_tuned_models()
