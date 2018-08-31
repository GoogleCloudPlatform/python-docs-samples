"""
    GCS Plugin
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
