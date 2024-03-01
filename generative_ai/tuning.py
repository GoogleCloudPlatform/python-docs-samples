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


from typing import Optional


from google.auth import default
from google.cloud import aiplatform
import pandas as pd
import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.preview.language_models import TuningEvaluationSpec


credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])


def tuning(
    project_id: str,
    location: str,
    model_display_name: str,
    training_data: pd.DataFrame | str,
    train_steps: int = 10,
    evaluation_dataset: Optional[str] = None,
    tensorboard_instance_name: Optional[str] = None,
) -> TextGenerationModel:
    """Tune a new model, based on a prompt-response data.

    "training_data" can be either the GCS URI of a file formatted in JSONL format
    (for example: training_data=f'gs://{bucket}/{filename}.jsonl'), or a pandas
    DataFrame. Each training example should be JSONL record with two keys, for
    example:
      {
        "input_text": <input prompt>,
        "output_text": <associated output>
      },
    or the pandas DataFame should contain two columns:
      ['input_text', 'output_text']
    with rows for each training example.

    Args:
      project_id: GCP Project ID, used to initialize vertexai
      location: GCP Region, used to initialize vertexai
      model_display_name: Customized Tuned LLM model name.
      training_data: GCS URI of jsonl file or pandas dataframe of training data.
      train_steps: Number of training steps to use when tuning the model.
      evaluation_dataset: GCS URI of jsonl file of evaluation data.
      tensorboard_instance_name: The full name of the existing Vertex AI TensorBoard instance:
        projects/PROJECT_ID/locations/LOCATION_ID/tensorboards/TENSORBOARD_INSTANCE_ID
        Note that this instance must be in the same region as your tuning job.
    """
    vertexai.init(project=project_id, location=location, credentials=credentials)
    eval_spec = TuningEvaluationSpec(evaluation_data=evaluation_dataset)
    eval_spec.tensorboard = aiplatform.Tensorboard(
        tensorboard_name=tensorboard_instance_name
    )
    model = TextGenerationModel.from_pretrained("text-bison@002")

    model.tune_model(
        training_data=training_data,
        # Optional:
        model_display_name=model_display_name,
        train_steps=train_steps,
        tuning_job_location="europe-west4",
        tuned_model_location=location,
        tuning_evaluation_spec=eval_spec,
    )

    print(model._job.status)

    return model


# [END aiplatform_sdk_tuning]
if __name__ == "__main__":
    tuning()
