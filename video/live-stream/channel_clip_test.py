# Copyright 2024 Google LLC.
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
import subprocess
import uuid

from google.cloud import storage
from google.protobuf import empty_pb2 as empty
import pytest

import create_channel
import create_channel_clip
import create_input
import delete_channel
import delete_channel_clip
import delete_input
import get_channel_clip
import list_channel_clips
import start_channel
import stop_channel

project_name = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
input_id = f"python-test-input-{uuid.uuid4()}"
channel_id = f"python-test-channel-{uuid.uuid4()}"
clip_id = f"python-test-clip-{uuid.uuid4()}"
output_bucket_name = f"python-test-bucket-{uuid.uuid4()}"
output_uri = f"gs://{output_bucket_name}/channel-test/"
clip_output_uri = f"gs://{output_bucket_name}/channel-test/clips"


@pytest.fixture(scope="module")
def test_bucket() -> None:
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(output_bucket_name)

    yield bucket
    bucket.delete(force=True)


def test_channel_clip_operations(
    capsys: pytest.fixture, test_bucket: pytest.fixture
) -> None:
    # Set up. ffmpeg must be installed.

    clip_name_project_id = f"projects/{project_name}/locations/{location}/channels/{channel_id}/clips/{clip_id}"

    input = create_input.create_input(project_name, location, input_id)

    create_channel.create_channel(
        project_name, location, channel_id, input_id, output_uri
    )

    start_channel.start_channel(project_name, location, channel_id)

    command = (
        'ffmpeg -re -f lavfi -t 45 -i "testsrc=size=1280x720 [out0]; sine=frequency=500 [out1]" -acodec aac -vcodec h264 -f flv '
        + input.uri
    )

    subprocess.run(
        command,
        capture_output=True,
        shell=True,
        check=True,
    )

    # Tests

    response = create_channel_clip.create_channel_clip(
        project_name, location, channel_id, clip_id, clip_output_uri
    )
    assert clip_name_project_id in response.name

    response = get_channel_clip.get_channel_clip(
        project_name, location, channel_id, clip_id
    )
    assert clip_name_project_id in response.name

    list_channel_clips.list_channel_clips(project_name, location, channel_id)
    out, _ = capsys.readouterr()
    assert clip_name_project_id in out

    response = delete_channel_clip.delete_channel_clip(
        project_name, location, channel_id, clip_id
    )
    assert response == empty.Empty()

    # Clean up

    stop_channel.stop_channel(project_name, location, channel_id)
    delete_channel.delete_channel(project_name, location, channel_id)
    delete_input.delete_input(project_name, location, input_id)
