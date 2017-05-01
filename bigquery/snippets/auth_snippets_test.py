# Copyright 2017 Google Inc.
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

import mock

import auth_snippets


def test_implicit():
    auth_snippets.implicit()


def test_explicit():
    with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as creds_file:
        creds_file_data = creds_file.read()

    open_mock = mock.mock_open(read_data=creds_file_data)

    with mock.patch('io.open', open_mock):
        auth_snippets.explicit()
