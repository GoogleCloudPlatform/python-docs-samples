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

# [START aiplatform_sdk_tuning]
from __future__ import annotations


def tuning(
    project_id: str,
) -> None:

    # [START generativeaionvertexai_tuning]
    import vertexai
    from vertexai.language_models import TextGenerationModel
    from google.auth import default

    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1", credentials=credentials)

    model = TextGenerationModel.from_pretrained("text-bison@002")

    tuning_job = model.tune_model(
        training_data="gs://cloud-samples-data/ai-platform/generative_ai/headline_classification.jsonl",
        tuning_job_location="europe-west4",
        tuned_model_location="us-central1",
    )

    print(tuning_job._status)
    # [END generativeaionvertexai_tuning]

    return model
