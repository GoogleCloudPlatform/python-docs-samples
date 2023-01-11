# Copyright 2023 Google LLC
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

from __future__ import annotations

# The conftest contains a bunch of reusable fixtures used all over the place.
# If we use a fixture not defined here, it must be on the conftest!
#   https://docs.pytest.org/en/latest/explanation/fixtures.html
import conftest  # python-docs-samples/people-and-planet-ai/conftest.py

import pytest

# ---------- FIXTURES ---------- #


# Many fixtures expect a fixture called `test_name`, so be sure to define it!
@pytest.fixture(scope="session")
def test_name(python_version: str) -> str:
    return f"ppai/weather-py{python_version}"


def test_predictions() -> None:
    raise RuntimeError("TODO: test_predictions")
