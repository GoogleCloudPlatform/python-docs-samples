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

# [START aiplatform_sdk_tune_code_generation_model]
from __future__ import annotations


def tune_code_generation_model(
    project_id: str
) -> None:

    # [START generativeaionvertexai_tune_code_generation_model]
    from google.auth import default
    import vertexai
    from vertexai.language_models import CodeGenerationModel

    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1", credentials=credentials)

    model = CodeGenerationModel.from_pretrained("code-bison@002")

    tuning_job = model.tune_model(
        training_data="gs://cloud-samples-data/ai-platform/generative_ai/headline_classification.jsonl",
        tuning_job_location="europe-west4",
        tuned_model_location="us-central1",
    )

    print(tuning_job._status)
    # [END generativeaionvertexai_tune_code_generation_model]

    return model


# [END aiplatform_sdk_tune_code_generation_model]
