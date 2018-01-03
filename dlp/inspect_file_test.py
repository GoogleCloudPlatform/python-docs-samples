# Copyright 2017 Google Inc.
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

import os

import inspect_file


def test_inspect_file(capsys):
    test_filepath = os.path.join(
        os.path.dirname(__file__), 'resources/test.txt')

    inspect_file.inspect_file(
        test_filepath, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_file_with_info_types(capsys):
    test_filepath = os.path.join(
        os.path.dirname(__file__), 'resources/test.txt')

    inspect_file.inspect_file(
        test_filepath, ['PHONE_NUMBER'], include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: PHONE_NUMBER' in out
    assert 'Info type: EMAIL_ADDRESS' not in out


def test_inspect_file_no_results(capsys):
    test_filepath = os.path.join(
        os.path.dirname(__file__), 'resources/harmless.txt')

    inspect_file.inspect_file(
        test_filepath, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'No findings' in out


def test_inspect_image_file(capsys):
    test_filepath = os.path.join(
        os.path.dirname(__file__), 'resources/test.png')

    inspect_file.inspect_file(
        test_filepath, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: PHONE_NUMBER' in out
