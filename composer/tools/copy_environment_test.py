# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import time

from google.cloud import storage
import mock
import pytest


def test_grant_rw_permissions_fails_gracefully(monkeypatch, capsys):
    mock_call = mock.Mock()
    mock_call.side_effect = RuntimeError()
    monkeypatch.setattr(subprocess, 'call', mock_call)
    monkeypatch.setattr(time, 'sleep', lambda sec: None)
    from . import copy_environment

    with pytest.raises(SystemExit):
        copy_environment.grant_rw_permissions(
            storage.Bucket(None, name='example-bucket'),
            'serviceaccount@example.com')

    out, _ = capsys.readouterr()
    assert 'Failed to set acls for service account' in out
