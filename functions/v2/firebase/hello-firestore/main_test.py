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
from google.events.cloud import firestore

import main


def test_hello_firestore(capsys):
    old_document = firestore.Document(
        name="/projects/test-project/databases/(default)/documents/test-collection/test-doc",
        fields={"name": firestore.Value(string_value="Test Name")},
    )
    new_document = firestore.Document(
        name="/projects/test-project/databases/(default)/documents/test-collection/test-doc",
        fields={"name": firestore.Value(string_value="New Test Name")},
    )

    firestore_payload = firestore.DocumentEventData(
        old_value=old_document,
        value=new_document,
    )

    attributes = {
        "id": "5e9f24a",
        "type": "google.cloud.firestore.document.v1.written",
        "source": "/projects/test-project/databases/(default)/documents/test-collection/test-doc",
    }

    data = firestore_payload._pb.SerializeToString()

    cloud_event = CloudEvent(attributes, data)

    # Calling the function with the mocked cloud event
    main.hello_firestore(cloud_event)

    out, _ = capsys.readouterr()

    assert "\nOld value:" in out
    assert firestore_payload.old_value.__str__() in out
    assert "\nNew value:" in out
    assert firestore_payload.value.__str__() in out
