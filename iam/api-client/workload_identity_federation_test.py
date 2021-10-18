#  Copyright 2021 Google LLC
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import re

from _pytest.capture import CaptureFixture

import workload_identity_federation


def test_workload_identity_federation_aws(capsys: CaptureFixture) -> None:
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    # Replace the below variables with your AWS EC2 credentials.
    aws_access_key_id = "AKIA000000000EXAMPLE"
    aws_secret_access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    workload_identity_federation.create_token_aws(project_id, "provider_id", "pool_id", aws_access_key_id,
                                                  aws_secret_access_key)
    out, _ = capsys.readouterr()
    assert re.search("URL encoded token:", out)
