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

# [START generativeaionvertexai_sdk_tune_code_generation_model]
from __future__ import annotations

import os

import vertexai
from vertexai.language_models import CodeGenerationModel

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def tune_code_generation_model() -> CodeGenerationModel:
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = CodeGenerationModel.from_pretrained("code-bison@002")

    # TODO(developer): Update the training data path
    tuning_job = model.tune_model(
        training_data="gs://cloud-samples-data/ai-platform/generative_ai/headline_classification.jsonl",
        tuning_job_location="europe-west4",
        tuned_model_location="us-central1",
    )

    print(tuning_job._status)
    # Example response:
    # ...
    # pipeline_job = aiplatform.PipelineJob.get('projects/1234567890/locations/europe-west4/pipelineJobs/tune...
    # PipelineState.PIPELINE_STATE_PENDING
    return model


# [END generativeaionvertexai_sdk_tune_code_generation_model]

if __name__ == "__main__":
    tune_code_generation_model()
