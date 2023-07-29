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

from . import run_notification


def test_run_notification(capsys, transfer_config_name, pubsub_topic):
    run_notification.run_notification(
        transfer_config_name=transfer_config_name,
        pubsub_topic=pubsub_topic,
    )
    out, _ = capsys.readouterr()
    assert "Updated config:" in out
    assert transfer_config_name in out
    assert "Notification Pub/Sub topic:" in out
    assert pubsub_topic in out
