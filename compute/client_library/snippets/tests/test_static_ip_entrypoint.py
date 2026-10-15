#  Copyright 2026 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import ast
from pathlib import Path

ROOT = Path(__file__).parents[2]
SOURCES = (
    ROOT / "recipes/instances/ip_address/assign_static_external_ip_to_new_vm.py",
    ROOT / "snippets/instances/ip_address/assign_static_external_ip_to_new_vm.py",
)


def _entrypoint_call(source: Path) -> ast.Call:
    tree = ast.parse(source.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "assign_static_external_ip_to_new_vm"
        ):
            return node
    raise AssertionError(f"entry point was not found in {source}")


def test_static_ip_entrypoints_pass_ip_address() -> None:
    for source in SOURCES:
        calls = []

        def assign_static_external_ip_to_new_vm(
            project_id: str, zone: str, instance_name: str, ip_address: str
        ) -> None:
            calls.append((project_id, zone, instance_name, ip_address))

        namespace = {
            "PROJECT": "project",
            "ZONE": "us-central1-a",
            "instance_name": "instance",
            "ip_address": "203.0.113.10",
            "assign_static_external_ip_to_new_vm": assign_static_external_ip_to_new_vm,
        }
        expression = ast.Expression(body=_entrypoint_call(source))
        ast.fix_missing_locations(expression)
        exec(compile(expression, str(source), "eval"), namespace)

        assert calls == [("project", "us-central1-a", "instance", "203.0.113.10")]
