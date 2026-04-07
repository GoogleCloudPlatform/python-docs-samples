# Copyright 2026 Google LLC
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

import bigframes.pandas as bpd

import call_python_udf


def test_call_python_udf(project_id: str, location: str) -> None:
    bpd.close_session()
    pd_result, bf_result = call_python_udf.call_python_udf(project_id=project_id, location=location)
    assert len(pd_result.index) == 3
    assert len(bf_result.index) == 3
