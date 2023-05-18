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

import os

import pytest

import grantable_roles


def test_grantable_roles(capsys: pytest.CaptureFixture) -> None:
    project = os.environ['GOOGLE_CLOUD_PROJECT']
    resource = '//cloudresourcemanager.googleapis.com/projects/' + project
    grantable_roles.view_grantable_roles(resource)
    out, _ = capsys.readouterr()
    assert 'Title:' in out
