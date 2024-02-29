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

# [START aiplatform_sdk_distillation]
from __future__ import annotations


from typing import Optional


from google.auth import default
import vertexai
from vertexai.preview.language_models import TextGenerationModel, TuningEvaluationSpec


credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])


def distill_model(
    project_id: str,
    location: str,
    dataset: str,
    teacher_model: str,
    train_steps: int = 300,
    evaluation_dataset: Optional[str] = None,
) -> None:
    """Distill a new model.

    Args:
      project_id: GCP Project ID, used to initialize vertexai
      location: GCP Region, used to initialize vertexai
      dataset: GCS URI of jsonl file.
      teacher_model: Name of the teacher model.
      train_steps: Number of training steps to use when tuning the model.
      evaluation_dataset: GCS URI of jsonl file of evaluation data.
    """
    vertexai.init(project=project_id, location=location, credentials=credentials)

    eval_spec = TuningEvaluationSpec(evaluation_data=evaluation_dataset)

    student_model = TextGenerationModel.from_pretrained("text-bison@002")
    distillation_job = student_model.distill_from(
        teacher_model=teacher_model,
        dataset=dataset,
        # Optional:
        train_steps=train_steps,
        evaluation_spec=eval_spec,
    )

    return distillation_job


# [END aiplatform_sdk_distillation]
if __name__ == "__main__":
    distill_model()
