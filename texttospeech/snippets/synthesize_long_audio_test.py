#!/usr/bin/env python
# Copyright 2018 Google LLC
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
#
# All Rights Reserved.

import os

import synthesize_long_audio

def test_synthesize_text(capsys):
    response = synthesize_long_audio.synthesize_long_audio("projects/p0/locations/global", 
                                                           "hello",
                                                           "gs://bucket/output.wav")

