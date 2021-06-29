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
import typing
import uuid

import google.auth
import google.cloud.storage as storage
import pytest

from sample_default_values import \
    disable_usage_export, get_usage_export_bucket, set_usage_export_bucket

PROJECT = google.auth.default()[1]
BUCKET_NAME = "test" + uuid.uuid4().hex[:10]
TEST_PREFIX = 'some-prefix'


@pytest.fixture
def temp_bucket():
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)
    yield bucket
    bucket.delete(force=True)


def test_set_usage_export_bucket_default(capsys: typing.Any,
                                         temp_bucket: storage.Bucket) -> None:
    set_usage_export_bucket(project_id=PROJECT, bucket_name=temp_bucket.name)
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert(uel.bucket_name == temp_bucket.name)
    assert(uel.report_name_prefix == 'usage_gce')
    out, _ = capsys.readouterr()
    assert('default prefix of `usage_gce`.' in out)

    disable_usage_export(project_id=PROJECT)
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert(uel.bucket_name == '')
    assert(uel.report_name_prefix == '')


def test_set_usage_export_bucket_custom(capsys: typing.Any,
                                        temp_bucket: storage.Bucket) -> None:
    set_usage_export_bucket(project_id=PROJECT, bucket_name=temp_bucket.name,
                            report_name_prefix=TEST_PREFIX)
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert(uel.bucket_name == temp_bucket.name)
    assert(uel.report_name_prefix == TEST_PREFIX)
    out, _ = capsys.readouterr()
    assert('usage_gce' not in out)

    disable_usage_export(project_id=PROJECT)
    uel = get_usage_export_bucket(project_id=PROJECT)
    assert(uel.bucket_name == '')
    assert(uel.report_name_prefix == '')
