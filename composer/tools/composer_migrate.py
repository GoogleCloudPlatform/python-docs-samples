#!/usr/bin/env python

# Copyright 2025 Google LLC.
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
"""Standalone script for migrating environments from Composer 2 to Composer 3."""

import argparse
import json
import math
import pprint
import time
from typing import Any, Dict, List

import google.auth
from google.auth.transport.requests import AuthorizedSession
import requests

import logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class ComposerClient:
    """Client for interacting with Composer API.

    The client uses Google Auth and Requests under the hood.
    """

    def __init__(self, project: str, location: str, sdk_endpoint: str) -> None:
        self.project = project
        self.location = location
        self.sdk_endpoint = sdk_endpoint.rstrip("/")
        self.credentials, _ = google.auth.default()
        self.session = AuthorizedSession(self.credentials)

    def get_environment(self, environment_name: str) -> Any:
        """Returns an environment json for a given Composer environment."""
        url = (
            f"{self.sdk_endpoint}/v1/projects/{self.project}/locations/"
            f"{self.location}/environments/{environment_name}"
        )
        response = self.session.get(url)
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get environment {environment_name}: {response.text}"
            )
        return response.json()

    def create_environment_from_config(self, config: Any) -> Any:
        """Creates a Composer environment based on the given json config."""
        url = (
            f"{self.sdk_endpoint}/v1/projects/{self.project}/locations/"
            f"{self.location}/environments"
        )
        # Verify that the environment name is present in the config.
        # The API expects the resource name in the format:
        # projects/{project}/locations/{location}/environments/{environment_name}
        if "name" not in config:
             raise ValueError("Environment name is missing in the config.")
        
        # Extract environment ID from the full name if needed as query param,
        # but the original code didn't use it, so we trust the body 'name' field.
        # However, usually for Create, we might need environmentId query param if we want to specify it explicitly
        # and it's not inferred.
        # The original code did: POST .../environments with body.
        
        response = self.session.post(url, json=config)
        if response.status_code == 409:
            logger.info("Environment already exists, skipping creation.")
            return

        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to create environment: {response.text}"
            )
        
        operation = response.json()
        logging.info("Create environment operation: %s", operation["name"])
        self._wait_for_operation(operation["name"])


    def list_dags(self, environment_name: str) -> List[Dict[str, Any]]:
        """Returns a list of DAGs in a given Composer environment."""
        # Get authentication context and Airflow URI
        environment = self.get_environment(environment_name)
        airflow_uri = environment["config"]["airflowUri"]
        
        url = f"{airflow_uri}/api/v1/dags"
        response = self.session.get(url)
        if response.status_code != 200:
             raise RuntimeError(
                f"Failed to list DAGs: {response.text}"
            )
        return response.json()["dags"]


    def pause_dag(
        self,
        dag_id: str,
        environment_name: str,
    ) -> Any:
        """Pauses a DAG in a Composer environment."""
        environment = self.get_environment(environment_name)
        airflow_uri = environment["config"]["airflowUri"]
        
        url = f"{airflow_uri}/api/v1/dags/{dag_id}"
        response = self.session.patch(url, json={"is_paused": True})
        if response.status_code != 200:
             raise RuntimeError(
                f"Failed to pause DAG {dag_id}: {response.text}"
            )
    

    def pause_all_dags(
        self,
        environment_name: str,
    ) -> Any:
        """Pauses all DAGs in a Composer environment."""
        environment = self.get_environment(environment_name)
        airflow_uri = environment["config"]["airflowUri"]
        
        url = f"{airflow_uri}/api/v1/dags?dag_id_pattern=%" # Pause all DAGs using % as a wildcard
        response = self.session.patch(url, json={"is_paused": True})
        if response.status_code != 200:
             raise RuntimeError(
                f"Failed to pause all DAGs: {response.text}"
            )


    def unpause_dag(
        self,
        dag_id: str,
        environment_name: str,
    ) -> Any:
        """Unpauses a DAG in a Composer environment."""
        environment = self.get_environment(environment_name)
        airflow_uri = environment["config"]["airflowUri"]
        
        url = f"{airflow_uri}/api/v1/dags/{dag_id}"
        response = self.session.patch(url, json={"is_paused": False})
        if response.status_code != 200:
             raise RuntimeError(
                f"Failed to unpause DAG {dag_id}: {response.text}"
            )

    def unpause_all_dags(
        self,
        environment_name: str,
    ) -> Any:
        """Unpauses all DAGs in a Composer environment."""
        environment = self.get_environment(environment_name)
        airflow_uri = environment["config"]["airflowUri"]
        
        url = f"{airflow_uri}/api/v1/dags?dag_id_pattern=%" # Pause all DAGs using % as a wildcard
        response = self.session.patch(url, json={"is_paused": False})
        if response.status_code != 200:
             raise RuntimeError(
                f"Failed to unpause all DAGs: {response.text}"
            )            

    def save_snapshot(self, environment_name: str) -> str:
        """Saves a snapshot of a Composer environment."""
        url = (
            f"{self.sdk_endpoint}/v1/projects/{self.project}/locations/"
            f"{self.location}/environments/{environment_name}:saveSnapshot"
        )
        response = self.session.post(url, json={})
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to initiate snapshot save: {response.text}"
            )
        
        operation = response.json()
        logging.info("Save snapshot operation: %s", operation["name"])
        completed_operation = self._wait_for_operation(operation["name"])
        return completed_operation["response"]["snapshotPath"]

    def load_snapshot(
        self,
        environment_name: str,
        snapshot_path: str,
    ) -> Any:
        """Loads a snapshot to a Composer environment."""
        url = (
            f"{self.sdk_endpoint}/v1/projects/{self.project}/locations/"
            f"{self.location}/environments/{environment_name}:loadSnapshot"
        )
        response = self.session.post(url, json={"snapshotPath": snapshot_path})
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to initiate snapshot load: {response.text}"
            )

        operation = response.json()
        logging.info("Load snapshot operation: %s", operation["name"])
        self._wait_for_operation(operation["name"])


    def _wait_for_operation(self, operation_name: str) -> Any:
        """Waits for a long-running operation to complete."""
        # operation_name is distinct from operation_id.
        # It is a full resource name: projects/.../locations/.../operations/...
        
        # We need to poll the operation status.
        url = f"{self.sdk_endpoint}/v1/{operation_name}"
        
        while True:
            response = self.session.get(url)
            if response.status_code != 200:
                 raise RuntimeError(
                    f"Failed to get operation status: {response.text}"
                )
            operation = response.json()
            if "done" in operation and operation["done"]:
                if "error" in operation:
                    raise RuntimeError(f"Operation failed: {operation['error']}")
                logging.info("Operation completed successfully.")
                return operation
            
            logging.info("Waiting for operation to complete...")
            time.sleep(10)


def get_target_cpu(source_cpu: float, max_cpu: float) -> float:
    """Returns a target CPU value for a Composer 3 workload."""
    # Allowed values for Composer 3 workloads are 0.5, 1.0 and multiples of 2.0 up
    # to max_cpu.
    if source_cpu < 1.0:
        return 0.5

    if source_cpu == 1.0:
        return source_cpu

    return min(math.ceil(source_cpu / 2.0) * 2, max_cpu)


def get_target_memory_gb(source_memory_gb: float, target_cpu: float) -> float:
    """Returns a target memory in GB for a Composer 3 workload."""
    # Allowed values for Composer 3 workloads are multiples of 0.25
    # starting from 1 * cpu up to 8 * cpu, with minimum of 1 GB.
    target_memory_gb = math.ceil(source_memory_gb * 4.0) / 4.0
    return max(1.0, target_cpu, min(target_memory_gb, target_cpu * 8))


def get_target_storage_gb(source_storage_gb: float) -> float:
    """Returns a target storage in GB for a Composer 3 workload."""
    # Composer 3 allows only whole numbers of GB for storage, up to 100 GB.
    return min(math.ceil(source_storage_gb), 100.0)


def get_target_workloads_config(
    source_workloads_config: Any,
) -> Dict[str, Any]:
    """Returns a Composer 3 workloads config based on the source environment."""
    workloads_config = {}

    if source_workloads_config.get("scheduler"):
        scheduler_cpu = get_target_cpu(source_workloads_config["scheduler"]["cpu"], 1.0)

        workloads_config["scheduler"] = {
            "cpu": scheduler_cpu,
            "memoryGb": get_target_memory_gb(
                source_workloads_config["scheduler"]["memoryGb"], scheduler_cpu
            ),
            "storageGb": get_target_storage_gb(
                source_workloads_config["scheduler"]["storageGb"]
            ),
            "count": min(source_workloads_config["scheduler"]["count"], 3),
        }
        # Use configuration from the Composer 2 scheduler for Composer 3
        # dagProcessor.
        dag_processor_cpu = get_target_cpu(
            source_workloads_config["scheduler"]["cpu"], 32.0
        )
        workloads_config["dagProcessor"] = {
            "cpu": dag_processor_cpu,
            "memoryGb": get_target_memory_gb(
                source_workloads_config["scheduler"]["memoryGb"], dag_processor_cpu
            ),
            "storageGb": get_target_storage_gb(
                source_workloads_config["scheduler"]["storageGb"]
            ),
            "count": min(source_workloads_config["scheduler"]["count"], 3),
        }

    if source_workloads_config.get("webServer"):
        web_server_cpu = get_target_cpu(
            source_workloads_config["webServer"]["cpu"], 4.0
        )
        workloads_config["webServer"] = {
            "cpu": web_server_cpu,
            "memoryGb": get_target_memory_gb(
                source_workloads_config["webServer"]["memoryGb"], web_server_cpu
            ),
            "storageGb": get_target_storage_gb(
                source_workloads_config["webServer"]["storageGb"]
            ),
        }

    if source_workloads_config.get("worker"):
        worker_cpu = get_target_cpu(source_workloads_config["worker"]["cpu"], 32.0)
        workloads_config["worker"] = {
            "cpu": worker_cpu,
            "memoryGb": get_target_memory_gb(
                source_workloads_config["worker"]["memoryGb"], worker_cpu
            ),
            "storageGb": get_target_storage_gb(
                source_workloads_config["worker"]["storageGb"]
            ),
            "minCount": source_workloads_config["worker"]["minCount"],
            "maxCount": source_workloads_config["worker"]["maxCount"],
        }

    if source_workloads_config.get("triggerer"):
        triggerer_cpu = get_target_cpu(source_workloads_config["triggerer"]["cpu"], 1.0)
        workloads_config["triggerer"] = {
            "cpu": triggerer_cpu,
            "memoryGb": get_target_memory_gb(
                source_workloads_config["triggerer"]["memoryGb"], triggerer_cpu
            ),
            "count": source_workloads_config["triggerer"]["count"],
        }
    else:
        workloads_config["triggerer"] = {
            "count": 0,
        }

    return workloads_config


def get_target_environment_config(
    target_environment_name: str,
    target_airflow_version: str,
    source_environment: Any,
) -> Dict[str, Any]:
    """Returns a Composer 3 environment config based on the source environment."""
    # Use the same project and location as the source environment.
    target_environment_name = "/".join(
        source_environment["name"].split("/")[:-1] + [target_environment_name]
    )

    target_workloads_config = get_target_workloads_config(
        source_environment["config"].get("workloadsConfig", {})
    )

    target_node_config = {
        "network": source_environment["config"]["nodeConfig"].get("network"),
        "serviceAccount": source_environment["config"]["nodeConfig"]["serviceAccount"],
        "tags": source_environment["config"]["nodeConfig"].get("tags", []),
    }
    if "subnetwork" in source_environment["config"]["nodeConfig"]:
        target_node_config["subnetwork"] = source_environment["config"]["nodeConfig"][
            "subnetwork"
        ]

    target_environment = {
        "name": target_environment_name,
        "labels": source_environment.get("labels", {}),
        "config": {
            "softwareConfig": {
                "imageVersion": f"composer-3-airflow-{target_airflow_version}",
                "cloudDataLineageIntegration": (
                    source_environment["config"]["softwareConfig"].get(
                        "cloudDataLineageIntegration", {}
                    )
                ),
            },
            "nodeConfig": target_node_config,
            "privateEnvironmentConfig": {
                "enablePrivateEnvironment": (
                    source_environment["config"]
                    .get("privateEnvironmentConfig", {})
                    .get("enablePrivateEnvironment", False)
                )
            },
            "webServerNetworkAccessControl": source_environment["config"][
                "webServerNetworkAccessControl"
            ],
            "environmentSize": source_environment["config"]["environmentSize"],
            "databaseConfig": source_environment["config"]["databaseConfig"],
            "encryptionConfig": source_environment["config"]["encryptionConfig"],
            "maintenanceWindow": source_environment["config"]["maintenanceWindow"],
            "dataRetentionConfig": {
                "airflowMetadataRetentionConfig": source_environment["config"][
                    "dataRetentionConfig"
                ]["airflowMetadataRetentionConfig"]
            },
            "workloadsConfig": target_workloads_config,
        },
    }

    return target_environment


def main(
    project_name: str,
    location: str,
    source_environment_name: str,
    target_environment_name: str,
    target_airflow_version: str,
    sdk_endpoint: str,
    dry_run: bool,
) -> int:

    client = ComposerClient(
        project=project_name, location=location, sdk_endpoint=sdk_endpoint
    )

    # 1. Get the source environment, validate whether it is eligible
    # for migration and produce a Composer 3 environment config.
    logger.info("STEP 1: Getting and validating the source environment...")
    source_environment = client.get_environment(source_environment_name)
    logger.info("Source environment:\n%s", pprint.pformat(source_environment))
    image_version = source_environment["config"]["softwareConfig"]["imageVersion"]
    if not image_version.startswith("composer-2"):
        raise ValueError(
            f"Source environment {source_environment['name']} is not a Composer 2"
            f" environment. Current image version: {image_version}"
        )

    # 2. Create a Composer 3 environment based on the source environment
    # configuration.
    target_environment = get_target_environment_config(
        target_environment_name, target_airflow_version, source_environment
    )
    logger.info(
        "Composer 3 environment will be created with the following config:\n%s",
        pprint.pformat(target_environment),
    )
    logger.warning(
        "Composer 3 environment workloads config may be different from the"
        " source environment."
    )
    logger.warning(
        "Newly created Composer 3 environment will not have set"
        " 'airflowConfigOverrides', 'pypiPackages' and 'envVariables'. Those"
        " fields will be set when the snapshot is loaded."
    )
    if dry_run:
        logger.info("Dry run enabled, exiting.")
        return 0

    logger.info("STEP 2: Creating a Composer 3 environment...")
    client.create_environment_from_config(target_environment)
    target_environment = client.get_environment(target_environment_name)
    logger.info(
        "Composer 3 environment successfully created%s",
        pprint.pformat(target_environment),
    )

    # 3. Pause all DAGs in the source environment
    logger.info("STEP 3: Pausing all DAGs in the source environment...")
    source_env_dags = client.list_dags(source_environment_name)
    source_env_dag_ids = [dag["dag_id"] for dag in source_env_dags]
    logger.info(
        "Found %d DAGs in the source environment: %s",
        len(source_env_dags),
        source_env_dag_ids,
    )
    client.pause_all_dags(source_environment_name)
    logger.info("All DAGs in the source environment paused.")

    # 4. Save snapshot of the source environment
    logger.info("STEP 4: Saving snapshot of the source environment...")
    snapshot_path = client.save_snapshot(source_environment_name)
    logger.info("Snapshot saved: %s", snapshot_path)

    # 5. Load the snapshot into the target environment
    logger.info("STEP 5: Loading snapshot into the new environment...")
    client.load_snapshot(target_environment_name, snapshot_path)
    logger.info("Snapshot loaded.")

    # 6. Unpause DAGs in the new environment
    logger.info("STEP 6: Unpausing DAGs in the new environment...")
    all_dags_present = False
    # Wait until all DAGs from source environment are visible.
    while not all_dags_present:
        target_env_dags = client.list_dags(target_environment_name)
        target_env_dag_ids = [dag["dag_id"] for dag in target_env_dags]
        missing_dags = set(source_env_dag_ids) - set(target_env_dag_ids)
        all_dags_present = not missing_dags
        if missing_dags:
            logger.info("Waiting for DAGs to appear in target: %s", missing_dags)
        else:
            logger.info("All DAGs present in target environment.")
        time.sleep(10)
    # Unpause only DAGs that were not paused in the source environment.
    # Optimization: if all DAGs were unpaused in source, use bulk unpause.
    if not any(d["is_paused"] for d in source_env_dags):
        logger.info("All DAGs were unpaused in source. Unpausing all DAGs in target.")
        client.unpause_all_dags(target_environment_name)
    else:
        for dag in source_env_dags:
            if dag["is_paused"]:
                logger.info("DAG %s was paused in the source environment.", dag["dag_id"])
                continue
            logger.info("Unpausing DAG %s in the target environment.", dag["dag_id"])
            client.unpause_dag(dag["dag_id"], target_environment_name)
            logger.info("DAG %s unpaused.", dag["dag_id"])
    logger.info("DAGs in the target environment unpaused.")

    logger.info("Migration complete.")
    return 0


def parse_arguments() -> Dict[Any, Any]:
    """Parses command line arguments."""
    argument_parser = argparse.ArgumentParser(
        usage="Script for migrating environments from Composer 2 to Composer 3.\n"
    )

    argument_parser.add_argument(
        "--project",
        type=str,
        required=True,
        help="Project name of the Composer environment to migrate.",
    )
    argument_parser.add_argument(
        "--location",
        type=str,
        required=True,
        help="Location of the Composer environment to migrate.",
    )
    argument_parser.add_argument(
        "--source_environment",
        type=str,
        required=True,
        help="Name of the Composer 2 environment to migrate.",
    )
    argument_parser.add_argument(
        "--target_environment",
        type=str,
        required=True,
        help="Name of the Composer 3 environment to create.",
    )
    argument_parser.add_argument(
        "--target_airflow_version",
        type=str,
        default="2",
        help="Airflow version for the Composer 3 environment.",
    )
    argument_parser.add_argument(
        "--dry_run",
        action="store_true",
        default=False,
        help=(
            "If true, script will only print the config for the Composer 3"
            " environment."
        ),
    )
    argument_parser.add_argument(
        "--sdk_endpoint",
        type=str,
        default="https://composer.googleapis.com/",
        required=False,
    )

    return argument_parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    exit(
        main(
            project_name=args.project,
            location=args.location,
            source_environment_name=args.source_environment,
            target_environment_name=args.target_environment,
            target_airflow_version=args.target_airflow_version,
            sdk_endpoint=args.sdk_endpoint,
            dry_run=args.dry_run,
        )
    )
