# Copyright 2018 Google LLC
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

"""GCS Plugin

This plugin provides an interface to GCS operator from Airflow Master.
"""

from airflow.plugins_manager import AirflowPlugin

from gcs_plugin.hooks.gcs_hook import GoogleCloudStorageHook
from gcs_plugin.operators.gcs_to_gcs import \
    GoogleCloudStorageToGoogleCloudStorageOperator


class GCSPlugin(AirflowPlugin):
    name = "gcs_plugin"
    operators = [GoogleCloudStorageToGoogleCloudStorageOperator]
    hooks = [GoogleCloudStorageHook]
