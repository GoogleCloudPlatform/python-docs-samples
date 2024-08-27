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
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_tuned_code_generation_models() -> None:
    """List tuned models."""
    # [START aiplatform_sdk_list_tuned_code_generation_models]

    import vertexai
    from vertexai.preview.language_models import CodeGenerationModel

    # TODO(developer): Update project_id
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = CodeGenerationModel.from_pretrained("code-bison@001")
    tuned_model_names = model.list_tuned_model_names()
    print(tuned_model_names)
    # [END aiplatform_sdk_list_tuned_code_generation_models]

    return tuned_model_names


if __name__ == "__main__":
    list_tuned_code_generation_models()
