# Copyright 2024 Google LLC
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

import create_vod_config
import delete_vod_config
import get_vod_config
import list_vod_configs
import update_vod_config
import utils

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
now = timestamp_pb2.Timestamp()
now.GetCurrentTime()

vod_config_id = f"python-test-vod-config-{uuid.uuid4().hex[:5]}-{now.seconds}"

input_bucket_name = "cloud-samples-data/media/"
input_video_file_name = "hls-vod/manifest.m3u8"
updated_input_video_file_name = "hls-vod/manifest.mpd"
vod_uri = f"https://storage.googleapis.com/{input_bucket_name}{input_video_file_name}"
updated_vod_uri = (
    f"https://storage.googleapis.com/{input_bucket_name}{updated_input_video_file_name}"
)
# VMAP Pre-roll (https://developers.google.com/interactive-media-ads/docs/sdks/html5/client-side/tags)
ad_tag_uri = "https://pubads.g.doubleclick.net/gampad/ads?iu=/21775744923/external/vmap_ad_samples&sz=640x480&cust_params=sample_ar%3Dpreonly&ciu_szs=300x250%2C728x90&gdfp_req=1&ad_rule=1&output=vmap&unviewed_position_start=1&env=vp&impl=s&correlator="


def test_vod_config_operations(capsys: pytest.fixture) -> None:
    utils.delete_stale_vod_configs(project_id, location)

    # Test setup

    vod_config_name = (
        f"projects/{project_id}/locations/{location}/vodConfigs/{vod_config_id}"
    )

    # Tests

    response = create_vod_config.create_vod_config(
        project_id, location, vod_config_id, vod_uri, ad_tag_uri
    )
    assert vod_config_name in response.name

    list_vod_configs.list_vod_configs(project_id, location)
    out, _ = capsys.readouterr()
    assert vod_config_name in out

    response = update_vod_config.update_vod_config(
        project_id, location, vod_config_id, updated_vod_uri
    )
    assert vod_config_name in response.name

    response = get_vod_config.get_vod_config(project_id, location, vod_config_id)
    assert vod_config_name in response.name

    response = delete_vod_config.delete_vod_config(project_id, location, vod_config_id)
    assert response == empty.Empty()
