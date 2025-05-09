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

from google.genai import types

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def genai_sdk_gemini_tuning_checkpoints_set_default_example() -> types.Model:
  # [START genaisdk_gemini_tuning_checkpoints_set_default]
  from google import genai

  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location="us-central1",
  )

  name = (
      "projects/123456789012/locations/us-central1/tuningJobs/123456789012345"
  )
  tuning_job = client.tunings.get(name=name)
  tuned_model = client.models.get(model=tuning_job.tuned_model.model)

  print(f"Default checkpoint: {tuned_model.default_checkpoint_id}")
  print(f"Tuned model endpoint: {tuning_job.tuned_model.endpoint}")
  # Example response:
  # Default checkpoint: 2
  # projects/123456789012/locations/us-central1/endpoints/123456789012345

  tuned_model = client.models.update(
      model=tuned_model.name,
      config=types.UpdateModelConfig(default_checkpoint_id="1"),
  )

  print(f"Default checkpoint: {tuned_model.default_checkpoint_id}")
  print(f"Tuned model endpoint: {tuning_job.tuned_model.endpoint}")
  # Example response:
  # Default checkpoint: 1
  # projects/123456789012/locations/us-central1/endpoints/123456789000000

  # [END genaisdk_gemini_tuning_checkpoints_set_default]
  return tuned_model


if __name__ == "__main__":
  genai_sdk_gemini_tuning_checkpoints_set_default_example()
