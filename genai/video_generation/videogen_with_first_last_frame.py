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


def generate_videos_from_first_last_frame(output_gcs_uri: str) -> str:
    # [START googlegenaisdk_videogen_with_first_last_frame]
    import time
    from google import genai
    from google.genai.types import GenerateVideosConfig, Image

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_gcs_uri = "gs://your-bucket/your-prefix"

    operation = client.models.generate_videos(
        model="veo-3.1-generate-001",
        prompt="a hand reaches in and places a glass of milk next to the plate of cookies",
        image=Image(
            gcs_uri="gs://cloud-samples-data/generative-ai/image/cookies.png",
            mime_type="image/png",
        ),
        config=GenerateVideosConfig(
            aspect_ratio="16:9",
            last_frame=Image(
                gcs_uri="gs://cloud-samples-data/generative-ai/image/cookies-milk.png",
                mime_type="image/png",
            ),
            output_gcs_uri=output_gcs_uri,
        ),
    )

    while not operation.done:
        time.sleep(15)
        operation = client.operations.get(operation)
        print(operation)

    if operation.response:
        print(operation.result.generated_videos[0].video.uri)

    # Example response:
    # gs://your-bucket/your-prefix
    # [END googlegenaisdk_videogen_with_first_last_frame]
    return operation.result.generated_videos[0].video.uri


if __name__ == "__main__":
    generate_videos_from_first_last_frame(output_gcs_uri="gs://your-bucket/your-prefix")
