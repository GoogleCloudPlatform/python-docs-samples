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

# [START generativeai_sdk_tuning]
from typing import Union
import pandas as pd

from vertex_ai.preview.language_models import TextGenerationModel, TextEmbeddingModel
from google.cloud import aiplatform


def tuning(
    project_id: str,
    location: str,
    training_data: Union[pd.DataFrame, str],
    train_steps: int = 10,
):
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
    project_id: GCP Project ID, used to initialize aiplatform
    location: GCP Region, used to initialize aiplatform
    training_data: GCS URI of training file or pandas dataframe of training data
    train_steps: Number of training steps to use when tuning the model.
  """
  aiplatform.init(project=project_id, location=location)
  model = TextGenerationModel.from_pretrained("text-bison@001")

  model.tune_model(
    training_data=training_data,
    # Optional:
    train_steps=1,
    tuning_job_location="us-south1",
    tuned_model_location="us-south1",
  )

  # Test the tuned model:
  response = model.predict("Tell me some ideas combining VR and fitness:")
  print(f"Response from Model: {response.text}")
# [END generativeai_sdk_tune_model]

  return response


if __name__ == "__main__":
    tuning()
