# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import uuid

import backoff
from google.cloud import storage
from googleapiclient.errors import HttpError
import pytest

import create_job_from_ad_hoc
import create_job_from_preset
import create_job_from_template
import create_job_template
import create_job_with_animated_overlay
import create_job_with_concatenated_inputs
import create_job_with_embedded_captions
import create_job_with_periodic_images_spritesheet
import create_job_with_set_number_images_spritesheet
import create_job_with_standalone_captions
import create_job_with_static_overlay
import delete_job
import delete_job_template
import get_job
import get_job_state
import list_jobs

location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
project_number = os.environ["GOOGLE_CLOUD_PROJECT_NUMBER"]
template_id = f"my-python-test-template-{uuid.uuid4()}"

input_bucket_name = "cloud-samples-data/media/"
output_bucket_name = f"python-samples-transcoder-{uuid.uuid4()}"
test_video_file_name = "ChromeCast.mp4"
test_overlay_image_file_name = "overlay.jpg"
test_concat1_file_name = "ForBiggerEscapes.mp4"
test_concat2_file_name = "ForBiggerJoyrides.mp4"
test_captions_file_name = "captions.srt"
test_subtitles1_file_name = "subtitles-en.srt"
test_subtitles2_file_name = "subtitles-es.srt"

input_uri = f"gs://{input_bucket_name}{test_video_file_name}"
overlay_image_uri = f"gs://{input_bucket_name}{test_overlay_image_file_name}"
concat1_uri = f"gs://{input_bucket_name}{test_concat1_file_name}"
concat2_uri = f"gs://{input_bucket_name}{test_concat2_file_name}"
captions_uri = f"gs://{input_bucket_name}{test_captions_file_name}"
subtitles1_uri = f"gs://{input_bucket_name}{test_subtitles1_file_name}"
subtitles2_uri = f"gs://{input_bucket_name}{test_subtitles2_file_name}"
output_uri_for_preset = f"gs://{output_bucket_name}/test-output-preset/"
output_uri_for_template = f"gs://{output_bucket_name}/test-output-template/"
output_uri_for_adhoc = f"gs://{output_bucket_name}/test-output-adhoc/"
output_uri_for_static_overlay = f"gs://{output_bucket_name}/test-output-static-overlay/"
output_uri_for_animated_overlay = (
    f"gs://{output_bucket_name}/test-output-animated-overlay/"
)
output_uri_for_embedded_captions = (
    f"gs://{output_bucket_name}/test-output-embedded-captions/"
)
output_uri_for_standalone_captions = (
    f"gs://{output_bucket_name}/test-output-standalone-captions/"
)

small_spritesheet_file_prefix = "small-sprite-sheet"
large_spritesheet_file_prefix = "large-sprite-sheet"
spritesheet_file_suffix = "0000000000.jpeg"

output_dir_for_set_number_spritesheet = "test-output-set-number-spritesheet/"
output_uri_for_set_number_spritesheet = (
    f"gs://{output_bucket_name}/{output_dir_for_set_number_spritesheet}"
)
output_dir_for_periodic_spritesheet = "test-output-periodic-spritesheet/"
output_uri_for_periodic_spritesheet = (
    f"gs://{output_bucket_name}/{output_dir_for_periodic_spritesheet}"
)
output_uri_for_concat = f"gs://{output_bucket_name}/test-output-concat/"

preset = "preset/web-hd"
job_succeeded_state = "ProcessingState.SUCCEEDED"
job_running_state = "ProcessingState.RUNNING"


@pytest.fixture(scope="module")
def test_bucket():
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(output_bucket_name)

    yield bucket
    bucket.delete(force=True)


def test_create_job_from_preset(capsys, test_bucket):
    create_job_from_preset.create_job_from_preset(
        project_id, location, input_uri, output_uri_for_preset, preset
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(30)

    _assert_job_state_succeeded_or_running(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_from_template(capsys, test_bucket):

    job_template_name = (
        f"projects/{project_number}/locations/{location}/jobTemplates/{template_id}"
    )

    create_job_template.create_job_template(project_id, location, template_id)
    out, _ = capsys.readouterr()
    assert job_template_name in out

    create_job_from_template.create_job_from_template(
        project_id, location, input_uri, output_uri_for_template, template_id
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(30)

    _assert_job_state_succeeded_or_running(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out

    delete_job_template.delete_job_template(project_id, location, template_id)
    out, _ = capsys.readouterr()
    assert "Deleted job template" in out


def test_create_job_from_ad_hoc(capsys, test_bucket):
    create_job_from_ad_hoc.create_job_from_ad_hoc(
        project_id, location, input_uri, output_uri_for_adhoc
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(30)

    _assert_job_state_succeeded_or_running(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_with_static_overlay(capsys, test_bucket):
    create_job_with_static_overlay.create_job_with_static_overlay(
        project_id,
        location,
        input_uri,
        overlay_image_uri,
        output_uri_for_static_overlay,
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(30)

    _assert_job_state_succeeded(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_with_animated_overlay(capsys, test_bucket):
    create_job_with_animated_overlay.create_job_with_animated_overlay(
        project_id,
        location,
        input_uri,
        overlay_image_uri,
        output_uri_for_animated_overlay,
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(30)

    _assert_job_state_succeeded(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_with_set_number_spritesheet(capsys, test_bucket):
    create_job_with_set_number_images_spritesheet.create_job_with_set_number_images_spritesheet(
        project_id,
        location,
        input_uri,
        output_uri_for_set_number_spritesheet,
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert (
        job_name in out
    )  # Get the job name so you can use it later to get the job and delete the job.

    time.sleep(
        30
    )  # Transcoding jobs need time to complete. Once the job completes, check the job state.

    _assert_job_state_succeeded(capsys, job_id)
    _assert_file_in_bucket(
        capsys,
        test_bucket,
        output_dir_for_set_number_spritesheet
        + small_spritesheet_file_prefix
        + spritesheet_file_suffix,
    )
    _assert_file_in_bucket(
        capsys,
        test_bucket,
        output_dir_for_set_number_spritesheet
        + large_spritesheet_file_prefix
        + spritesheet_file_suffix,
    )

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_with_periodic_spritesheet(capsys, test_bucket):
    create_job_with_periodic_images_spritesheet.create_job_with_periodic_images_spritesheet(
        project_id,
        location,
        input_uri,
        output_uri_for_periodic_spritesheet,
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert (
        job_name in out
    )  # Get the job name so you can use it later to get the job and delete the job.

    time.sleep(
        30
    )  # Transcoding jobs need time to complete. Once the job completes, check the job state.

    _assert_job_state_succeeded(capsys, job_id)
    _assert_file_in_bucket(
        capsys,
        test_bucket,
        output_dir_for_periodic_spritesheet
        + small_spritesheet_file_prefix
        + spritesheet_file_suffix,
    )
    _assert_file_in_bucket(
        capsys,
        test_bucket,
        output_dir_for_periodic_spritesheet
        + large_spritesheet_file_prefix
        + spritesheet_file_suffix,
    )

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_with_concatenated_inputs(capsys, test_bucket):
    create_job_with_concatenated_inputs.create_job_with_concatenated_inputs(
        project_id,
        location,
        concat1_uri,
        "0s",
        "8.1s",
        concat2_uri,
        "3.5s",
        "15s",
        output_uri_for_concat,
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(
        30
    )  # Transcoding jobs need time to complete. Once the job completes, check the job state.

    _assert_job_state_succeeded(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_with_embedded_captions(capsys, test_bucket):
    create_job_with_embedded_captions.create_job_with_embedded_captions(
        project_id,
        location,
        input_uri,
        captions_uri,
        output_uri_for_embedded_captions,
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(
        30
    )  # Transcoding jobs need time to complete. Once the job completes, check the job state.

    _assert_job_state_succeeded(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


def test_create_job_with_standalone_captions(capsys, test_bucket):
    create_job_with_standalone_captions.create_job_with_standalone_captions(
        project_id,
        location,
        input_uri,
        subtitles1_uri,
        subtitles2_uri,
        output_uri_for_standalone_captions,
    )
    out, _ = capsys.readouterr()
    job_name_prefix = f"projects/{project_number}/locations/{location}/jobs/"
    assert job_name_prefix in out

    str_slice = out.split("/")
    job_id = str_slice[len(str_slice) - 1].rstrip("\n")
    job_name = f"projects/{project_number}/locations/{location}/jobs/{job_id}"
    assert job_name in out

    get_job.get_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert job_name in out

    time.sleep(
        30
    )  # Transcoding jobs need time to complete. Once the job completes, check the job state.

    _assert_job_state_succeeded(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


# Retrying up to 10 mins. This function checks if the job completed
# successfully.
@backoff.on_exception(backoff.expo, AssertionError, max_time=600)
def _assert_job_state_succeeded(capsys, job_id):
    try:
        get_job_state.get_job_state(project_id, location, job_id)
    except HttpError as err:
        raise AssertionError(f"Could not get job state: {err.resp.status}")

    out, _ = capsys.readouterr()
    assert job_succeeded_state in out


# Retrying up to 10 mins. This function checks if the job is running or has
# completed. Both of these conditions signal the API is functioning. The test
# can list or delete a job that is running or completed with no ill effects.
@backoff.on_exception(backoff.expo, AssertionError, max_time=600)
def _assert_job_state_succeeded_or_running(capsys, job_id):
    try:
        get_job_state.get_job_state(project_id, location, job_id)
    except HttpError as err:
        raise AssertionError(f"Could not get job state: {err.resp.status}")

    out, _ = capsys.readouterr()
    assert (job_succeeded_state in out) or (job_running_state in out)


def _assert_file_in_bucket(capsys, test_bucket, directory_and_filename):
    blob = test_bucket.blob(directory_and_filename)
    assert blob.exists()
