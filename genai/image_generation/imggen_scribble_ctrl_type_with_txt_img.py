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


def scribble_customization(output_gcs_uri: str) -> str:
    # [START googlegenaisdk_imggen_scribble_ctrl_type_with_txt_img]
    from google import genai
    from google.genai.types import ControlReferenceConfig, ControlReferenceImage, EditImageConfig, Image

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_gcs_uri = "gs://your-bucket/your-prefix"

    # Create a reference image out of an existing scribble image signal
    # using https://storage.googleapis.com/cloud-samples-data/generative-ai/image/car_scribble.png
    control_reference_image = ControlReferenceImage(
        reference_id=1,
        reference_image=Image(gcs_uri="gs://cloud-samples-data/generative-ai/image/car_scribble.png"),
        config=ControlReferenceConfig(control_type="CONTROL_TYPE_SCRIBBLE"),
    )

    image = client.models.edit_image(
        model="imagen-3.0-capability-001",
        prompt="an oil painting showing the side of a red car[1]",
        reference_images=[control_reference_image],
        config=EditImageConfig(
            edit_mode="EDIT_MODE_CONTROLLED_EDITING",
            number_of_images=1,
            seed=1,
            safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
            person_generation="ALLOW_ADULT",
            output_gcs_uri=output_gcs_uri,
        ),
    )

    # Example response:
    # gs://your-bucket/your-prefix
    print(image.generated_images[0].image.gcs_uri)
    # [END googlegenaisdk_imggen_scribble_ctrl_type_with_txt_img]
    return image.generated_images[0].image.gcs_uri


if __name__ == "__main__":
    scribble_customization(output_gcs_uri="gs://your-bucket/your-prefix")
