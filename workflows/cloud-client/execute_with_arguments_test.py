# Copyright 2025 Google LLC
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

import backoff

from google.cloud.workflows.executions_v1.types import executions

import execute_with_arguments


@backoff.on_exception(backoff.expo, AssertionError, max_tries=5)
def test_workflow_execution_with_arguments(
    project_id: str, location: str, workflow_id: str
) -> None:
    execution_result = execute_with_arguments.execute_workflow_with_arguments(
        project_id, location, workflow_id
    )
    assert execution_result.state == executions.Execution.State.SUCCEEDED
    assert "searchTerm" in execution_result.argument
    assert "Cloud" in execution_result.result
