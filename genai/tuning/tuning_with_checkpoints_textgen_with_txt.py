# Copyright 2025 Google LLC
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


def test_checkpoint(name: str) -> str:
    # [START googlegenaisdk_tuning_with_checkpoints_test]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Get the tuning job and the tuned model.
    # Eg. name = "projects/123456789012/locations/us-central1/tuningJobs/123456789012345"
    tuning_job = client.tunings.get(name=name)

    contents = "Why is the sky blue?"

    # Tests the default checkpoint
    response = client.models.generate_content(
        model=tuning_job.tuned_model.endpoint,
        contents=contents,
    )
    print(response.text)

    # Tests Checkpoint 1
    checkpoint1_response = client.models.generate_content(
        model=tuning_job.tuned_model.checkpoints[0].endpoint,
        contents=contents,
    )
    print(checkpoint1_response.text)

    # Tests Checkpoint 2
    checkpoint2_response = client.models.generate_content(
        model=tuning_job.tuned_model.checkpoints[1].endpoint,
        contents=contents,
    )
    print(checkpoint2_response.text)

    # [END googlegenaisdk_tuning_with_checkpoints_test]
    return response.text


if __name__ == "__main__":
    tuning_job_name = input("Tuning job name: ")
    test_checkpoint(tuning_job_name)
