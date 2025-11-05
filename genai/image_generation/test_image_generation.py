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

#
# Using Google Cloud Vertex AI to test the code samples.
#

from datetime import datetime as dt

import os

from google.cloud import storage

import pytest

import imggen_canny_ctrl_type_with_txt_img
import imggen_inpainting_insert_mask_with_txt_img
import imggen_inpainting_insert_with_txt_img
import imggen_inpainting_removal_mask_with_txt_img
import imggen_inpainting_removal_with_txt_img
import imggen_mask_free_edit_with_txt_img
import imggen_outpainting_with_txt_img
import imggen_product_background_mask_with_txt_img
import imggen_product_background_with_txt_img
import imggen_raw_reference_with_txt_img
import imggen_scribble_ctrl_type_with_txt_img
import imggen_style_reference_with_txt_img
import imggen_subj_refer_ctrl_refer_with_txt_imgs
import imggen_upscale_with_img
import imggen_virtual_try_on_with_txt_img
import imggen_with_txt

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"

GCS_OUTPUT_BUCKET = "python-docs-samples-tests"
RESOURCES = os.path.join(os.path.dirname(__file__), "test_resources")


@pytest.fixture(scope="session")
def output_gcs_uri() -> str:
    prefix = f"text_output/{dt.now()}"

    yield f"gs://{GCS_OUTPUT_BUCKET}/{prefix}"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCS_OUTPUT_BUCKET)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        blob.delete()


def test_img_generation() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "dog_newspaper.png")
    response = imggen_with_txt.generate_images(OUTPUT_FILE)
    assert response


def test_img_edit_inpainting_insert_with_mask() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "fruit_edit.png")
    response = imggen_inpainting_insert_mask_with_txt_img.edit_inpainting_insert_mask(OUTPUT_FILE)
    assert response


def test_img_edit_inpainting_insert() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "fruit_edit.png")
    response = imggen_inpainting_insert_with_txt_img.edit_inpainting_insert(OUTPUT_FILE)
    assert response


def test_img_edit_inpainting_removal_mask() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "fruit_edit.png")
    response = imggen_inpainting_removal_mask_with_txt_img.edit_inpainting_removal_mask(OUTPUT_FILE)
    assert response


def test_img_edit_inpainting_removal() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "fruit_edit.png")
    response = imggen_inpainting_removal_with_txt_img.edit_inpainting_removal(OUTPUT_FILE)
    assert response


def test_img_edit_product_background_mask() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "suitcase_edit.png")
    response = imggen_product_background_mask_with_txt_img.edit_product_background_mask(OUTPUT_FILE)
    assert response


def test_img_edit_product_background() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "suitcase_edit.png")
    response = imggen_product_background_with_txt_img.edit_product_background(OUTPUT_FILE)
    assert response


def test_img_edit_outpainting() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "living_room_edit.png")
    response = imggen_outpainting_with_txt_img.edit_outpainting(OUTPUT_FILE)
    assert response


def test_img_edit_mask_free() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "latte_edit.png")
    response = imggen_mask_free_edit_with_txt_img.edit_mask_free(OUTPUT_FILE)
    assert response


def test_img_customization_subject(output_gcs_uri: str) -> None:
    response = imggen_subj_refer_ctrl_refer_with_txt_imgs.subject_customization(
        output_gcs_uri=output_gcs_uri
    )
    assert response


def test_img_customization_style(output_gcs_uri: str) -> None:
    response = imggen_style_reference_with_txt_img.style_customization(output_gcs_uri=output_gcs_uri)
    assert response


def test_img_customization_style_transfer(output_gcs_uri: str) -> None:
    response = imggen_raw_reference_with_txt_img.style_transfer_customization(output_gcs_uri=output_gcs_uri)
    assert response


def test_img_customization_scribble(output_gcs_uri: str) -> None:
    response = imggen_scribble_ctrl_type_with_txt_img.scribble_customization(output_gcs_uri=output_gcs_uri)
    assert response


def test_img_customization_canny_edge(output_gcs_uri: str) -> None:
    response = imggen_canny_ctrl_type_with_txt_img.canny_edge_customization(output_gcs_uri=output_gcs_uri)
    assert response


def test_img_virtual_try_on() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "man_in_sweater.png")
    response = imggen_virtual_try_on_with_txt_img.virtual_try_on(OUTPUT_FILE)
    assert response


def test_img_upscale() -> None:
    OUTPUT_FILE = os.path.join(RESOURCES, "dog_newspaper.png")
    response = imggen_upscale_with_img.upscale_images(OUTPUT_FILE)
    assert response
