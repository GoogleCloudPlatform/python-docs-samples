# Copyright 2018, Google, Inc.
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

import synthesize_text

TEXT = 'Hello there.'
SSML = """<?xml version="1.0"?>
 <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.w3.org/2001/10/synthesis
 http://www.w3.org/TR/speech-synthesis/synthesis.xsd" xml:lang="en-US">
 Hello there.
 </speak>
"""


def test_synthesize_text(capsys):
    synthesize_text.synthesize_text(text=TEXT)
    out, err = capsys.readouterr()

    assert 'Audio content written to file' in out


def test_synthesize_ssml(capsys):
    synthesize_text.synthesize_ssml(ssml=SSML)
    out, err = capsys.readouterr()

    assert 'Audio content written to file' in out
