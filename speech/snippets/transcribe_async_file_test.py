# Copyright 2021 Google LLC

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

import os
import re

import transcribe_async_file

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


def test_transcribe(capsys):
    transcribe_async_file.transcribe_file(os.path.join(RESOURCES, "audio.raw"))
    out, err = capsys.readouterr()

    assert re.search(r"how old is the Brooklyn Bridge", out, re.DOTALL | re.I)
