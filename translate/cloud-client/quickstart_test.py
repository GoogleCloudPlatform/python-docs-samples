# -*- coding: utf-8 -*-
# Copyright 2016 Google Inc. All Rights Reserved.
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

from google.cloud import translate
import mock
import pytest

import quickstart


@pytest.fixture
def mock_client(cloud_config):
    original_client_ctor = translate.Client

    def new_client_ctor(api_key):
        # Strip api_key argument and replace with our api key.
        return original_client_ctor(cloud_config.api_key)

    with mock.patch(
            'google.cloud.translate.Client',
            side_effect=new_client_ctor):
        yield


def test_quickstart(mock_client, capsys):
    quickstart.run_quickstart()
    out, _ = capsys.readouterr()
    assert u'Привет мир!' in out
