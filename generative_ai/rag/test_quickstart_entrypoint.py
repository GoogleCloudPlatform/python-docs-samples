# Copyright 2026 Google LLC
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

import ast
from pathlib import Path

SOURCE = Path(__file__).with_name("quickstart_example.py")


def _entrypoint_call() -> ast.Call:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "quickstart"
        ):
            return node
    raise AssertionError("quickstart entry point was not found")


def test_entrypoint_passes_gcs_path() -> None:
    calls = []

    def quickstart(display_name: str, gcs_path: str) -> None:
        calls.append((display_name, gcs_path))

    namespace = {
        "gcloud_path": "gs://your-bucket-name/file.txt",
        "quickstart": quickstart,
    }
    expression = ast.Expression(body=_entrypoint_call())
    ast.fix_missing_locations(expression)
    exec(compile(expression, str(SOURCE), "eval"), namespace)

    assert calls == [("test_corpus", "gs://your-bucket-name/file.txt")]
