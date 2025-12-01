#!/usr/bin/env python
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

# [START composer_dag_linter_core]
"""
Core logic for the Composer DAG Linter & Parsing Profiler.

This script is executed inside an isolated Kubernetes Pod. It handles GCS downloads,
parallel parsing/profiling of DAG files, and final report generation. Its primary
goal is to detect parsing latency issues and identify heavy top-level code execution.
"""

import cProfile
import importlib.util
import io
import json
import logging
import os
import pstats
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from multiprocessing import Pool, cpu_count

from airflow.models.dag import DAG
from google.cloud import storage


class Ansi:
    """ANSI escape codes for colored terminal output."""
    # pylint: disable=too-few-public-methods
    BOLD = '\033[1m'
    RESET = '\033[0m'


def download_folder(bucket: storage.Bucket, prefix: str, local_subdir: str, config: dict, report_lines: list[str]) -> int:
    """Downloads a directory from GCS to a local path, mirroring the structure.

    Args:
        bucket: The google.cloud.storage Bucket object.
        prefix: The GCS prefix (folder) to download from.
        local_subdir: The subdirectory inside BASE_WORK_DIR to save files to.
        config: Dictionary containing BASE_WORK_DIR configuration.
        report_lines: A list of strings to append logs to (for final reporting).

    Returns:
        int: The number of files successfully downloaded.
    """
    base_work_dir = config['BASE_WORK_DIR']
    blobs = bucket.list_blobs(prefix=prefix)
    target_dir = os.path.join(base_work_dir, local_subdir)
    os.makedirs(target_dir, exist_ok=True)

    count = 0
    for blob in blobs:
        if blob.name.endswith('/'):
            continue

        # Calculate relative path (e.g., 'plugins/hooks/my_hook.py' -> 'hooks/my_hook.py')
        rel_path = os.path.relpath(blob.name, prefix)
        dest_path = os.path.join(target_dir, rel_path)

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        blob.download_to_filename(dest_path)
        count += 1

    report_lines.append(f"Downloaded {count} files from '{prefix}' to '{target_dir}'")
    return count


def parse_file(filepath: str, config: dict) -> dict:
    """Parses a single Python file to check for DAG integrity and import performance.

    This function is designed to be run in parallel. It captures stdout/stderr
    to prevent console interleaving and optionally profiles execution time.

    Args:
        filepath: The absolute path to the Python file to test.
        config: Dictionary containing configuration for profiling and logging.

    Returns:
        dict: A dictionary containing status (SUCCESS/WARNING/ERROR), messages,
              captured stdout/stderr, and optional profile data.
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    result = {}
    profiler = cProfile.Profile()

    # Load configuration (Snake case for local variables to satisfy pylint)
    profile_slow = config['PROFILE_SLOW']
    profile_sort_key = config['PROFILE_SORT_KEY']
    parse_threshold = config['PARSE_TIME_THRESHOLD_SECONDS']

    # Note: Temporarily disable logging to prevent plugins from printing to the console
    # during import, which would interleave with the linter's report output.
    previous_log_level = logging.root.manager.disable
    logging.disable(logging.CRITICAL)

    try:
        start_time = time.monotonic()

        # Capture standard print() statements
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            module_name = f"dag_linter_test.{os.path.basename(filepath).replace('.py', '')}"
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec is None:
                raise ImportError("Could not create module spec.")

            module = importlib.util.module_from_spec(spec)

            # Execute module import inside profiler
            profiler.runctx(
                'spec.loader.exec_module(module)',
                globals(),
                {"spec": spec, "module": module}
            )

        duration = time.monotonic() - start_time
        captured_stderr = stderr_buffer.getvalue()
        is_slow = duration > parse_threshold

        # Determine Status
        if captured_stderr:
            result = {'status': 'ERROR', 'message': "DAG generated error messages during parsing (see stderr)."}
        elif is_slow:
            result = {'status': 'WARNING', 'duration': duration, 'message': f"Slow parse time: {duration:.4f}s."}
        elif not any(isinstance(var, DAG) for var in vars(module).values()):
            result = {'status': 'WARNING', 'message': "Parsed, but no DAG objects were found."}
        else:
            result = {'status': 'SUCCESS', 'duration': duration, 'message': f"Parsed in {duration:.4f}s."}

        # Attach Profile Data if Slow
        if is_slow and profile_slow:
            profile_stream = io.StringIO()
            stats = pstats.Stats(profiler, stream=profile_stream).sort_stats(profile_sort_key)
            stats.print_stats(10)  # Limit to Top 10 offenders
            result['profile_output'] = profile_stream.getvalue()

    # pylint: disable=broad-except
    except Exception as e:
        result = {'status': 'ERROR', 'message': f"Failed to import file. Full error: {e}"}
    finally:
        # Restore logging configuration immediately
        logging.disable(previous_log_level)

    result['stdout'] = stdout_buffer.getvalue()
    result['stderr'] = stderr_buffer.getvalue()
    return result


def main(config_json: str):
    """Main execution flow for the Linter Pod.

    Args:
        config_json: A JSON string containing all necessary runtime configuration.
    """
    config = json.loads(config_json)

    report_lines = ["--- Starting DAG Linter ---"]

    # Extract config variables
    gcs_bucket = config['GCS_BUCKET']
    base_work_dir = config['BASE_WORK_DIR']
    fetch_extras = config['FETCH_EXTRAS']

    dags_source_folder = config['GCS_DAGS_SOURCE_FOLDER']
    plugins_source_folder = config['GCS_PLUGINS_SOURCE_FOLDER']
    data_source_folder = config['GCS_DATA_SOURCE_FOLDER']

    # Determine Parallelism based on available CPU resources
    parallelism = max(cpu_count() - 1, 1)

    # 1. Configure System Paths
    dags_dir = os.path.join(base_work_dir, "dags")
    plugins_dir = os.path.join(base_work_dir, "plugins")

    sys.path.append(dags_dir)
    sys.path.append(plugins_dir)

    # 2. Download Content from GCS
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(gcs_bucket)

        # Essential: Download DAGs
        download_folder(bucket, dags_source_folder, "dags", config, report_lines)

        # Optional: Download supporting folders
        if fetch_extras:
            report_lines.append("Flag enabled: Fetching data/ and plugins/ folders...")
            download_folder(bucket, data_source_folder, "data", config, report_lines)
            download_folder(bucket, plugins_source_folder, "plugins", config, report_lines)

    # pylint: disable=broad-except
    except Exception as e:
        report_lines.append(f"FATAL: GCS Download failed. Error: {e}")
        print("\n".join(report_lines))
        return

    # 3. Identify Target Files
    files_to_process = []
    if os.path.exists(dags_dir):
        for root, _, files in os.walk(dags_dir):
            for file in files:
                if not file.endswith(".py"):
                    continue
                
                # Exclude the orchestrator DAG and the Linter Core script
                # to prevent recursion loops or self-parsing errors.
                if file in ['dag_linter_kubernetes_pod.py', 'linter_core.py']:
                    continue

                files_to_process.append(os.path.join(root, file))

    if not files_to_process:
        report_lines.append("WARNING: No DAG files found.")
        print("\n".join(report_lines))
        return

    report_lines.append(f"Analyzing {len(files_to_process)} Python files using {parallelism} processes...")

    # 4. Execute Parallel Linting
    with Pool(processes=parallelism) as pool:
        results = pool.starmap(parse_file, [(f, config) for f in files_to_process])

    # 5. Generate Final Report
    report_lines.append("\n" + "#" * 80)
    report_lines.append("##### Linter Report #####".center(80, ' '))
    report_lines.append("#" * 80)
    has_issues = False

    for i, res in enumerate(results):
        filepath = files_to_process[i]
        filename = os.path.basename(filepath)

        report_lines.append(f"\n{Ansi.BOLD}########## [START] Processing: {filename} ##########{Ansi.RESET}")

        status = res.get('status', 'ERROR')
        message = res.get('message', 'Unknown error')

        if status == 'SUCCESS':
            report_lines.append(f"    ✅ Status: SUCCESS")
        elif status == 'WARNING':
            report_lines.append(f"    ⚠️ Status: WARNING")
            has_issues = True
        elif status == 'ERROR':
            report_lines.append(f"    🚨 Status: FAILED")
            has_issues = True

        report_lines.append(f"       Details: {message}")

        if res.get('stdout'):
            report_lines.append("    📋 Captured Output (stdout):")
            for line in res['stdout'].strip().split('\n'):
                report_lines.append(f"       | {line}")
        if res.get('stderr'):
            report_lines.append("    📋 Captured Errors (stderr):")
            for line in res['stderr'].strip().split('\n'):
                report_lines.append(f"       | {line}")
        if res.get('profile_output'):
            report_lines.append(f"    🔎 Performance Profile (Top 10 slowest calls by {config['PROFILE_SORT_KEY']}):")
            for line in res['profile_output'].strip().split('\n'):
                report_lines.append(f"       | {line}")

        report_lines.append(f"{Ansi.BOLD}########## [END] Processing: {filename} ##########{Ansi.RESET}")

    report_lines.append("\n" + "#" * 80)
    if has_issues:
        report_lines.append("Linter finished and found one or more performance issues.")
    else:
        report_lines.append("✅ Linting complete. All files parsed successfully.")

    print("\n".join(report_lines))


if __name__ == "__main__":
    # The KubernetesPodOperator passes the JSON configuration as sys.argv[1]
    if len(sys.argv) > 1:
        main(sys.argv[1])
# [END composer_dag_linter_core]