# Copyright 2021 Google LLC
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


def test_functions_log_cloudevent_should_print_message(capsys):

    attributes = {
        "source": "test",
        "type": "google.cloud.audit.log.v1.written",
        "subject": "storage.googleapis.com/projects/_/buckets/my-bucket/objects/test.txt",
    }

    data = {
        "protoPayload": {
            "methodName": "storage.objects.create",
            "authenticationInfo": {"principalEmail": "nobody@example.com"},
            "resourceName": "some-resource",
        }
    }

    event = CloudEvent(attributes, data)

    main.hello_auditlog(event)

    out, _ = capsys.readouterr()
    assert "Event type: google.cloud.audit.log.v1.written" in out
    assert (
        "Subject: storage.googleapis.com/projects/_/buckets/my-bucket/objects/test.txt"
        in out
    )
    assert "API method: storage.objects.create" in out
    assert "Resource name: some-resource" in out
    assert "Principal: nobody@example.com" in out
