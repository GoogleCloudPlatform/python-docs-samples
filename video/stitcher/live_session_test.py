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
import re
import uuid

from google.protobuf import empty_pb2 as empty
from google.protobuf import timestamp_pb2
import pytest
import requests

import create_live_config
import create_live_session
import create_slate
import delete_live_config
import delete_slate
import get_live_ad_tag_detail
import get_live_session
import list_live_ad_tag_details

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
project_number = os.environ["GOOGLE_CLOUD_PROJECT_NUMBER"]
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


def test_live_session_operations(capsys: pytest.fixture) -> None:
    # Test setup

    slate_name = f"projects/{project_id}/locations/{location}/slates/{slate_id}"

    response = create_slate.create_slate(project_id, location, slate_id, slate_uri)
    assert slate_name in response.name

    live_config_name = (
        f"projects/{project_id}/locations/{location}/liveConfigs/{live_config_id}"
    )

    response = create_live_config.create_live_config(
        project_id, location, live_config_id, live_stream_uri, ad_tag_uri, slate_id
    )
    assert live_config_name in response.name

    # Tests

    response = create_live_session_response = create_live_session.create_live_session(
        project_id, location, live_config_id
    )
    session_name_prefix = (
        f"projects/{project_number}/locations/{location}/liveSessions/"
    )
    assert session_name_prefix in response.name

    str_slice = response.name.split("/")
    session_id = str_slice[len(str_slice) - 1].rstrip("\n")
    session_name = (
        f"projects/{project_number}/locations/{location}/liveSessions/{session_id}"
    )
    assert session_name in response.name

    response = get_live_session.get_live_session(project_id, location, session_id)
    assert session_name in response.name

    # No list or delete methods for live sessions

    # Ad tag details

    # To get ad tag details, you need to curl the main manifest and
    # a rendition first. This supplies media player information to the API.
    #
    # Curl the play_uri first. The last line of the response will contain a
    # renditions location. Curl the live session name with the rendition
    # location appended.

    r = requests.get(create_live_session_response.play_uri)
    match = re.search("renditions/.*", r.text)
    assert match
    renditions = match.group()
    assert "renditions/" in renditions

    # create_live_session_response.play_uri will be in the following format:
    # /projects/{project}/locations/{location}/liveSessions/{session-id}/manifest.m3u8?signature=...
    # Replace manifest.m3u8?signature=... with the renditions location.
    arr = create_live_session_response.play_uri.split("/")
    arr.pop()
    tmp = "/".join(arr)
    renditions_uri = f"{tmp}/{renditions}"
    r = requests.get(renditions_uri)

    list_live_ad_tag_details_response = (
        list_live_ad_tag_details.list_live_ad_tag_details(
            project_id, location, session_id
        )
    )
    out, _ = capsys.readouterr()
    ad_tag_details_name_prefix = f"projects/{project_number}/locations/{location}/liveSessions/{session_id}/liveAdTagDetails/"
    assert ad_tag_details_name_prefix in out

    str_slice = list_live_ad_tag_details_response.live_ad_tag_details[0].name.split("/")
    ad_tag_details_id = str_slice[len(str_slice) - 1].rstrip("\n")
    ad_tag_details_name = f"projects/{project_number}/locations/{location}/liveSessions/{session_id}/liveAdTagDetails/{ad_tag_details_id}"
    assert ad_tag_details_name in out

    # b/231626944 for projectNumber below
    response = get_live_ad_tag_detail.get_live_ad_tag_detail(
        project_number, location, session_id, ad_tag_details_id
    )
    assert ad_tag_details_name in response.name

    # Clean up live config and slate
    response = delete_live_config.delete_live_config(
        project_id, location, live_config_id
    )
    assert response == empty.Empty()

    response = delete_slate.delete_slate(project_id, location, slate_id)
    assert response == empty.Empty()
