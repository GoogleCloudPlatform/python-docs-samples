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


def generate_videos_from_image(output_gcs_uri: str) -> str:
    # [START googlegenaisdk_videogen_with_img]
    import time
    from google import genai
    from google.genai.types import GenerateVideosConfig, Image

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_gcs_uri = "gs://your-bucket/your-prefix"

    operation = client.models.generate_videos(
        model="veo-3.0-generate-preview",
        image=Image(
            gcs_uri="gs://cloud-samples-data/generative-ai/image/flowers.png",
            mime_type="image/png",
        ),
        config=GenerateVideosConfig(
            aspect_ratio="16:9",
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
    # [END googlegenaisdk_videogen_with_img]
    return operation.result.generated_videos[0].video.uri


if __name__ == "__main__":
    generate_videos_from_image(output_gcs_uri="gs://your-bucket/your-prefix")
