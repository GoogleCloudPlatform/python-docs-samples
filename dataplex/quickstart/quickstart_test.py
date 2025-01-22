# Copyright 2024 Google LLC
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
import os

import uuid

from google.api_core.exceptions import NotFound
from google.api_core.retry import Retry
from google.cloud import dataplex_v1

import pytest

import quickstart

ID = str(uuid.uuid4()).split("-")[0]
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
ASPECT_TYPE_ID = f"quickstart-aspect-type-{ID}"
ENTRY_TYPE_ID = f"quickstart-entry-type-{ID}"
ENTRY_GROUP_ID = f"quickstart-entry-group-{ID}"
ENTRY_ID = f"quickstart-entry-{ID}"


@Retry()
def test_quickstart(capsys: pytest.CaptureFixture) -> None:
    expected_logs = [
        f"Step 1: Created aspect type -> projects/{PROJECT_ID}/locations/global/aspectTypes/{ASPECT_TYPE_ID}",
        f"Step 2: Created entry type -> projects/{PROJECT_ID}/locations/global/entryTypes/{ENTRY_TYPE_ID}",
        (
            f"Step 3: Created entry group -> projects/{PROJECT_ID}/locations/{LOCATION}"
            f"/entryGroups/{ENTRY_GROUP_ID}"
        ),
        (
            f"Step 4: Created entry -> projects/{PROJECT_ID}/locations/{LOCATION}"
            f"/entryGroups/{ENTRY_GROUP_ID}/entries/{ENTRY_ID}"
        ),
        (
            f"Step 5: Retrieved entry -> projects/{PROJECT_ID}/locations/{LOCATION}"
            f"/entryGroups/{ENTRY_GROUP_ID}/entries/{ENTRY_ID}"
        ),
        # Step 6 - result from Search
        "Entries found in Search:",
        "Step 7: Successfully cleaned up resources",
    ]

    quickstart.quickstart(
        PROJECT_ID, LOCATION, ASPECT_TYPE_ID, ENTRY_TYPE_ID, ENTRY_GROUP_ID, ENTRY_ID
    )
    out, _ = capsys.readouterr()

    for expected_log in expected_logs:
        assert expected_log in out


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_aspect_type() -> None:
    # No set-up
    yield
    force_clean_resources()


def force_clean_resources() -> None:
    with dataplex_v1.CatalogServiceClient() as client:
        try:
            client.delete_entry_group(
                name=f"projects/{PROJECT_ID}/locations/{LOCATION}/entryGroups/{ENTRY_GROUP_ID}"
            )
        except NotFound:
            pass  # no resource to delete
        try:
            client.delete_entry_type(
                name=f"projects/{PROJECT_ID}/locations/global/entryTypes/{ENTRY_TYPE_ID}"
            )
        except NotFound:
            pass  # no resource to delete
        try:
            client.delete_aspect_type(
                name=f"projects/{PROJECT_ID}/locations/global/aspectTypes/{ASPECT_TYPE_ID}"
            )
        except NotFound:
            pass  # no resource to delete
