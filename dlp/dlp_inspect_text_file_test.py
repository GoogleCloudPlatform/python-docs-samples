# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import subprocess
import sys


def test_inspect_text_file():
    base_filepath = os.path.dirname(__file__)
    snippet_filepath = os.path.join(base_filepath, 'dlp_inspect_text_file.py')
    resource_filepath = os.path.join(base_filepath, 'resources', 'test.txt')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

    out = subprocess.check_output(
        [sys.executable, snippet_filepath, project_id, resource_filepath])

    assert 'Info type: PHONE_NUMBER' in str(out)
    assert 'Info type: EMAIL_ADDRESS' in str(out)
