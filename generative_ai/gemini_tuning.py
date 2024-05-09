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

from typing import List

from vertexai.preview.tuning import sft


def gemini_tuning_basic(project_id: str) -> sft.SupervisedTuningJob:
    # [START generativeaionvertexai_tuning_basic]

    import time
    import vertexai
    from vertexai.preview.tuning import sft

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id)

    sft_tuning_job = sft.train(
        source_model="gemini-1.0-pro-002",
        train_dataset="gs://cloud-samples-data/ai-platform/generative_ai/sft_train_data.jsonl",
    )

    # Polling for job completion
    while not sft_tuning_job.has_ended:
        time.sleep(60)
        sft_tuning_job.refresh()

    print(sft_tuning_job.tuned_model_name)
    print(sft_tuning_job.tuned_model_endpoint_name)
    print(sft_tuning_job.experiment)
    # [END generativeaionvertexai_tuning_basic]

    return sft_tuning_job


def gemini_tuning_advanced(project_id: str) -> sft.SupervisedTuningJob:
    # [START generativeaionvertexai_tuning_advanced]

    import time
    import vertexai
    from vertexai.preview.tuning import sft

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id)

    sft_tuning_job = sft.train(
        source_model="gemini-1.0-pro-002",
        train_dataset="gs://cloud-samples-data/ai-platform/generative_ai/sft_train_data.jsonl",
        # The following parameters are optional
        validation_dataset="gs://cloud-samples-data/ai-platform/generative_ai/sft_validation_data.jsonl",
        epochs=4,
        learning_rate_multiplier=1.0,
        tuned_model_display_name="tuned_gemini_pro",
    )

    # Polling for job completion
    while not sft_tuning_job.has_ended:
        time.sleep(60)
        sft_tuning_job.refresh()

    print(sft_tuning_job.tuned_model_name)
    print(sft_tuning_job.tuned_model_endpoint_name)
    print(sft_tuning_job.experiment)
    # [END generativeaionvertexai_tuning_advanced]

    return sft_tuning_job


def get_tuning_job(
    project_id: str, location: str, tuning_job_id: str
) -> sft.SupervisedTuningJob:
    # [START generativeaionvertexai_get_tuning_job]
    import vertexai
    from vertexai.preview.tuning import sft

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # tuning_job_id = "TUNING_JOB_ID"

    vertexai.init(project=project_id)

    response = sft.SupervisedTuningJob(
        f"projects/{project_id}/locations/{location}/tuningJobs/{tuning_job_id}"
    )

    print(response)
    # [END generativeaionvertexai_get_tuning_job]

    return response


def list_tuning_jobs(
    project_id: str,
) -> List[sft.SupervisedTuningJob]:
    # [START generativeaionvertexai_list_tuning_jobs]
    import vertexai
    from vertexai.preview.tuning import sft

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id)

    responses = sft.SupervisedTuningJob.list()

    for response in responses:
        print(response)
    # [END generativeaionvertexai_list_tuning_jobs]

    return responses


def cancel_tuning_job(project_id: str, location: str, tuning_job_id: str) -> None:
    # [START generativeaionvertexai_cancel_tuning_job]
    import vertexai
    from vertexai.preview.tuning import sft

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # tuning_job_id = "TUNING_JOB_ID"

    vertexai.init(project=project_id)

    job = sft.SupervisedTuningJob(
        f"projects/{project_id}/locations/{location}/tuningJobs/{tuning_job_id}"
    )
    job.cancel()
    # [END generativeaionvertexai_cancel_tuning_job]
