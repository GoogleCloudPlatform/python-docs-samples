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


def set_default_checkpoint(tuning_job_name: str, checkpoint_id: str) -> str:
    # [START googlegenaisdk_tuning_with_checkpoints_set_default]
    from google import genai
    from google.genai.types import HttpOptions, UpdateModelConfig

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Get the tuning job and the tuned model.
    # Eg. tuning_job_name = "projects/123456789012/locations/us-central1/tuningJobs/123456789012345"
    tuning_job = client.tunings.get(name=tuning_job_name)
    tuned_model = client.models.get(model=tuning_job.tuned_model.model)

    print(f"Default checkpoint: {tuned_model.default_checkpoint_id}")
    print(f"Tuned model endpoint: {tuning_job.tuned_model.endpoint}")
    # Example response:
    # Default checkpoint: 2
    # projects/123456789012/locations/us-central1/endpoints/123456789012345

    # Set a new default checkpoint.
    # Eg. checkpoint_id = "1"
    tuned_model = client.models.update(
        model=tuned_model.name,
        config=UpdateModelConfig(default_checkpoint_id=checkpoint_id),
    )

    print(f"Default checkpoint: {tuned_model.default_checkpoint_id}")
    print(f"Tuned model endpoint: {tuning_job.tuned_model.endpoint}")
    # Example response:
    # Default checkpoint: 1
    # projects/123456789012/locations/us-central1/endpoints/123456789000000

    # [END googlegenaisdk_tuning_with_checkpoints_set_default]
    return tuned_model.default_checkpoint_id


if __name__ == "__main__":
    input_tuning_job_name = input("Tuning job name: ")
    default_checkpoint_id = input("Default checkpoint id: ")
    set_default_checkpoint(input_tuning_job_name, default_checkpoint_id)
