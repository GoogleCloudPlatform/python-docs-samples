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

from unittest.mock import patch

from cloudevents.http import CloudEvent
from google.events.cloud import firestore as firestoredata

import main


def make_event(string_value, collection_id, document_path):
    firestore_payload = firestoredata.DocumentEventData()
    firestore_payload.value = firestoredata.Document()
    firestore_payload.value.name = f"/projects/test-project/databases/(default)/documents/{collection_id}/{document_path}"
    field_value = firestoredata.Value()
    field_value.string_value = string_value
    firestore_payload.value.fields = {"original": field_value}

    attributes = {
        "id": "5e9f24a",
        "type": "google.cloud.firestore.document.v1.written",
        "source": "/projects/test-project/databases/(default)",
    }
    data = firestore_payload._pb.SerializeToString()
    cloud_event = CloudEvent(attributes, data)

    return cloud_event


def test_make_upper_case(capsys):
    with patch("main.client"):
        event = make_event("foo", "test-collection", "test-doc")

        main.make_upper_case(event)

        out, _ = capsys.readouterr()
        assert "Collection path: test-collection" in out
        assert "Document path: test-doc" in out
        assert "Replacing value: foo --> FOO" in out


def test_make_upper_case_skips_if_upper(capsys):
    with patch("main.client"):
        event = make_event("FOO", "foods", "tacos/vegan")

        main.make_upper_case(event)

        out, _ = capsys.readouterr()
        assert "Collection path: foods" in out
        assert "Document path: tacos/vegan" in out
        assert "Value is already upper-case." in out
