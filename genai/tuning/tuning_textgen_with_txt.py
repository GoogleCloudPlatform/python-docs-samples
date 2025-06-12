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


def predict_with_tuned_endpoint(tuning_job_name: str) -> str:
    # [START googlegenaisdk_tuning_textgen_with_txt]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Get the tuning job and the tuned model.
    # Eg. tuning_job_name = "projects/123456789012/locations/us-central1/tuningJobs/123456789012345"
    tuning_job = client.tunings.get(name=tuning_job_name)

    contents = "Why is the sky blue?"

    # Predicts with the tuned endpoint.
    response = client.models.generate_content(
        model=tuning_job.tuned_model.endpoint,
        contents=contents,
    )
    print(response.text)
    # Example response:
    # The sky is blue because ...

    # [END googlegenaisdk_tuning_textgen_with_txt]
    return response.text


if __name__ == "__main__":
    input_tuning_job_name = input("Tuning job name: ")
    predict_with_tuned_endpoint(input_tuning_job_name)
