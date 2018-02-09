# Copyright 2017, Google, Inc.
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

import transcribe_with_metadata

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


def test_transcribe_file_original_media_type_video(capsys):
    transcribe_with_metadata.transcribe_file_with_metadata(
        os.path.join(RESOURCES, 'Google_Gnome.wav'))
    out, _ = capsys.readouterr()

    assert 'you do keep doing that' in out
    assert 'organic matter and will return' in out


def test_transcribe_gcs_original_media_type_video(capsys):
    transcribe_with_metadata.transcribe_gcs_with_metadata(
        'gs://python-docs-samples-tests/speech/Google_Gnome.wav')
    out, _ = capsys.readouterr()

    assert 'you do keep doing that' in out
    assert 'organic matter and will return' in out
