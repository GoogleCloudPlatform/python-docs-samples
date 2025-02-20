# Copyright 2025 Google LLC
#
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

import gcloud_commands
import pytest

test_proposal_resource = """projects/hawksbill-playground/locations/\
us-east1/singleTenantHsmInstances/my_sth
  """

# def test_build_custom():
#     process = gcloud_commands.build_custom_gcloud()
#     assert not process.stderr

# def test_fetch_challenges():
#     process = gcloud_commands.fetch_challenges(test_proposal_resource)
#     # assert not process.stderr

# def test_send_signed_challenges():
#     process = gcloud_commands.send_signed_challenges()
#     # assert not process.stderr

