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

import google.auth

import simple_app


def test_query_stackoverflow(capsys):
    credentials, project_id = google.auth.default(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    simple_app.query_stackoverflow(credentials, project_id)
    out, _ = capsys.readouterr()
    assert 'stackoverflow.com' in out
