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


def generate_content(PROJECT_ID: str, REGION: str) -> dict:
    # [START generativeaionvertexai_tuning_basic]
    import vertexai
    from vertexai.preview import tuning
    from vertexai.preview.tuning import sft
    
    vertexai.init(project=PROJECT_ID, location=REGION)

    sft_tuning_job = sft.train(
        source_model="gemini-1.0-pro-002",
        train_dataset="gs://cloud-samples-data/ai-platform/generative_ai/sft_train_data.jsonl",
    )
    
    responses = sft_tuning_job.to_dict()
    
    for response in responses:
        print(response)
    # [END generativeaionvertexai_tuning_basic]

    return responses