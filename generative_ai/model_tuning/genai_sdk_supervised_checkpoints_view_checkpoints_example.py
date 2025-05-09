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
from typing import List

from google.genai import types

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def genai_sdk_gemini_tuning_checkpoints_view_checkpoints() -> types.TuningJob:
  # [START genaisdk_gemini_tuning_checkpoints_view_checkpoints]
  from google import genai

  # TODO(developer): Update and un-comment below lines
  # PROJECT_ID = "your-project-id"
  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location="us-central1",
  )

  name = (
      "projects/123456789012/locations/us-central1/tuningJobs/123456789012345"
  )
  tuning_job = client.tunings.get(name=name)

  if tuning_job.tuned_model.checkpoints:
    for i in range(len(tuning_job.tuned_model.checkpoints)):
      checkpoint = tuning_job.tuned_model.checkpoints[i]
      print(f"Checkpoint {i + 1}: ", checkpoint)
  # Example response:
  # Checkpoint 1:  checkpoint_id='1' epoch=1 step=10 endpoint='projects/123456789012/locations/us-central1/endpoints/123456789000000'
  # Checkpoint 2:  checkpoint_id='2' epoch=2 step=20 endpoint='projects/123456789012/locations/us-central1/endpoints/123456789012345'

  # [END genaisdk_gemini_tuning_checkpoints_view_checkpoints]
  return tuning_job


if __name__ == "__main__":
  genai_sdk_gemini_tuning_checkpoints_view_checkpoints()
