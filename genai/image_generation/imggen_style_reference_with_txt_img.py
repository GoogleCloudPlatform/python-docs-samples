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


def style_customization(output_gcs_uri: str) -> str:
    # [START googlegenaisdk_imggen_style_reference_with_txt_img]
    from google import genai
    from google.genai.types import EditImageConfig, Image, StyleReferenceConfig, StyleReferenceImage

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_gcs_uri = "gs://your-bucket/your-prefix"

    # Create a style reference image of a neon sign stored in Google Cloud Storage
    # using https://storage.googleapis.com/cloud-samples-data/generative-ai/image/neon.png
    style_reference_image = StyleReferenceImage(
        reference_id=1,
        reference_image=Image(gcs_uri="gs://cloud-samples-data/generative-ai/image/neon.png"),
        config=StyleReferenceConfig(style_description="neon sign"),
    )

    image = client.models.edit_image(
        model="imagen-3.0-capability-001",
        prompt="generate an image of a neon sign [1] with the words: have a great day",
        reference_images=[style_reference_image],
        config=EditImageConfig(
            edit_mode="EDIT_MODE_DEFAULT",
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
    # [END googlegenaisdk_imggen_style_reference_with_txt_img]
    return image.generated_images[0].image.gcs_uri


if __name__ == "__main__":
    style_customization(output_gcs_uri="gs://your-bucket/your-prefix")
