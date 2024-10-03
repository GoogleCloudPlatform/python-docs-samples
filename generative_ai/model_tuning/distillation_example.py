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

# [START generativeaionvertexai_sdk_distillation]
from __future__ import annotations

import os

from typing import Optional

import vertexai
from vertexai.preview.language_models import TextGenerationModel, TuningEvaluationSpec


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def distill_model(
    dataset: str,
    source_model: str,
    evaluation_dataset: Optional[str] = None,
) -> None:
    """Distill a new model using a teacher model and a dataset.
    Args:
        dataset (str): GCS URI of the JSONL file containing the training data.
            E.g., "gs://[BUCKET]/[FILENAME].jsonl".
        source_model (str): Name of the teacher model to distill from.
            E.g., "text-unicorn@001".
        evaluation_dataset (Optional[str]): GCS URI of the JSONL file containing the evaluation data.
    """
    # TODO developer - override these parameters as needed:
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Create a tuning evaluation specification with the evaluation dataset
    eval_spec = TuningEvaluationSpec(evaluation_data=evaluation_dataset)

    # Load the student model from a pre-trained model
    student_model = TextGenerationModel.from_pretrained("text-bison@002")

    # Start the distillation job using the teacher model and dataset
    distillation_job = student_model.distill_from(
        teacher_model=source_model,
        dataset=dataset,
        # Optional:
        train_steps=300,  # Number of training steps to use when tuning the model.
        evaluation_spec=eval_spec,
    )

    return distillation_job


# [END generativeaionvertexai_sdk_distillation]

if __name__ == "__main__":
    distill_model(
        dataset="your-dataset-uri",
        source_model="your-source-model",
        evaluation_dataset="your-evaluation-dataset-uri",
    )
