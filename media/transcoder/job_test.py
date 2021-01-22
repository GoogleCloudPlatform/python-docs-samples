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

from google.cloud import storage
from googleapiclient.errors import HttpError
import pytest
from retrying import retry

import create_job_from_ad_hoc
import create_job_from_preset
import create_job_from_template
import create_job_template
import delete_job
import delete_job_template
import get_job
import get_job_state
import list_jobs

location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
project_number = os.environ["GOOGLE_CLOUD_PROJECT_NUMBER"]
template_id = f"my-python-test-template-{uuid.uuid4()}"

bucket_name = f"python-samples-transcoder-{uuid.uuid4()}"
test_video_file_name = "ChromeCast.mp4"
input_uri = "gs://" + bucket_name + "/" + test_video_file_name
output_uri_for_preset = "gs://" + bucket_name + "/test-output-preset/"
output_uri_for_template = "gs://" + bucket_name + "/test-output-template/"
output_uri_for_adhoc = "gs://" + bucket_name + "/test-output-adhoc/"
preset = "preset/web-hd"
job_succeeded_state = "ProcessingState.SUCCEEDED"
test_data = os.path.join(os.path.dirname(__file__), "..", "testdata")
test_file = os.path.join(test_data, test_video_file_name)


@pytest.fixture(scope="module")
def test_bucket():
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    blob = bucket.blob(test_video_file_name)
    blob.upload_from_filename(test_file)
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

    _get_job_state(capsys, job_id)

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

    _get_job_state(capsys, job_id)

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

    _get_job_state(capsys, job_id)

    list_jobs.list_jobs(project_id, location)
    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_job(project_id, location, job_id)
    out, _ = capsys.readouterr()
    assert "Deleted job" in out


@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
    stop_max_attempt_number=10,
    retry_on_exception=None,
)
def _get_job_state(capsys, job_id):
    try:
        get_job_state.get_job_state(project_id, location, job_id)
    except HttpError as err:
        raise AssertionError(f"Could not get job state: {err.resp.status}")

    out, _ = capsys.readouterr()
    assert job_succeeded_state in out
