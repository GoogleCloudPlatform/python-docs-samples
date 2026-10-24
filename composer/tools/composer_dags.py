#!/usr/bin/env python

# Copyright 2022 Google LLC.
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
"""Standalone script to pause/unpause all the dags in the specific environment."""

import argparse
import logging
from typing import Any

import google.auth
from google.auth.transport.requests import AuthorizedSession

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
        self._airflow_uris = {}

    def _get_airflow_uri(self, environment_name: str) -> str:
        """Returns the Airflow URI for a given environment, caching the result."""
        if environment_name not in self._airflow_uris:
            environment = self.get_environment(environment_name)
            self._airflow_uris[environment_name] = environment["config"]["airflowUri"]
        return self._airflow_uris[environment_name]

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

    def pause_all_dags(self, environment_name: str) -> Any:
        """Pauses all DAGs in a Composer environment."""
        airflow_uri = self._get_airflow_uri(environment_name)

        url = f"{airflow_uri}/api/v1/dags?dag_id_pattern=%"
        response = self.session.patch(url, json={"is_paused": True})
        if response.status_code != 200:
            raise RuntimeError(f"Failed to pause all DAGs: {response.text}")

    def unpause_all_dags(self, environment_name: str) -> Any:
        """Unpauses all DAGs in a Composer environment."""
        airflow_uri = self._get_airflow_uri(environment_name)

        url = f"{airflow_uri}/api/v1/dags?dag_id_pattern=%"
        response = self.session.patch(url, json={"is_paused": False})
        if response.status_code != 200:
            raise RuntimeError(f"Failed to unpause all DAGs: {response.text}")


def main(
    project_name: str,
    environment: str,
    location: str,
    operation: str,
    sdk_endpoint: str,
) -> int:
    logger.info("DAG Pause/UnPause Script for Cloud Composer")

    client = ComposerClient(
        project=project_name, location=location, sdk_endpoint=sdk_endpoint
    )

    if operation == "pause":
        logger.info("Pausing all DAGs in the environment...")
        client.pause_all_dags(environment)
        logger.info("All DAGs paused.")
    else:
        # Optimization: use bulk unpause
        logger.info("Unpausing all DAGs in the environment...")
        client.unpause_all_dags(environment)
        logger.info("All DAGs unpaused.")
    return 0


def parse_arguments() -> dict[Any, Any]:
    """Parses command line parameters."""
    argument_parser = argparse.ArgumentParser(
        usage="Script to Pause/UnPause DAGs in Cloud Composer Environment \n"
    )
    argument_parser.add_argument("--operation", type=str, choices=["pause", "unpause"])
    argument_parser.add_argument("--project", type=str, required=True)
    argument_parser.add_argument("--environment", type=str, required=True)
    argument_parser.add_argument("--location", type=str, required=True)
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
            args.project,
            args.environment,
            args.location,
            args.operation,
            args.sdk_endpoint,
        )
    )
