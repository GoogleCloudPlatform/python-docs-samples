#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.auth

import list_training_phrases

_, PROJECT_ID = google.auth.default()
INTENT_ID = "7b5bd47e-6dd9-4b45-8624-565862bd2d85"


def test_list_training_phrases(capsys):
    training_phrases = list_training_phrases.list_training_phrases(
        PROJECT_ID,
        INTENT_ID,
    )
    assert len(training_phrases) >= 9  # Number of training phrases at this point.
