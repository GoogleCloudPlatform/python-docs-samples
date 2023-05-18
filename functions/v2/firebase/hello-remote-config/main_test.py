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

from cloudevents.http import CloudEvent

import main


def test_hello_remote_config(capsys):
    attributes = {
        "id": "5e9f24a",
        "type": "google.firebase.remoteconfig.remoteConfig.v1.updated",
        "source": "this is a test source",
    }

    data = {"updateType": "INCREMENTAL", "updateOrigin": "CONSOLE", "versionNumber": 2}
    cloud_event = CloudEvent(attributes, data)

    # Calling the function with the mocked cloud event
    main.hello_remote_config(cloud_event)

    out, _ = capsys.readouterr()

    assert f"Update type: {data['updateType']}" in out
    assert f"Origin: {data['updateOrigin']}" in out
    assert f"Version: {data['versionNumber']}" in out
