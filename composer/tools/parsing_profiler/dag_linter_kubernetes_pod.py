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

# [START composer_dag_parsing_profiler_dag]
"""
Orchestration DAG for the Composer Parsing Profiler.

This script defines the Airflow DAG that provisions and launches the isolated
profiling environment. It handles:
1. Configuration resolution (auto-detecting buckets and worker images).
2. Resource provisioning (ephemeral storage volumes).
3. Execution of the core analysis logic within a KubernetesPodOperator.
"""

from __future__ import annotations

import json
import os
import pendulum
import requests

import google.auth
from google.auth.transport.requests import Request

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s

# ==============================================================================
# ⚙️ CONFIGURATION SECTION
# ==============================================================================

# --- 1. Feature Flags ---
# Enable to run cProfile on DAGs that exceed the parse time threshold.
_CONFIG_PROFILE_SLOW_DAGS = True

# Enable to download 'data/' and 'plugins/' folders to the pod.
# Essential if your DAGs rely on custom plugins or local data files during import.
_CONFIG_FETCH_DATA_AND_PLUGINS = True

# Profiling Sorting Strategy:
# 'tottime' (Default): Sort by time spent INSIDE the function itself.
#                      Best for finding specific bottlenecks (math, regex, sleeps).
# 'cumtime':           Sort by cumulative time (function + sub-calls).
#                      Best for finding heavy high-level imports.
_CONFIG_PROFILE_SORT_KEY = "tottime"

# The maximum acceptable time (in seconds) for a DAG file to be parsed.
# Files exceeding this threshold trigger a WARNING and performance profiling.
#
# CALIBRATION HINT: This default is arbitrary. Parsing duration within this
# isolated Pod differs from the actual Scheduler parsing time. It is recommended
# to use the parse time of the simple, built-in 'airflow_monitoring' DAG as a
# reference baseline.
_CONFIG_PARSE_TIME_THRESHOLD_SECONDS = 1.0

# --- 2. Infrastructure Configuration ---

# OPTIONAL: Manual Override for the GCS Bucket.
# Leave as None to automatically detect the environment's default bucket.
# Set to a specific string only if you need to target a different environment's
# bucket (e.g., for cross-environment troubleshooting).
# Format: "region-envName-hash-bucket"
_CONFIG_GCS_BUCKET_NAME = None

# OPTIONAL: Manual Override for the Worker Image.
# Leave as None to automatically detect the correct image for the current environment.
# Set to a specific string URI only if you need to replicate a remote environment
# (see Cross-Environment Troubleshooting Guide below).
_CONFIG_POD_IMAGE = None

# --- 3. Source Folder Paths (Defaults) ---
# These variables define the specific source folders within the GCS bucket.
# They allow developers to point the linter at non-standard directories (e.g.,
# a test copy like 'dags_staging/') while the core script ensures the contents
# are mapped to the correct Airflow local directory name (dags, plugins, etc.)
# for validation.
_CONFIG_GCS_DAGS_SOURCE_FOLDER = "dags/"
_CONFIG_GCS_PLUGINS_SOURCE_FOLDER = "plugins/"
_CONFIG_GCS_DATA_SOURCE_FOLDER = "data/"

# --- 4. Kubernetes Resources ---
# The disk size is crucial for parallel processing, especially when downloading
# large supporting files. This configures ephemeral storage for the pod.
#
# CAUTION: If setting this value above 10Gi, ensure you are running on
# Composer 3+ environments (which support up to 100Gi). Large values often
# indicate unnecessary files; consider cleaning up the source folders before
# increasing this limit.
_CONFIG_POD_DISK_SIZE = "10Gi"  # Default set to 10Gi (typical Composer 2 maximum).

# Keep these values as the minimum resources. Having smaller values can crash the
# pod due to the heavy parallel processing and multiple DAG imports happening simultaneously.
_CONFIG_POD_NAMESPACE = "composer-user-workloads"
_CONFIG_POD_RESOURCES = k8s.V1ResourceRequirements(
    requests={"cpu": "4000m", "memory": "16Gi"},
    limits={"cpu": "4000m", "memory": "16Gi"},
)

# ==============================================================================
# 🧰 CROSS-ENVIRONMENT TROUBLESHOOTING GUIDE
# ==============================================================================
# For unstable environments (e.g., crashing schedulers), run this DAG from a
# stable Composer environment. Ensure the stable environment's service account
# has read access to the target environment's GCS bucket, and set POD_IMAGE
# manually to the exact image path in Artifact Registry of the unstable
# environment to have a valid replication scenario for the parsing analysis.
#
# Manual Image Retrieval:
# 1. Cloud Build Logs: Check the logs of the most recent successful build.
# 2. GKE (Composer 2): Go to Workloads > airflow-worker > YAML tab. Look for
#    the 'image:' field under the 'spec.containers' section.
# 3. Support: Customers with a valid support package can contact Google Cloud
#    Support for assistance in locating the correct worker image path.


# ==============================================================================
# 🕵️ IMAGE DETECTION LOGIC (ARTIFACT REGISTRY CHECK)
# ==============================================================================
def _verify_docker_image_v2(image_uri: str) -> bool:
    """
    Verifies if an image exists by checking its manifest via the Docker Registry V2 API.
    This mimics a 'docker pull' check and works even if 'list' permissions are restricted.
    """
    print(f"   🔎 Verifying Manifest for: {image_uri}")

    try:
        # 1. Parse the URI
        parts = image_uri.split('/')
        domain = parts[0]
        repo_path = "/".join(parts[1:])

        # 2. Construct V2 API URL
        api_url = f"https://{domain}/v2/{repo_path}/manifests/latest"

        # 3. Authenticate
        credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        credentials.refresh(Request())

        # 4. Request Manifest
        response = requests.get(
            api_url,
            headers={'Authorization': f'Bearer {credentials.token}'},
            timeout=10
        )

        if response.status_code == 200:
            print(f"   ✅ Manifest found (HTTP 200). Valid Custom Image.")
            return True

        if response.status_code == 404:
            print(f"   ℹ️  Manifest not found (HTTP 404). Confirmed Vanilla Environment.")
            return False

        print(f"   ⚠️  Access Forbidden (HTTP {response.status_code}). Assuming Vanilla.")
        return False

    except requests.RequestException as e:
        print(f"   ⚠️  Verification failed with error: {e}. Assuming Vanilla.")
        return False


def _get_c3_image_string() -> str | None:
    """Constructs and verifies the C3 image URL."""
    fingerprint = os.getenv('COMPOSER_OPERATION_FINGERPRINT')
    project_id = os.getenv('GCP_TENANT_PROJECT')
    location = os.getenv('COMPOSER_LOCATION')

    if not all([fingerprint, location, project_id]):
        return None

    image_uuid = fingerprint.split('@')[0]
    registry_domain = f"{location}-docker.pkg.dev"

    c3_image = f"{registry_domain}/{project_id}/composer-images/{image_uuid}"

    # Validate existence via Docker V2 API
    if _verify_docker_image_v2(c3_image):
        print(f"   ✅ Using C3 Image Path: {c3_image}")
        return c3_image

    return None


def _get_c2_image_api() -> str | None:
    """Queries the Google Artifact Registry API to find the latest Docker image (C2)."""
    project_id = os.getenv('GCP_PROJECT')
    location = os.getenv('COMPOSER_LOCATION')
    gke_name = os.getenv('COMPOSER_GKE_NAME')

    if not all([project_id, location, gke_name]):
        return None

    repo_name = f"composer-images-{gke_name}"
    print(f"   🔎 Querying Repo: projects/{project_id}/locations/{location}/repositories/{repo_name}")

    try:
        credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        credentials.refresh(Request())
    except google.auth.exceptions.DefaultCredentialsError as e:
        print(f"   ⚠️ Authentication failed: {e}")
        return None

    api_url = (
        f"https://artifactregistry.googleapis.com/v1/"
        f"projects/{project_id}/locations/{location}/repositories/{repo_name}/dockerImages"
    )

    try:
        response = requests.get(
            api_url,
            params={'pageSize': 1, 'orderBy': 'update_time desc'},
            headers={'Authorization': f'Bearer {credentials.token}'},
            timeout=10
        )

        if response.status_code == 404:
            print("   ℹ️  Repository not found (Likely a Vanilla Environment).")
            return None

        response.raise_for_status()
        data = response.json()

        if 'dockerImages' in data and len(data['dockerImages']) > 0:
            image_uri = data['dockerImages'][0]['uri']
            clean_uri = image_uri.split('@')[0]
            print(f"   ✅ Found Custom Image: {clean_uri}")
            return clean_uri
        else:
            print("   ℹ️  Repository exists but is empty (Vanilla Environment).")
            return None

    except requests.RequestException as e:
        print(f"   ⚠️ API Request failed: {e}")
        return None


def detect_worker_image(**context) -> str:
    """Determines the correct worker image to use for the profiler Pod.

    Logic:
    1. Manual: Checks _CONFIG_POD_IMAGE variable.
    2. C3 (Auto): Constructs path from Fingerprint and verifies manifest via V2 API.
    3. C2 (Auto): Queries Artifact Registry API.

    Returns:
        str: The full URI of the worker image to use.

    Raises:
        AirflowSkipException: If a custom image cannot be detected (Vanilla environment).
    """
    # 1. Check for Manual Override
    if _CONFIG_POD_IMAGE:
        print(f"✅ Using manually configured image: {_CONFIG_POD_IMAGE}")
        return _CONFIG_POD_IMAGE

    print("🔹 Manual image not configured. Attempting to detect CUSTOM image...")

    c3_fingerprint = os.getenv('COMPOSER_OPERATION_FINGERPRINT')

    if c3_fingerprint:
        print("   Detected: Composer 3 Environment")
        c3_image = _get_c3_image_string()
        if c3_image:
            return c3_image
    else:
        print("   Detected: Composer 2 Environment")
        c2_image = _get_c2_image_api()
        if c2_image:
            return c2_image

    # 4. Graceful Skip for Vanilla Environments
    print("   ⚠️  No Custom Image found. This environment appears to be 'Vanilla'.")
    print("   ⚠️  Skipping Linter execution as default images cannot be auto-detected.")

    raise AirflowSkipException(
        "Skipping: Vanilla Environment detected. To profile this environment, "
        "please retrieve the image manually (see 'Cross-Environment Guide' in code) "
        "and set the '_CONFIG_POD_IMAGE' variable."
    )


# ==============================================================================
# 🐍 LINTER SCRIPT GENERATION (EXECUTION TIME)
# ==============================================================================
def generate_linter_command(**context):
    """
    Reads the core script, resolves configuration, and builds the python command.
    """
    # 1. Resolve the GCS Bucket Name (Auto-detect or Manual)
    target_bucket = _CONFIG_GCS_BUCKET_NAME if _CONFIG_GCS_BUCKET_NAME else os.environ.get("GCS_BUCKET")

    if not target_bucket:
        raise ValueError(
            "🚨 FATAL: Could not auto-detect GCS Bucket. "
            "Please configure '_CONFIG_GCS_BUCKET_NAME' manually in the DAG file."
        )

    # 2. Read the content of the external script.
    # We use the location of the current file to find linter_core.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    core_script_path = os.path.join(current_dir, 'linter_core.py')

    try:
        with open(core_script_path, 'r') as f:
            linter_script_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find 'linter_core.py' at {core_script_path}. "
            "Ensure both files are in the DAGs folder."
        )

    # 3. Build the configuration dictionary
    linter_config_payload = {
        "GCS_BUCKET": target_bucket,
        "BASE_WORK_DIR": "/mnt/data/airflow_content",
        "FETCH_EXTRAS": _CONFIG_FETCH_DATA_AND_PLUGINS,
        "PROFILE_SLOW": _CONFIG_PROFILE_SLOW_DAGS,
        "PROFILE_SORT_KEY": _CONFIG_PROFILE_SORT_KEY,
        "PARSE_TIME_THRESHOLD_SECONDS": _CONFIG_PARSE_TIME_THRESHOLD_SECONDS,
        "GCS_DAGS_SOURCE_FOLDER": _CONFIG_GCS_DAGS_SOURCE_FOLDER,
        "GCS_PLUGINS_SOURCE_FOLDER": _CONFIG_GCS_PLUGINS_SOURCE_FOLDER,
        "GCS_DATA_SOURCE_FOLDER": _CONFIG_GCS_DATA_SOURCE_FOLDER,
    }

    # 4. Serialize the config dictionary to a JSON string
    config_json_arg = json.dumps(linter_config_payload)

    # 5. Construct the full Python command string
    # Use string concatenation (+) to prevent f-string corruption of the script content.
    final_command_string = (
        linter_script_content +
        f"\nmain('{config_json_arg}')"
    )

    # Push to XCom manually to avoid printing the huge command string in the logs
    context['task_instance'].xcom_push(key='linter_command', value=final_command_string)


# ==============================================================================
# 💨 DAG DEFINITION
# ==============================================================================
with DAG(
    dag_id="composer_dag_parser_profile",
    start_date=pendulum.datetime(2025, 8, 6, tz="UTC"),
    schedule=None,  # Triggered manually/on-demand
    catchup=False,
    tags=["profiler", "troubleshooting", "gcp-composer"],
    doc_md=__doc__,  # Use the module docstring as DAG documentation
) as dag:

    # Define the Volume and Volume Mount for guaranteed storage
    storage_volume = k8s.V1Volume(
        name="ephemeral-storage",
        # Use EmptyDir with size_limit to guarantee the requested ephemeral storage
        empty_dir=k8s.V1EmptyDirVolumeSource(size_limit=_CONFIG_POD_DISK_SIZE),
    )

    storage_volume_mount = k8s.V1VolumeMount(
        name="ephemeral-storage",
        mount_path="/mnt/data",  # Mount point used by BASE_WORK_DIR in injected script
    )

    # Task 1: Detect the correct worker image (Auto or Manual)
    detect_image_task = PythonOperator(
        task_id="detect_worker_image",
        python_callable=detect_worker_image,
        retries=0,  # FAIL FAST: If image detection fails (Vanilla), stop DAG immediately.
    )

    # Task 2: Prepare the Linter Command (Reads file, builds config)
    prepare_script_task = PythonOperator(
        task_id="prepare_linter_script",
        python_callable=generate_linter_command,
    )

    # Task 3: Execute the Linter Pod
    profile_and_check_linter = KubernetesPodOperator(
        task_id="profile_and_check_linter",
        name="dag-linter-pod",
        namespace=_CONFIG_POD_NAMESPACE,

        # Dynamically pull the image and command from previous tasks (using custom XCom key for command)
        image="{{ task_instance.xcom_pull(task_ids='detect_worker_image') }}",
        arguments=["-c", "{{ task_instance.xcom_pull(task_ids='prepare_linter_script', key='linter_command') }}"],
        cmds=["python"],

        container_resources=_CONFIG_POD_RESOURCES,
        do_xcom_push=False,
        get_logs=True,
        log_events_on_failure=True,
        startup_timeout_seconds=300,

        # Kubernetes connection parameters (Required for permissions in some environments)
        config_file="/home/airflow/composer_kube_config",
        kubernetes_conn_id="kubernetes_default",

        # Attach Ephemeral Storage Volume
        volumes=[storage_volume],
        volume_mounts=[storage_volume_mount],
    )

    detect_image_task >> prepare_script_task >> profile_and_check_linter
# [END composer_dag_parsing_profiler_dag]