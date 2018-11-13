# Copyright 2018 Google LLC
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

import access


def test_access(capsys):
    project = os.environ['GCLOUD_PROJECT']

    policy = access.get_policy(project)
    out, _ = capsys.readouterr()
    assert 'etag' in out

    policy = access.set_policy(project, policy)
    out, _ = capsys.readouterr()
    assert 'etag' in out
