# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from unittest import mock
from unittest.mock import MagicMock

import uuid

import pytest

import stored_infotype

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
TEST_BUCKET_NAME = GCLOUD_PROJECT + "-dlp-python-client-test" + UNIQUE_STRING
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
RESOURCE_FILE_NAMES = ["term_list.txt"]
STORED_INFO_TYPE_ID = "github-usernames" + UNIQUE_STRING


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_create_stored_infotype(
    dlp_client: MagicMock, capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value

    # Configure the mock CreateStoredInfoType DLP method and its behavior.
    mock_dlp_instance.create_stored_info_type.return_value.name = (
        f"projects/{GCLOUD_PROJECT}/storedInfoTypes/{STORED_INFO_TYPE_ID}"
    )

    stored_infotype.create_stored_infotype(
        GCLOUD_PROJECT,
        STORED_INFO_TYPE_ID,
        TEST_BUCKET_NAME,
    )

    out, _ = capsys.readouterr()
    assert STORED_INFO_TYPE_ID in out


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_update_stored_infotype_dictionary(
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value

    # Configure the mock UpdateStoredInfoType DLP method and its behavior.
    stored_infotype_path = f"projects/{GCLOUD_PROJECT}/storedInfoTypes/{STORED_INFO_TYPE_ID}"
    mock_dlp_instance.update_stored_info_type.return_value.name = stored_infotype_path

    test_updated_list_path = f"{TEST_BUCKET_NAME}/{RESOURCE_FILE_NAMES[0]}"

    stored_infotype.update_stored_infotype(
        GCLOUD_PROJECT,
        STORED_INFO_TYPE_ID,
        test_updated_list_path,
        TEST_BUCKET_NAME,
    )

    out, _ = capsys.readouterr()
    assert stored_infotype_path in out


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_with_stored_infotype(
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value

    # Configure the mock InspectContent DLP method and its behavior.
    mock_inspect_result = mock_dlp_instance.inspect_content.return_value

    mock_inspect_result.result.findings.info_type.name = "STORED_TYPE"
    finding = mock_inspect_result.result.findings.info_type

    mock_inspect_result.result.findings = [
        MagicMock(info_type=finding, quote="gary1998", likelihood='LIKELY'),
    ]

    # Call the sample.
    stored_infotype.inspect_with_stored_infotype(
        GCLOUD_PROJECT,
        STORED_INFO_TYPE_ID,
        "The commit was made by gary1998",
    )

    out, _ = capsys.readouterr()
    assert "STORED_TYPE" in out
    assert "Quote: gary1998" in out
