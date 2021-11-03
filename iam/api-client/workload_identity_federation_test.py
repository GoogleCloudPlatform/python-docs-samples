#  Copyright 2021 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re

from _pytest.capture import CaptureFixture

import workload_identity_federation


def test_workload_identity_federation_aws(capsys: CaptureFixture) -> None:
    import google.auth
    credentials, project_id = google.auth.default()
    workload_identity_federation.create_token_aws(project_id, "provider_id", "pool_id")
    out, _ = capsys.readouterr()
    assert re.search("URL encoded token:", out)
