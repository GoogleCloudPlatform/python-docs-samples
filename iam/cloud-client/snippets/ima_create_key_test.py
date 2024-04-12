# # Copyright 2022 Google LLC
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# import os
# import re

# import pytest
# from snippets.iam_create_key import iam_create_key

# PROJECT_ID = os.environ["IAM_PROJECT_ID"]


# def test_retrieve_policy(
#     capsys: "pytest.CaptureFixture[str]", deny_policy: str
# ) -> None:
#     # Test policy retrieval, given the policy id.
#     iam_create_key(PROJECT_ID, deny_policy)
#     out, _ = capsys.readouterr()
#     assert re.search(f"Retrieved the deny policy: {deny_policy}", out)
