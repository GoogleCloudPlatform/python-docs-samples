# Copyright 2020 Google LLC
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

from . import manage_transfer_configs


def test_update_credentials_with_service_account(
    capsys, project_id, service_account_name, transfer_config_name
):
    manage_transfer_configs.update_credentials_with_service_account(
        {
            "project_id": project_id,
            "service_account_name": service_account_name,
            "transfer_config_name": transfer_config_name,
        }
    )
    out, _ = capsys.readouterr()
    assert "Updated config:" in out
    assert transfer_config_name in out


def test_schedule_backfill_manual_transfer(capsys, transfer_config_name):
    runs = manage_transfer_configs.schedule_backfill_manual_transfer(
        {"transfer_config_name": transfer_config_name}
    )
    out, _ = capsys.readouterr()
    assert "Started manual transfer runs:" in out
    # Run IDs should include the transfer name in their path.
    assert transfer_config_name in out
    # Check that there are three runs for between 2 and 5 days ago.
    assert len(runs) == 3
