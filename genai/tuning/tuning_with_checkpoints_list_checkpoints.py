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


def list_checkpoints(tuning_job_name: str) -> str:
    # [START googlegenaisdk_tuning_with_checkpoints_list_checkpoints]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Get the tuning job and the tuned model.
    # Eg. tuning_job_name = "projects/123456789012/locations/us-central1/tuningJobs/123456789012345"
    tuning_job = client.tunings.get(name=tuning_job_name)

    if tuning_job.tuned_model.checkpoints:
        for i, checkpoint in enumerate(tuning_job.tuned_model.checkpoints):
            print(f"Checkpoint {i + 1}: ", checkpoint)
    # Example response:
    # Checkpoint 1:  checkpoint_id='1' epoch=1 step=10 endpoint='projects/123456789012/locations/us-central1/endpoints/123456789000000'
    # Checkpoint 2:  checkpoint_id='2' epoch=2 step=20 endpoint='projects/123456789012/locations/us-central1/endpoints/123456789012345'

    # [END googlegenaisdk_tuning_with_checkpoints_list_checkpoints]
    return tuning_job.name


if __name__ == "__main__":
    input_tuning_job_name = input("Tuning job name: ")
    list_checkpoints(input_tuning_job_name)
