# Copyright 2023 Google LLC
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

"""File containing abstract class for CPIX clients."""

import abc
import os

from google.cloud import secretmanager


class CpixClient(abc.ABC):
    """Abstract class for CPIX clients."""

    @abc.abstractmethod
    def fetch_keys(self, media_id: str, key_ids: list[str]):
        """Fetches encryption keys and prepares JSON content to be written to Secret Manager.

        Args:
        media_id (string): Name for your asset, sometimes used by DRM providers to
            show usage and reports.
        key_ids (string[]): List of IDs of any keys to fetch and prepare.

        Returns:
        dict: Object containing key information to be written to Secret Manager.
        """

    @property
    @abc.abstractmethod
    def required_env_vars(self):
        """Returns environment variables which must be set to use the class.

        The `PROJECT` env var is always required and does not need to be included
        in the returned list.

        Returns:
        list: list of strings, names of environment variables which must be
            set.
        """

    def access_secret_version(self, secret_id: str, version_id: str) -> list[str]:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.environ.get('PROJECT')
        secret_name = (
            f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
        )
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode().replace('\r\n', '\n')
