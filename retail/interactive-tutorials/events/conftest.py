# Copyright 2022 Google LLC
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

import pytest
import test_utils.prefixer

prefixer = test_utils.prefixer.Prefixer(
    "python-docs-samples", "retail/interactive-tutorials/product"
)


@pytest.fixture(scope="session")
def table_id_prefix() -> str:
    return prefixer.create_prefix()


@pytest.fixture(scope="session")
def bucket_name_prefix() -> str:
    return prefixer.create_prefix()
