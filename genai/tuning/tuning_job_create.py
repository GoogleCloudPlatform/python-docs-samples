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


def create_tuning_job() -> str:
    # [START googlegenaisdk_tuning_job_create]
    import time

    from google import genai
    from google.genai.types import HttpOptions, CreateTuningJobConfig

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    tuning_job = client.tunings.tune(
        base_model="gemini-2.0-flash-lite-001",
        training_dataset="gs://cloud-samples-data/ai-platform/generative_ai/gemini-2_0/text/sft_train_data.jsonl",
        config=CreateTuningJobConfig(
            tuned_model_display_name="Example tuning job",
        ),
    )

    running_states = set([
        "JOB_STATE_PENDING",
        "JOB_STATE_RUNNING",
    ])

    while tuning_job.state in running_states:
        print(tuning_job.state)
        tuning_job = client.tunings.get(name=tuning_job.name)
        time.sleep(60)

    print(tuning_job.tuned_model.model)
    print(tuning_job.tuned_model.endpoint)
    print(tuning_job.experiment)
    # Example response:
    # projects/123456789012/locations/us-central1/models/1234567890@1
    # projects/123456789012/locations/us-central1/endpoints/123456789012345
    # projects/123456789012/locations/us-central1/metadataStores/default/contexts/tuning-experiment-2025010112345678

    if tuning_job.tuned_model.checkpoints:
        for i, checkpoint in enumerate(tuning_job.tuned_model.checkpoints):
            print(f"Checkpoint {i + 1}: ", checkpoint)
        # Example response:
        # Checkpoint 1:  checkpoint_id='1' epoch=1 step=10 endpoint='projects/123456789012/locations/us-central1/endpoints/123456789000000'
        # Checkpoint 2:  checkpoint_id='2' epoch=2 step=20 endpoint='projects/123456789012/locations/us-central1/endpoints/123456789012345'

    # [END googlegenaisdk_tuning_job_create]
    return tuning_job.name


if __name__ == "__main__":
    create_tuning_job()
