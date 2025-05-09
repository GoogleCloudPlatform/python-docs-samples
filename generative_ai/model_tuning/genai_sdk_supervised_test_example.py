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

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def genai_sdk_gemini_test_tuned_endpoint() -> str:
  # [START genaisdk_gemini_test_tuned_endpoint]
  from google import genai

  # TODO(developer): Update and un-comment below lines
  # PROJECT_ID = "your-project-id"
  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location="us-central1",
  )

  name = "projects/12345678/locations/us-central1/tuningJobs/123456789012345"
  tuning_job = client.tunings.get(name=name)

  contents = "Why is the sky blue?"

  # Tests the tuned model Endpoint.
  # If intermediate checkpoints are enabled, the tuned model Endpoint will be the default checkpoint Endpoint.
  response = client.models.generate_content(
      model=tuning_job.tuned_model.endpoint,
      contents=contents,
  )
  print(response.text)

  # [END genaisdk_gemini_test_tuned_endpoint]
  return response.text


if __name__ == "__main__":
  genai_sdk_gemini_test_tuned_endpoint()
