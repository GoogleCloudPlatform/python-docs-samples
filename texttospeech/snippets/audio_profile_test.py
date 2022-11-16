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

import os
import os.path

import audio_profile

TEXT = "hello"
OUTPUT = "output.mp3"
EFFECTS_PROFILE_ID = "telephony-class-application"


def test_audio_profile(capsys):
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
    assert not os.path.exists(OUTPUT)
    audio_profile.synthesize_text_with_audio_profile(TEXT, OUTPUT, EFFECTS_PROFILE_ID)
    out, err = capsys.readouterr()

    assert ('Audio content written to file "%s"' % OUTPUT) in out
    assert os.path.exists(OUTPUT)
    os.remove(OUTPUT)
