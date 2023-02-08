#!/usr/bin/env python

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.auth

import list_training_phrases


_, PROJECT_ID = google.auth.default()
INTENT_ID = os.getenv("INTENT_ID")
LOCATION = "global"
AGENT_ID = os.getenv("AGENT_ID")


def test_list_training_phrases(capsys):
    training_phrases = list_training_phrases.list_training_phrases(
        PROJECT_ID, AGENT_ID, INTENT_ID, LOCATION
    )
    assert len(training_phrases) >= 15  # Number of training phrases at this point.
