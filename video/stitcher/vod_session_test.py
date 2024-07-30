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

import create_vod_config
import create_vod_session
import delete_vod_config
import get_vod_ad_tag_detail
import get_vod_session
import get_vod_stitch_detail
import list_vod_ad_tag_details
import list_vod_stitch_details

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
project_number = os.environ["GOOGLE_CLOUD_PROJECT_NUMBER"]
location = "us-central1"
now = timestamp_pb2.Timestamp()
now.GetCurrentTime()

vod_config_id = f"python-test-vod-config-{uuid.uuid4().hex[:5]}-{now.seconds}"

input_bucket_name = "cloud-samples-data/media/"
input_video_file_name = "hls-vod/manifest.m3u8"
vod_uri = f"https://storage.googleapis.com/{input_bucket_name}{input_video_file_name}"
# VMAP Pre-roll (https://developers.google.com/interactive-media-ads/docs/sdks/html5/client-side/tags)
ad_tag_uri = "https://pubads.g.doubleclick.net/gampad/ads?iu=/21775744923/external/vmap_ad_samples&sz=640x480&cust_params=sample_ar%3Dpreonly&ciu_szs=300x250%2C728x90&gdfp_req=1&ad_rule=1&output=vmap&unviewed_position_start=1&env=vp&impl=s&correlator="


def test_vod_session_operations(capsys: pytest.fixture) -> None:
    # Test setup

    vod_config_name = (
        f"projects/{project_id}/locations/{location}/vodConfigs/{vod_config_id}"
    )

    response = create_vod_config.create_vod_config(
        project_id, location, vod_config_id, vod_uri, ad_tag_uri
    )
    assert vod_config_name in response.name

    # Tests

    request = create_vod_session.create_vod_session(project_id, location, vod_config_id)
    session_name_prefix = f"projects/{project_number}/locations/{location}/vodSessions/"
    assert session_name_prefix in request.name

    str_slice = request.name.split("/")
    session_id = str_slice[len(str_slice) - 1].rstrip("\n")
    session_name = (
        f"projects/{project_number}/locations/{location}/vodSessions/{session_id}"
    )
    assert session_name in request.name

    request = get_vod_session.get_vod_session(project_id, location, session_id)
    assert session_name in request.name

    # No list or delete methods for VOD sessions

    # Ad tag details

    response = list_vod_ad_tag_details.list_vod_ad_tag_details(
        project_id, location, session_id
    )
    out, _ = capsys.readouterr()
    ad_tag_details_name_prefix = f"projects/{project_number}/locations/{location}/vodSessions/{session_id}/vodAdTagDetails/"
    assert ad_tag_details_name_prefix in out

    str_slice = response.name.split("/")
    ad_tag_details_id = str_slice[len(str_slice) - 1].rstrip("\n")
    ad_tag_details_name = f"projects/{project_number}/locations/{location}/vodSessions/{session_id}/vodAdTagDetails/{ad_tag_details_id}"
    assert ad_tag_details_name in out

    response = get_vod_ad_tag_detail.get_vod_ad_tag_detail(
        project_id, location, session_id, ad_tag_details_id
    )
    assert ad_tag_details_name in response.name

    # Stitch details

    response = list_vod_stitch_details.list_vod_stitch_details(
        project_id, location, session_id
    )
    out, _ = capsys.readouterr()
    stitch_details_name_prefix = f"projects/{project_number}/locations/{location}/vodSessions/{session_id}/vodStitchDetails/"
    assert stitch_details_name_prefix in out

    str_slice = response.name.split("/")
    stitch_details_id = str_slice[len(str_slice) - 1].rstrip("\n")
    stitch_details_name = f"projects/{project_number}/locations/{location}/vodSessions/{session_id}/vodStitchDetails/{stitch_details_id}"
    assert stitch_details_name in out

    response = get_vod_stitch_detail.get_vod_stitch_detail(
        project_id, location, session_id, stitch_details_id
    )
    assert stitch_details_name in response.name

    # Clean up

    response = delete_vod_config.delete_vod_config(project_id, location, vod_config_id)
    assert response == empty.Empty()
