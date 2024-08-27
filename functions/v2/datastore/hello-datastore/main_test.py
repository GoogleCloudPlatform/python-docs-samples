# Copyright 2024 Google LLC
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
from google.events.cloud import datastore

import main


def test_hello_datastore(capsys):
    old_entity = datastore.EntityResult(
        entity=datastore.Entity(
            properties={"name": datastore.Value(string_value="Old Test Name")}
        ),
    )
    new_entity = datastore.EntityResult(
        entity=datastore.Entity(
            properties={"name": datastore.Value(string_value="New Test Name")}
        ),
    )

    datastore_payload = datastore.EntityEventData(
        old_value=old_entity,
        value=new_entity,
    )

    attributes = {
        "id": "5e9f24a",
        "type": "google.cloud.datastore.entity.v1.written",
        "source": "/projects/test-project/databases/(default)/documents/test-kind/test-entity",
    }

    data = datastore_payload._pb.SerializeToString()

    cloud_event = CloudEvent(attributes, data)

    # Calling the function with the mocked cloud event
    main.hello_datastore(cloud_event)

    out, _ = capsys.readouterr()

    assert "\nOld value:" in out
    assert datastore_payload.old_value.__str__() in out
    assert "\nNew value:" in out
    assert datastore_payload.value.__str__() in out
