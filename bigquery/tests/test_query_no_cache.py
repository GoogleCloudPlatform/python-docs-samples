# Copyright 2019 Google LLC
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

import re
import typing

from .. import query_no_cache

if typing.TYPE_CHECKING:
    import pytest


def test_query_no_cache(capsys: "pytest.CaptureFixture[str]") -> None:

    query_no_cache.query_no_cache()
    out, err = capsys.readouterr()
    assert re.search(r"(Row[\w(){}:', ]+)$", out)
