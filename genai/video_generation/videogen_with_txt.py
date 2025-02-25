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


def generate_videos(output_gcs_uri: str) -> str:
    # [START googlegenaisdk_videogen_with_txt]
    import time
    from google import genai
    from google.genai.types import GenerateVideosConfig

    client = genai.Client()
    prompt = "A person skiing down a snow covered mountain."

    # TODO(developer): Update and un-comment below line
    # output_gcs_uri = "gs://your-bucket/your-prefix"

    operation = client.models.generate_videos(
        model="veo-2.0-generate-001",
        prompt=prompt,
        config=GenerateVideosConfig(
            aspect_ratio="16:9",
            output_gcs_uri=output_gcs_uri,
        ),
    )

    print(operation)
    while not operation.done:
        time.sleep(20)
        operation = client.models.get_generate_videos_operation(operation.name)
        print(operation)

    if operation.response:
        print(operation.generate_videos_response.videos[0].uri)

    # Example response:
    # gs://your-bucket/your-prefix
    # [END googlegenaisdk_videogen_with_txt]
    return operation.generate_videos_response.videos[0].uri


if __name__ == "__main__":
    generate_videos(output_gcs_uri="gs://your-bucket/your-prefix")
