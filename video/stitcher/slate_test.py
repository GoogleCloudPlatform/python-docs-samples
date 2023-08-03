# Copyright 2022 Google LLC
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
import uuid

from google.protobuf import empty_pb2 as empty
from google.protobuf import timestamp_pb2
import pytest

import create_slate
import delete_slate
import get_slate
import list_slates
import update_slate
import utils

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
now = timestamp_pb2.Timestamp()
now.GetCurrentTime()

input_bucket_name = "cloud-samples-data/media/"
slate_video_file_name = "ForBiggerEscapes.mp4"
updated_slate_video_file_name = "ForBiggerJoyrides.mp4"
slate_id = f"python-test-slate-{uuid.uuid4().hex[:5]}-{now.seconds}"
slate_uri = f"https://storage.googleapis.com/{input_bucket_name}{slate_video_file_name}"
updated_slate_uri = (
    f"https://storage.googleapis.com/{input_bucket_name}{updated_slate_video_file_name}"
)


def test_slate_operations(capsys: pytest.fixture) -> None:
    utils.delete_stale_slates(project_id, location)

    slate_name_project_id = (
        f"projects/{project_id}/locations/{location}/slates/{slate_id}"
    )

    response = create_slate.create_slate(project_id, location, slate_id, slate_uri)
    assert slate_name_project_id in response.name

    list_slates.list_slates(project_id, location)
    out, _ = capsys.readouterr()
    assert slate_name_project_id in out

    response = update_slate.update_slate(
        project_id, location, slate_id, updated_slate_uri
    )
    assert slate_name_project_id in response.name
    assert updated_slate_uri in response.uri

    response = get_slate.get_slate(project_id, location, slate_id)
    assert slate_name_project_id in response.name

    response = delete_slate.delete_slate(project_id, location, slate_id)
    assert response == empty.Empty()
