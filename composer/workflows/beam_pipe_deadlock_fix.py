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

# [START composer_beam_pipe_deadlock_fix]
"""Workaround for Apache Beam subprocess pipe deadlock in Cloud Composer.

When the JVM prints a JAVA_TOOL_OPTIONS startup message to stderr and a Beam
command writes more than 64 KB to stdout, the Apache Beam provider can deadlock
while reading the two pipes separately. This plugin replaces run_beam_command
with a version that merges stderr into stdout so one reader drains both streams.

Install:
  Upload this file to the plugins/ folder in your environment's Cloud Storage
  bucket.

Side effect:
  Beam subprocess stderr lines appear in task logs at INFO level instead of
  WARNING.

Cleanup:
  Delete this file after upgrading to a Cloud Composer version that includes
  the upstream fix in apache-airflow-providers-apache-beam.
"""

from __future__ import annotations

import shlex
import subprocess
from typing import Callable

import logging

# Airflow 3.1+ provides AirflowPlugin through the Task SDK; Airflow 2.5 to 3.0
# provides it through airflow.plugins_manager.
try:
    from airflow.sdk.plugins_manager import AirflowPlugin
except ImportError:
    from airflow.plugins_manager import AirflowPlugin


def _patched_run_beam_command(
    cmd: list[str],
    log: logging.Logger,
    process_line_callback: Callable[[str], None] | None = None,
    working_directory: str | None = None,
    is_dataflow_job_id_exist_callback: Callable[[], bool] | None = None,
    check_job_id_by_name_callback: Callable[[], bool] | None = None,
    *,
    check_job_status_callback: Callable[[], bool | None] | None = None,
    **_kwargs: object,
) -> None:
    # Import from the Beam hook module so the raised exception matches the
    # installed provider on both Airflow 2 and Airflow 3.
    from airflow.providers.apache.beam.hooks.beam import AirflowException

    # Support early exit across provider versions: 5.5-6.0 uses
    # check_job_status_callback; 6.0.1+ uses is_dataflow_job_id_exist_callback.
    stop_callback = is_dataflow_job_id_exist_callback or check_job_status_callback

    log.info("Running command: %s", " ".join(shlex.quote(c) for c in cmd))
    # Merge stderr into stdout so a single reader drains all subprocess output.
    proc = subprocess.Popen(
        cmd,
        cwd=working_directory,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=True,
    )
    log.info("Start waiting for Apache Beam process to complete.")

    # Close only the pipe in finally. Streaming and deferrable jobs require an
    # early return once stop_callback succeeds, so proc.wait() runs only after EOF.
    try:
        if proc.stdout is not None:
            for raw_line in iter(proc.stdout.readline, b""):
                line = raw_line.decode("utf-8", errors="replace")
                if process_line_callback:
                    process_line_callback(line)
                log.info("%s", line.rstrip("\r\n"))
                if stop_callback and stop_callback():
                    return
    finally:
        if proc.stdout is not None:
            proc.stdout.close()

    proc.wait()
    log.info("Process exited with return code: %s", proc.returncode)
    if proc.returncode != 0:
        raise AirflowException(
            f"Apache Beam process failed with return code {proc.returncode}"
        )

    # Preserve provider 6.3.2+ fallback for pipelines that disable job ID logs.
    if check_job_id_by_name_callback and not (stop_callback and stop_callback()):
        check_job_id_by_name_callback()


class BeamPipeDeadlockFixPlugin(AirflowPlugin):
    """Registers the patched Beam command runner when Airflow loads plugins."""

    name = "beam_pipe_deadlock_fix"

    @classmethod
    def on_load(cls, *args, **kwargs) -> None:
        # Airflow calls on_load once per process before running tasks.
        try:
            import airflow.providers.apache.beam.hooks.beam as beam_hook_mod
        except ImportError:
            return
        beam_hook_mod.run_beam_command = _patched_run_beam_command


# [END composer_beam_pipe_deadlock_fix]
