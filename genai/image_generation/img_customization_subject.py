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

from google import genai

from google.genai.types import ControlReferenceConfig, ControlReferenceImage, EditImageConfig, EditImageResponse, Image, SubjectReferenceConfig, SubjectReferenceImage


def subject_customization(output_file: str) -> EditImageResponse:
    # [START googlegenaisdk_imagen_subject_customization]

    client = genai.Client()

    subject_image = Image(gcs_uri="gs://cloud-samples-data/generative-ai/image/person.png")

    subject_reference_image = SubjectReferenceImage(
        reference_id=1,
        reference_image=subject_image,
        config=SubjectReferenceConfig(
            subject_description="a headshot of a woman", subject_type="SUBJECT_TYPE_PERSON"
        ),
    )
    control_reference_image = ControlReferenceImage(
        reference_id=2,
        reference_image=subject_image,
        config=ControlReferenceConfig(control_type="CONTROL_TYPE_FACE_MESH"),
    )

    image = client.models.edit_image(
        model="imagen-3.0-capability-001",
        prompt="a portrait of a woman[1] in the pose of the control image[2]in a watercolor style by a professional artist, light and low-contrast stokes, bright pastel colors, a warm atmosphere, clean background, grainy paper, bold visible brushstrokes, patchy details",
        reference_images=[subject_reference_image, control_reference_image],
        config=EditImageConfig(
            edit_mode="EDIT_MODE_DEFAULT",
            number_of_images=1,
            seed=1,
            safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
            person_generation="ALLOW_ADULT",
        ),
    )

    image.generated_images[0].image._pil_image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes

    # [END googlegenaisdk_imagen_subject_customization]

    return image


if __name__ == "__main__":
    subject_customization(output_file="test_resources/img_customization.png",)
