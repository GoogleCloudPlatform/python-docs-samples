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
#
import google.auth
from google.cloud import contact_center_insights_v1
from google.protobuf import field_mask_pb2
import pytest

import set_project_ttl


@pytest.fixture
def project_id():
    _, project_id = google.auth.default()
    return project_id


@pytest.fixture
def clear_project_ttl(project_id):
    yield
    settings = contact_center_insights_v1.Settings()
    settings.name = (
        contact_center_insights_v1.ContactCenterInsightsClient.settings_path(
            project_id, "us-central1"
        )
    )
    settings.conversation_ttl = None
    update_mask = field_mask_pb2.FieldMask()
    update_mask.paths.append("conversation_ttl")

    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    insights_client.update_settings(settings=settings, update_mask=update_mask)


def test_set_project_ttl(capsys, project_id, clear_project_ttl):
    set_project_ttl.set_project_ttl(project_id)
    out, err = capsys.readouterr()
    assert "Set TTL for all incoming conversations to 1 day" in out
