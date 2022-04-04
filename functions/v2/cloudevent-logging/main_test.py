# Copyright 2022 Google LLC
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

    # Build a CloudEvent log entry
    attributes = {
        "id": "0",
        "subject": "test subject",
        "type": "google.cloud.pubsub.topic.v1.messagePublished",
        "source": "//pubsub.googleapis.com/projects/example/topics/test-topic",
        "data": "{'message': 'hello'}"
    }

    data = {
        "protoPayload": {
            "methodName": "storage.objects.create",
            "authenticationInfo": {"principalEmail": "nobody@example.com"},
            "resourceName": "some-resource",
        }
    }

    event = CloudEvent(attributes, data)

    main.structured_logging_event(event)

    out, _ = capsys.readouterr()

    assert "Wrote logs to New-Structured-Log" in out
