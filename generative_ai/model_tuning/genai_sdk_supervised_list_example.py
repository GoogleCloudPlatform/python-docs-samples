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


def genai_sdk_list_tuning_jobs() -> List[types.TuningJob]:
  # [START genaisdk_gemini_list_tuning_jobs]
  from google import genai

  # TODO(developer): Update and un-comment below lines
  # PROJECT_ID = "your-project-id"
  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location="us-central1",
  )

  responses = client.tunings.list()
  for response in responses:
    print(response)
  # Example response:
  # name='projects/123456789012/locations/us-central1/tuningJobs/123456789012345' state=<JobState.JOB_STATE_RUNNING: 'JOB_STATE_RUNNING'> ...

  # [END genaisdk_gemini_list_tuning_jobs]
  return responses


if __name__ == "__main__":
  genai_sdk_list_tuning_jobs()
