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

"""Checks that the deprecated top-level samples match their package copies.

Docs pages embed the top-level files until they're updated to the package
paths. Delete this test with the top-level files.
"""

import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "src" / "workflows_samples"


def code_from_first_region(path: pathlib.Path) -> str:
    """Returns the file from its first region tag on, skipping the header."""
    text = path.read_text()
    return text[text.index("# [START") :]


@pytest.mark.parametrize(
    "filename", ["main.py", "execute_with_arguments.py", "execute_without_arguments.py"]
)
def test_deprecated_copy_matches_package(filename: str) -> None:
    assert code_from_first_region(ROOT / filename) == code_from_first_region(
        PACKAGE / filename
    )
