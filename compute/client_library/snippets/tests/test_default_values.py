# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time
import typing
import uuid

from flaky import flaky
import google.auth
import google.cloud.storage as storage
import pytest

from ..usage_report.usage_reports import disable_usage_export
from ..usage_report.usage_reports import get_usage_export_bucket
from ..usage_report.usage_reports import set_usage_export_bucket

PROJECT = google.auth.default()[1]
BUCKET_NAME = "test" + uuid.uuid4().hex[:10]
TEST_PREFIX = "some-prefix"


@pytest.fixture
def temp_bucket():
    storage_client = storage.Client()

    # Get exclusive lock for testing. Lock bucket name is compute-snippets-lock.

    lock_name = "compute-snippets-lock"
    for _ in range(10):
        try:
            lock_bucket = storage_client.create_bucket(lock_name)
            break
        except google.cloud.exceptions.Conflict:
            time.sleep(30)

    bucket = storage_client.create_bucket(BUCKET_NAME)
    yield bucket

    lock_bucket.delete(force=True)
    bucket.delete(force=True)


@flaky(max_runs=3)
def test_set_usage_export_bucket_default(
    capsys: typing.Any, temp_bucket: storage.Bucket
) -> None:
    set_usage_export_bucket(project_id=PROJECT, bucket_name=temp_bucket.name)
    time.sleep(5)  # To make sure the settings are properly updated
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert uel.bucket_name == temp_bucket.name
    assert uel.report_name_prefix == "usage_gce"
    out, _ = capsys.readouterr()
    assert "default prefix of `usage_gce`." in out

    disable_usage_export(project_id=PROJECT)
    time.sleep(5)  # To make sure the settings are properly updated
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert uel.bucket_name == ""
    assert uel.report_name_prefix == ""

    # Testing setting a custom export bucket. Keeping this in one test function
    # to avoid race conditions, as this is a global setting for the project.
    set_usage_export_bucket(
        project_id=PROJECT, bucket_name=temp_bucket.name, report_name_prefix=TEST_PREFIX
    )
    time.sleep(5)  # To make sure the settings are properly updated
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert uel.bucket_name == temp_bucket.name
    assert uel.report_name_prefix == TEST_PREFIX
    out, _ = capsys.readouterr()
    assert "usage_gce" not in out

    disable_usage_export(project_id=PROJECT)
    time.sleep(5)  # To make sure the settings are properly updated
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert uel.bucket_name == ""
    assert uel.report_name_prefix == ""
