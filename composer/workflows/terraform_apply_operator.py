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

"""Custom Airflow Operator for executing Terraform in Google Cloud Composer environments."""

# [START composer_terraform_apply_operator]

import hashlib
import logging
import os
import platform
import shutil
import subprocess
import tempfile
from typing import Any, Dict, Optional, Sequence
import urllib.request
import zipfile

try:
    from airflow.models import BaseOperator
except ImportError:
    class BaseOperator:
        """Fallback BaseOperator when Airflow is not installed in local environment."""

        def __init__(self, **kwargs):
            self.task_id = kwargs.get("task_id", "local_terraform_task")
            self.log = logging.getLogger(self.__class__.__name__)


class TerraformApplyOperator(BaseOperator):
    """Airflow Operator to execute `terraform apply` within Google Cloud Composer workers.

    Key Features:
    - Supports pre-installed Terraform binaries or dynamic download with cryptographic SHA-256 verification.
    - Staging `.tf` files from GCSFuse mount paths to local pod `/tmp/` disk storage to avoid GCSFuse file-locking errors.
    - Streaming real-time `terraform init` and `terraform apply` logs to Airflow task logs.
    - Automatic cleanup of temporary workspace directories upon task completion.

    Security & Reliability Considerations:
    - Pre-installing Terraform or providing `binary_path` is recommended for Private IP Composer environments.
    - If dynamically downloading from HashiCorp releases, official SHA-256 checksum verification is enforced.
    """

    template_fields: Sequence[str] = ("terraform_dir", "variables", "terraform_version")

    def __init__(
        self,
        *,
        terraform_dir: str,
        variables: Optional[Dict[str, Any]] = None,
        terraform_version: str = "1.5.7",
        binary_path: Optional[str] = None,
        auto_approve: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.terraform_dir = terraform_dir
        self.variables = variables or {}
        self.terraform_version = terraform_version
        self.binary_path = binary_path
        self.auto_approve = auto_approve

    def _fetch_expected_checksum(self, version: str, filename: str) -> Optional[str]:
        """Downloads the official HashiCorp SHA256SUMS file and extracts the expected hash for filename."""
        sums_url = f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_SHA256SUMS"
        self.log.info("Fetching SHA256 checksums from %s", sums_url)
        with urllib.request.urlopen(sums_url) as response:
            content = response.read().decode("utf-8")

        for line in content.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1].endswith(filename):
                return parts[0]
        return None

    def _verify_sha256(self, file_path: str, expected_checksum: str) -> None:
        """Verifies that the SHA-256 digest of file_path matches expected_checksum."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        calculated_checksum = sha256_hash.hexdigest()

        if calculated_checksum.lower() != expected_checksum.lower():
            raise ValueError(
                f"SHA256 checksum verification failed for {file_path}! "
                f"Expected: {expected_checksum}, Got: {calculated_checksum}"
            )
        self.log.info("SHA256 checksum verified successfully (%s)", calculated_checksum)

    def _ensure_terraform_binary(self) -> str:
        """Finds or bootstraps the terraform executable.

        1. Uses `self.binary_path` if explicitly specified.
        2. Checks system PATH for pre-installed `terraform`.
        3. If unavailable, downloads and extracts the verified binary into `/tmp/`.
        """
        # 1. Check custom binary path
        if self.binary_path:
            if os.path.exists(self.binary_path) and os.access(self.binary_path, os.X_OK):
                self.log.info("Using specified Terraform binary at %s", self.binary_path)
                return self.binary_path
            raise FileNotFoundError(f"Specified binary_path not found or executable: {self.binary_path}")

        # 2. Check system PATH (pre-installed in custom worker images)
        path_binary = shutil.which("terraform")
        if path_binary:
            self.log.info("Using system Terraform binary found in PATH at %s", path_binary)
            return path_binary

        # 3. Dynamic download with SHA-256 verification
        bin_dir = f"/tmp/terraform_bin_{self.terraform_version}"
        binary_path = os.path.join(bin_dir, "terraform")

        if os.path.exists(binary_path) and os.access(binary_path, os.X_OK):
            self.log.info("Found cached Terraform binary at %s", binary_path)
            return binary_path

        os.makedirs(bin_dir, exist_ok=True)

        arch = platform.machine()
        if arch in ("x86_64", "AMD64"):
            platform_arch = "linux_amd64"
        elif arch in ("aarch64", "arm64"):
            platform_arch = "linux_arm64"
        else:
            platform_arch = "linux_amd64"

        zip_filename = f"terraform_{self.terraform_version}_{platform_arch}.zip"
        url = f"https://releases.hashicorp.com/terraform/{self.terraform_version}/{zip_filename}"
        zip_path = os.path.join(bin_dir, zip_filename)

        self.log.info("Downloading Terraform v%s from %s", self.terraform_version, url)
        urllib.request.urlretrieve(url, zip_path)

        expected_checksum = self._fetch_expected_checksum(self.terraform_version, zip_filename)
        if expected_checksum:
            self._verify_sha256(zip_path, expected_checksum)
        else:
            self.log.warning("Could not find official checksum for %s in SHA256SUMS file", zip_filename)

        self.log.info("Extracting Terraform binary to %s", bin_dir)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(bin_dir)

        if os.path.exists(zip_path):
            os.remove(zip_path)

        os.chmod(binary_path, 0o755)
        self.log.info("Terraform binary successfully bootstrapped at %s", binary_path)
        return binary_path

    def _stage_workspace(self) -> str:
        """Copies Terraform configuration files from GCSFuse mount directory

        to an isolated local temporary working directory.
        """
        work_dir = tempfile.mkdtemp(prefix=f"tf_workdir_{self.task_id}_")
        self.log.info(
            "Staging Terraform configuration from %s to local workspace %s",
            self.terraform_dir,
            work_dir,
        )

        if not os.path.exists(self.terraform_dir):
            raise FileNotFoundError(
                f"Specified terraform_dir does not exist: {self.terraform_dir}"
            )

        shutil.copytree(self.terraform_dir, work_dir, dirs_exist_ok=True)
        return work_dir

    def _run_command(self, command: list, cwd: str) -> None:
        """Executes a command subprocess and streams output line-by-line to Airflow logs."""
        self.log.info("Executing command: %s (in %s)", " ".join(command), cwd)
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                self.log.info(line.rstrip())
            process.stdout.close()

        return_code = process.wait()
        if return_code != 0:
            raise RuntimeError(
                f"Command '{' '.join(command)}' failed with exit code {return_code}"
            )

    def execute(self, context: Any) -> str:
        """Airflow task execution lifecycle entry point."""
        work_dir = None
        try:
            tf_binary = self._ensure_terraform_binary()
            work_dir = self._stage_workspace()

            # 1. Initialize Terraform
            self._run_command([tf_binary, "init"], cwd=work_dir)

            # 2. Build Terraform Apply command
            apply_cmd = [tf_binary, "apply"]
            if self.auto_approve:
                apply_cmd.append("-auto-approve")

            if self.variables:
                for key, val in self.variables.items():
                    apply_cmd.extend(["-var", f"{key}={val}"])

            # 3. Execute Apply
            self._run_command(apply_cmd, cwd=work_dir)

            return f"Terraform apply executed successfully in {work_dir}"

        finally:
            if work_dir and os.path.exists(work_dir):
                self.log.info("Cleaning up temporary workspace at %s", work_dir)
                shutil.rmtree(work_dir, ignore_errors=True)

# [END composer_terraform_apply_operator]
