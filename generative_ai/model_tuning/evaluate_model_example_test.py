# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import backoff

from google.api_core.exceptions import ResourceExhausted

import pytest

import evaluate_model_example


@pytest.mark.skip(
    reason="Model is giving 404 Not found error."
    "Need to investigate. Created an issue tracker is at "
    "python-docs-samples/issues/11264"
)
@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_evaluate_model() -> None:
    eval_metrics = evaluate_model_example.evaluate_model()
    assert hasattr(eval_metrics, "auRoc")
