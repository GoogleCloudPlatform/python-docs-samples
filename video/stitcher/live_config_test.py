# Copyright 2023 Google LLC
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

import create_live_config
import create_slate
import delete_live_config
import delete_slate
import get_live_config
import list_live_configs
import utils

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
now = timestamp_pb2.Timestamp()
now.GetCurrentTime()

live_config_id = f"python-test-live-config-{uuid.uuid4().hex[:5]}-{now.seconds}"

input_bucket_name = "cloud-samples-data/media/"
input_video_file_name = "hls-live/manifest.m3u8"
live_stream_uri = (
    f"https://storage.googleapis.com/{input_bucket_name}{input_video_file_name}"
)
# Single Inline Linear (https://developers.google.com/interactive-media-ads/docs/sdks/html5/client-side/tags)
ad_tag_uri = "https://pubads.g.doubleclick.net/gampad/ads?iu=/21775744923/external/single_ad_samples&sz=640x480&cust_params=sample_ct%3Dlinear&ciu_szs=300x250%2C728x90&gdfp_req=1&output=vast&unviewed_position_start=1&env=vp&impl=s&correlator="
slate_id = f"python-test-slate-{uuid.uuid4().hex[:5]}-{now.seconds}"
slate_video_file_name = "ForBiggerJoyrides.mp4"
slate_uri = f"https://storage.googleapis.com/{input_bucket_name}{slate_video_file_name}"


def test_live_config_operations(capsys: pytest.fixture) -> None:
    utils.delete_stale_slates(project_id, location)
    utils.delete_stale_live_configs(project_id, location)

    # Test setup

    slate_name = f"projects/{project_id}/locations/{location}/slates/{slate_id}"

    response = create_slate.create_slate(project_id, location, slate_id, slate_uri)
    assert slate_name in response.name

    live_config_name = (
        f"projects/{project_id}/locations/{location}/liveConfigs/{live_config_id}"
    )

    # Tests

    response = create_live_config.create_live_config(
        project_id, location, live_config_id, live_stream_uri, ad_tag_uri, slate_id
    )
    assert live_config_name in response.name

    list_live_configs.list_live_configs(project_id, location)
    out, _ = capsys.readouterr()
    assert live_config_name in out

    response = get_live_config.get_live_config(project_id, location, live_config_id)
    assert live_config_name in response.name

    response = delete_live_config.delete_live_config(
        project_id, location, live_config_id
    )
    assert response == empty.Empty()

    # Clean up slate as it is no longer needed

    response = delete_slate.delete_slate(project_id, location, slate_id)
    assert response == empty.Empty()
