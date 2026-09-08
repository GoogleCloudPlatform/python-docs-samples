# Copyright 2026 Google LLC
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

import os
import shutil
import tempfile
import unittest
from unittest import mock

try:
    import pytest
except ImportError:
    pytest = None

from .terraform_apply_operator import TerraformApplyOperator


class TestTerraformApplyOperator(unittest.TestCase):

    def test_operator_initialization(self):
        operator = TerraformApplyOperator(
            task_id="test_tf_task",
            terraform_dir="/tmp/test_dir",
            variables={"project_id": "test-project"},
            terraform_version="1.5.7",
            auto_approve=True,
        )
        self.assertEqual(operator.task_id, "test_tf_task")
        self.assertEqual(operator.terraform_dir, "/tmp/test_dir")
        self.assertEqual(operator.variables, {"project_id": "test-project"})
        self.assertEqual(operator.terraform_version, "1.5.7")
        self.assertTrue(operator.auto_approve)

    def test_stage_workspace_nonexistent_dir(self):
        operator = TerraformApplyOperator(
            task_id="test_tf_task",
            terraform_dir="/nonexistent/path/to/tf",
        )
        with self.assertRaises(FileNotFoundError):
            operator._stage_workspace()

    def test_stage_workspace_success(self):
        with tempfile.TemporaryDirectory() as src_dir:
            test_file = os.path.join(src_dir, "main.tf")
            with open(test_file, "w") as f:
                f.write("# terraform config")

            operator = TerraformApplyOperator(
                task_id="test_stage",
                terraform_dir=src_dir,
            )
            work_dir = operator._stage_workspace()
            try:
                self.assertTrue(os.path.exists(os.path.join(work_dir, "main.tf")))
            finally:
                shutil.rmtree(work_dir, ignore_errors=True)

    def test_custom_binary_path(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"mock binary")
            binary_file = f.name

        try:
            os.chmod(binary_file, 0o755)
            operator = TerraformApplyOperator(
                task_id="test_binary",
                terraform_dir="/tmp/test",
                binary_path=binary_file,
            )
            self.assertEqual(operator._ensure_terraform_binary(), binary_file)
        finally:
            if os.path.exists(binary_file):
                os.remove(binary_file)

    @mock.patch("shutil.which", return_value="/usr/local/bin/terraform")
    def test_path_binary_detection(self, mock_which):
        operator = TerraformApplyOperator(
            task_id="test_path",
            terraform_dir="/tmp/test",
        )
        self.assertEqual(operator._ensure_terraform_binary(), "/usr/local/bin/terraform")

    def test_sha256_verification_success_and_failure(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"sample data content")
            sample_file = f.name

        operator = TerraformApplyOperator(
            task_id="test_hash",
            terraform_dir="/tmp/test",
        )
        try:
            # Correct SHA-256 for "sample data content"
            correct_hash = "4a922a0548a2e7d67bbff25c9bc4ea16b08eab6f314d8df525e2f6cef1334166"
            operator._verify_sha256(sample_file, correct_hash)

            # Incorrect SHA-256 should raise ValueError
            with self.assertRaises(ValueError):
                operator._verify_sha256(sample_file, "deadbeef123456")
        finally:
            if os.path.exists(sample_file):
                os.remove(sample_file)

    @mock.patch.object(TerraformApplyOperator, "_ensure_terraform_binary", return_value="/tmp/mock_terraform")
    @mock.patch.object(TerraformApplyOperator, "_stage_workspace", return_value="/tmp/mock_workdir")
    @mock.patch.object(TerraformApplyOperator, "_run_command")
    @mock.patch("shutil.rmtree")
    @mock.patch("os.path.exists", return_value=True)
    def test_operator_execute_flow(self, mock_exists, mock_rmtree, mock_run_command, mock_stage, mock_binary):
        operator = TerraformApplyOperator(
            task_id="test_exec",
            terraform_dir="/tmp/sample",
            variables={"region": "us-central1"},
            auto_approve=True,
        )

        result = operator.execute(context={})

        self.assertIn("Terraform apply executed successfully", result)
        self.assertEqual(mock_run_command.call_count, 2)
        # Verify init was called
        mock_run_command.assert_any_call(["/tmp/mock_terraform", "init"], cwd="/tmp/mock_workdir")
        # Verify apply was called with arguments
        mock_run_command.assert_any_call(
            ["/tmp/mock_terraform", "apply", "-auto-approve", "-var", "region=us-central1"],
            cwd="/tmp/mock_workdir",
        )
        # Verify workspace cleanup occurred
        mock_rmtree.assert_called_once_with("/tmp/mock_workdir", ignore_errors=True)


if __name__ == "__main__":
    unittest.main()


