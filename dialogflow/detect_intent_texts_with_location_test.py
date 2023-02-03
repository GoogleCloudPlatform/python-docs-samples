# Copyright 2017, Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import os
import uuid

from detect_intent_texts_with_location import detect_intent_texts_with_location

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = "europe-west2"
SESSION_ID = "test_{}".format(uuid.uuid4())
TEXTS = [
    "hello",
    "book a meeting room",
    "Mountain View",
    "tomorrow",
    "10 AM",
    "2 hours",
    "10 people",
    "A",
    "yes",
]


def test_detect_intent_texts_with_location(capsys):
    detect_intent_texts_with_location(
        PROJECT_ID, LOCATION_ID, SESSION_ID, TEXTS, "en-GB"
    )
    out, _ = capsys.readouterr()

    assert "Fulfillment text: All set!" in out
