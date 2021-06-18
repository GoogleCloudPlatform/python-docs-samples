#!/usr/bin/env python

# Copyright 2021 Google LLC. All Rights Reserved.
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

"""Database transfer script for Cloud Composer."""

import argparse
import json
import logging
import os
import re
import subprocess
import time
import typing
import uuid

SCRIPT_VERSION = "1.0"

USAGE = r"""This script handles database transfer for Cloud Composer
(Airflow 1.10.14/15 -> Airflow 2.0.1+).

EXPORT

  python3 composer_db_transfer.py export \
    --project [PROJECT NAME] \
    --environment [ENVIRONMENT NAME] \
    --location [REGION]
    --fernet-key-file [PATH TO FERNET KEY FILE - TO BE CREATED]

  CSV files with exported database are stored as
  /export/tables/[TABLE NAME].csv in the environment's bucket.
  dags, plugins and data directories are stored in
  /export/dirs in the environment's bucket.

  File with a fernet key is going to be created on the machine executing the
  script.

Copying the files between the environments

  Exported files can be copied to the target environment, e.g. with:

  gsutil -m cp -r \
    gs://[SOURCE ENV BUCKET NAME]/export \
    gs://[TARGET ENV BUCKET NAME]/import

IMPORT

  python3 composer_db_transfer.py import \
    --project [PROJECT NAME] \
    --environment [ENVIRONMENT NAME] \
    --location [REGION]
    --fernet-key-file [PATH TO FERNET KEY FILE FROM SOURCE ENVIRONMENT]

  CSV files that should be imported are expected to be stored as
  /import/tables/[TABLE NAME].csv in the environment's bucket.
  dags, plugins and data directories that should be imported are expected to be
  stored in /import/dirs in the environment's bucket.

  `fernet-key-file` parameter specifies path to the fernet key file of the
  source environment on the machine executing the script. It is created during
  export phase.

TROUBLESHOOTING

  Check "Troubleshooting" section of the script manual for troubleshooting
  guidance.

Temporary kubeconfig file is created in the current directory.
"""


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class Command:
    """Provides run_shell_command function to invoke shell commands."""

    class CommandExecutionError(Exception):
        pass

    @staticmethod
    def run_shell_command(
        command: typing.List[str],
        use_shell: bool = False,
        retry_number: int = 3,
        delay: float = 4.0,
        command_input: str = None,
        log_command: bool = True,
        log_error: bool = True,
    ) -> str:
        """Executes shell command with given maximum number of retries on failure."""
        for i in range(retry_number + 1):
            try:
                return Command._run_shell_command(
                    command,
                    use_shell,
                    command_input=command_input,
                    log_command=log_command,
                )
            except Command.CommandExecutionError as e:
                if log_error:
                    logger.error(e)
                if i == retry_number:
                    raise
                time.sleep(delay)
                if log_command:
                    logger.info("Retrying...")

    @staticmethod
    def _run_shell_command(
        command: typing.List[str],
        use_shell: bool = False,
        command_input: str = None,
        log_command: bool = True,
    ) -> str:
        """Executes shell command and returns its output."""

        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=use_shell
        )
        if log_command:
            logger.info("Executing shell command: %s", command)
        (res, _) = p.communicate(input=command_input)
        if p.returncode:
            logged_command = f' "{command}"' if log_command else ""
            error_message = (
                f"Failed to run shell command{logged_command}, " f"details: {res}"
            )
            raise Command.CommandExecutionError(error_message)
        return str(res.decode().strip("\n"))


class DatabaseUtils:
    """Utility functions for interactions with CloudSQL."""

    # Null values are exported to CSV files as this string. As with high enough
    # probability this string is not going to appear in any value, conversion of
    # nulls to unquoted empty strings (as required by PostgreSQL) can be performed
    # in postprocessing phase with sed.
    null_string = "a8fc0a-b77fe61-a9cf0b-9a0abf"

    @staticmethod
    def nullable(column: str) -> str:
        """Returns SQL expression processing nullable column for export.

        Returned expression transforms nullable column into either its value
        (if not null) or DatabaseUtils.null_string (if null).
        This is necessary to process exported columns as MySQL exports nulls as
        opening double-quote and capital N ("N), wchich breaks CSV file structure.
        Null can not be transformed into empty string here, because during import
        from CSV PostgreSQL differentiates between quoted empty string (translated
        to empty string) and unquoted empty string (translated to null).

        Args:
          column: name of the column
        """
        return (
            f'CASE WHEN {column} IS NULL THEN "{DatabaseUtils.null_string}" '
            f"ELSE {column} END"
        )

    @staticmethod
    def blob(column: str) -> str:
        """Returns SQL expression processing blob column for export."""
        big_enough_length_to_hold_hex_representation_of_blob = 150000
        return (
            f'CASE WHEN {column} IS NULL THEN "{DatabaseUtils.null_string}" '
            fr'ELSE CONCAT("\\\x", CAST(HEX({column}) '
            f"as char({big_enough_length_to_hold_hex_representation_of_blob}))) "
            "END"
        )

    @staticmethod
    def fetch_cloudsql_service_account_through_the_workload(
        namespace: str,
        pod_name: str,
        container_name: str,
        sql_instance_name: str,
        project_name: str,
    ) -> str:
        """Returns service account name used by given CloudSQL instance."""
        logger.info("Fetching service account name of Cloud SQL...")
        sql_instance_json = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"gcloud sql instances describe {sql_instance_name} "
            f"--project {project_name} --format json",
        )
        sql_instance_config = json.loads(sql_instance_json)
        sql_service_account = sql_instance_config["serviceAccountEmailAddress"]
        logger.info("Cloud SQL service account: %s", sql_service_account)
        return sql_service_account


# List of the tables/columns that should be exported/imported during database
# migration from Airflow 1.10.15 to Airflow 2.*.*.
# (table name, list of columns, does it require fixing sequence number after
# importing explicitly given primary keys)
#
# Order of the tables is relevant as a row can not be inserted if it refers
# (through a foreign key) to not yet inserted row from other table.
#
# dag_code and serialized_dag tables are skipped, as they are going to be
# automatically recreated once DAG code is imported.
tables = [
    ("ab_role", ["id", "name"], True),
    ("ab_permission", ["id", "name"], True),
    (
        "ab_view_menu",
        [
            "id",
            DatabaseUtils.nullable("name"),
        ],
        True,
    ),
    (
        "ab_permission_view",
        [
            "id",
            DatabaseUtils.nullable("permission_id"),
            DatabaseUtils.nullable("view_menu_id"),
        ],
        True,
    ),
    (
        "ab_permission_view_role",
        [
            "id",
            DatabaseUtils.nullable("permission_view_id"),
            DatabaseUtils.nullable("role_id"),
        ],
        True,
    ),
    (
        "ab_register_user",
        [
            "id",
            "first_name",
            "last_name",
            "username",
            DatabaseUtils.nullable("password"),
            "email",
            DatabaseUtils.nullable("registration_date"),
            DatabaseUtils.nullable("registration_hash"),
        ],
        True,
    ),
    (
        "ab_user",
        [
            "id",
            "first_name",
            "last_name",
            "username",
            DatabaseUtils.nullable("password"),
            DatabaseUtils.nullable("active"),
            "email",
            DatabaseUtils.nullable("last_login"),
            DatabaseUtils.nullable("login_count"),
            DatabaseUtils.nullable("fail_login_count"),
            DatabaseUtils.nullable("created_on"),
            DatabaseUtils.nullable("changed_on"),
            DatabaseUtils.nullable("created_by_fk"),
            DatabaseUtils.nullable("changed_by_fk"),
        ],
        True,
    ),
    (
        "ab_user_role",
        [
            "id",
            DatabaseUtils.nullable("user_id"),
            DatabaseUtils.nullable("role_id"),
        ],
        True,
    ),
    ("alembic_version", ["*"], False),
    (
        "chart",
        [
            "id",
            DatabaseUtils.nullable("label"),
            DatabaseUtils.nullable("conn_id"),
            DatabaseUtils.nullable("user_id"),
            DatabaseUtils.nullable("chart_type"),
            DatabaseUtils.nullable("sql_layout"),
            DatabaseUtils.nullable("chart.sql"),
            DatabaseUtils.nullable("y_log_scale"),
            DatabaseUtils.nullable("show_datatable"),
            DatabaseUtils.nullable("show_sql"),
            DatabaseUtils.nullable("height"),
            DatabaseUtils.nullable("default_params"),
            DatabaseUtils.nullable("x_is_date"),
            DatabaseUtils.nullable("iteration_no"),
            DatabaseUtils.nullable("last_modified"),
        ],
        True,
    ),
    (
        "connection",
        [
            "id",
            DatabaseUtils.nullable("conn_id"),
            DatabaseUtils.nullable("conn_type"),
            DatabaseUtils.nullable("host"),
            DatabaseUtils.nullable("connection.schema"),
            DatabaseUtils.nullable("login"),
            DatabaseUtils.nullable("password"),
            DatabaseUtils.nullable("port"),
            DatabaseUtils.nullable("extra"),
            DatabaseUtils.nullable("is_encrypted"),
            DatabaseUtils.nullable("is_extra_encrypted"),
        ],
        True,
    ),
    (
        "dag",
        [
            "dag_id",
            DatabaseUtils.nullable("is_paused"),
            DatabaseUtils.nullable("is_subdag"),
            DatabaseUtils.nullable("is_active"),
            DatabaseUtils.nullable("last_scheduler_run"),
            DatabaseUtils.nullable("last_pickled"),
            DatabaseUtils.nullable("last_expired"),
            DatabaseUtils.nullable("scheduler_lock"),
            DatabaseUtils.nullable("pickle_id"),
            DatabaseUtils.nullable("fileloc"),
            DatabaseUtils.nullable("owners"),
            DatabaseUtils.nullable("description"),
            DatabaseUtils.nullable("default_view"),
            DatabaseUtils.nullable("schedule_interval"),
            DatabaseUtils.nullable("root_dag_id"),
        ],
        False,
    ),
    (
        "dag_pickle",
        [
            "id",
            DatabaseUtils.blob("pickle"),
            DatabaseUtils.nullable("created_dttm"),
            DatabaseUtils.nullable("pickle_hash"),
        ],
        True,
    ),
    (
        "dag_run",
        [
            "id",
            DatabaseUtils.nullable("dag_id"),
            DatabaseUtils.nullable("execution_date"),
            DatabaseUtils.nullable("state"),
            DatabaseUtils.nullable("run_id"),
            DatabaseUtils.nullable("external_trigger"),
            DatabaseUtils.blob("conf"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("start_date"),
        ],
        True,
    ),
    ("dag_tag", ["*"], False),
    (
        "import_error",
        [
            "id",
            DatabaseUtils.nullable("timestamp"),
            DatabaseUtils.nullable("filename"),
            DatabaseUtils.nullable("stacktrace"),
        ],
        True,
    ),
    (
        "job",
        [
            "id",
            DatabaseUtils.nullable("dag_id"),
            DatabaseUtils.nullable("state"),
            DatabaseUtils.nullable("job_type"),
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("latest_heartbeat"),
            DatabaseUtils.nullable("executor_class"),
            DatabaseUtils.nullable("hostname"),
            DatabaseUtils.nullable("unixname"),
        ],
        True,
    ),
    (
        "known_event",
        [
            "id",
            DatabaseUtils.nullable("label"),
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("user_id"),
            DatabaseUtils.nullable("known_event_type_id"),
            DatabaseUtils.nullable("description"),
        ],
        True,
    ),
    (
        "known_event_type",
        [
            "id",
            DatabaseUtils.nullable("know_event_type"),
        ],
        True,
    ),
    (
        "kube_resource_version",
        [
            "one_row_id",
            DatabaseUtils.nullable("resource_version"),
        ],
        False,
    ),
    (
        "kube_worker_uuid",
        [
            "one_row_id",
            DatabaseUtils.nullable("worker_uuid"),
        ],
        False,
    ),
    (
        "log",
        [
            "id",
            DatabaseUtils.nullable("dttm"),
            DatabaseUtils.nullable("dag_id"),
            DatabaseUtils.nullable("task_id"),
            DatabaseUtils.nullable("event"),
            DatabaseUtils.nullable("execution_date"),
            DatabaseUtils.nullable("owner"),
            DatabaseUtils.nullable("extra"),
        ],
        True,
    ),
    ("rendered_task_instance_fields", ["*"], False),
    (
        "sla_miss",
        [
            "task_id",
            "dag_id",
            "execution_date",
            DatabaseUtils.nullable("email_sent"),
            DatabaseUtils.nullable("timestamp"),
            DatabaseUtils.nullable("description"),
            DatabaseUtils.nullable("notification_sent"),
        ],
        False,
    ),
    (
        "slot_pool",
        [
            "id",
            DatabaseUtils.nullable("pool"),
            DatabaseUtils.nullable("slots"),
            DatabaseUtils.nullable("description"),
        ],
        True,
    ),
    (
        "task_fail",
        [
            "id",
            "task_id",
            "dag_id",
            "execution_date",
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("duration"),
        ],
        True,
    ),
    (
        "task_instance",
        [
            "task_id",
            "dag_id",
            "execution_date",
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("duration"),
            DatabaseUtils.nullable("state"),
            DatabaseUtils.nullable("try_number"),
            DatabaseUtils.nullable("hostname"),
            DatabaseUtils.nullable("unixname"),
            DatabaseUtils.nullable("job_id"),
            "pool",
            DatabaseUtils.nullable("queue"),
            DatabaseUtils.nullable("priority_weight"),
            DatabaseUtils.nullable("operator"),
            DatabaseUtils.nullable("queued_dttm"),
            DatabaseUtils.nullable("pid"),
            DatabaseUtils.nullable("max_tries"),
            DatabaseUtils.blob("executor_config"),
            DatabaseUtils.nullable("pool_slots"),
        ],
        False,
    ),
    (
        "task_reschedule",
        [
            "id",
            "task_id",
            "dag_id",
            "execution_date",
            "try_number",
            "start_date",
            "end_date",
            "duration",
            "reschedule_date",
        ],
        True,
    ),
    (
        "users",
        [
            "id",
            DatabaseUtils.nullable("username"),
            DatabaseUtils.nullable("email"),
            DatabaseUtils.nullable("password"),
            DatabaseUtils.nullable("superuser"),
        ],
        True,
    ),
    (
        "variable",
        [
            "id",
            DatabaseUtils.nullable("variable.key"),
            DatabaseUtils.nullable("val"),
            DatabaseUtils.nullable("is_encrypted"),
        ],
        True,
    ),
    (
        "xcom",
        [
            "id",
            DatabaseUtils.nullable("xcom.key"),
            DatabaseUtils.blob("value"),
            "timestamp",
            "execution_date",
            "task_id",
            "dag_id",
        ],
        True,
    ),
]


class EnvironmentUtils:
    """Utility functions for interactions with Composer environment."""

    @staticmethod
    def unique_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def read_environment_config(
        project_name: str, environment_name: str, location: str
    ) -> typing.Dict[typing.Any, typing.Any]:
        logger.info("*** Fetching details of the environment: %s...", environment_name)
        environment_json = Command.run_shell_command(
            [
                "gcloud",
                "composer",
                "environments",
                "describe",
                environment_name,
                "--project",
                project_name,
                "--location",
                location,
                "--format",
                "json",
            ]
        )
        return json.loads(environment_json)

    @staticmethod
    def get_gke_credentials(gke_id: str) -> None:
        """Gets credentials of gived GKE cluster."""
        items = gke_id.split("/")
        if (
            len(items) != 6
            or items[0] != "projects"
            or (items[2] != "zones" and items[2] != "locations")
            or items[4] != "clusters"
        ):
            raise Exception(
                f'GKE id "{gke_id}" is not an appriopriate id of GKE cluster.'
            )
        shell_command = [
            "gcloud",
            "container",
            "clusters",
            "get-credentials",
            gke_id,
            "--zone" if items[2] == "zones" else "--region",
            items[3],
        ]
        Command.run_shell_command(shell_command)

    @staticmethod
    def access_gke_cluster(
        project_name: str, environment_name: str, location: str
    ) -> str:
        """Gets credentials for the environment's cluster and returns its id."""
        logger.info("*** Inspecting GKE cluster...")
        environment_config = EnvironmentUtils.read_environment_config(
            project_name, environment_name, location
        )
        gke_id = environment_config["config"]["gkeCluster"]
        logger.info("GKE URL: %s", gke_id)
        EnvironmentUtils.get_gke_credentials(gke_id)
        return gke_id

    @staticmethod
    def get_pods_config() -> typing.Dict[typing.Any, typing.Any]:
        """Returns configuration of pods in given GKE cluster."""
        shell_command = [
            "kubectl",
            "get",
            "pods",
            "--all-namespaces",
            "--field-selector=status.phase=Running",
            "-o",
            "json",
        ]
        pods_json = Command.run_shell_command(shell_command)
        pods_config = json.loads(pods_json)
        return pods_config

    @staticmethod
    def get_pod_with_label(
        pods_config: typing.Dict[typing.Any, typing.Any], label: str
    ) -> typing.Dict[typing.Any, typing.Any]:
        """Returns a pod with a given label."""
        for pod_desc in pods_config["items"]:
            if (
                "run" in pod_desc["metadata"]["labels"]
                and pod_desc["metadata"]["labels"]["run"] == label
            ):
                namespace = pod_desc["metadata"]["namespace"]
                name = pod_desc["metadata"]["name"]
                logger.info(
                    "The following pod has been found: namespace = %s; name = %s",
                    namespace,
                    name,
                )
                return pod_desc
        raise Exception(
            f'Could not find any pod with label "{label}" running in the cluster.'
        )

    @staticmethod
    def get_namespace_and_name_from_pod(
        pod_desc: typing.Dict[typing.Any, typing.Any]
    ) -> typing.Tuple[str, str]:
        """Returns namespace and name of a given pod."""
        return pod_desc["metadata"]["namespace"], pod_desc["metadata"]["name"]

    @staticmethod
    def create_gke_worfload(workload_definition: str, deployment_name: str) -> str:
        """Creates a workload in GKE cluster."""
        file_name = f"deployment-{deployment_name}.yaml"
        with open(file_name, "w") as file:
            file.write(workload_definition)
        shell_command = ["kubectl", "create", "-f", file_name]
        logger.info("Creating GKE workload...")
        return Command.run_shell_command(shell_command)

    @staticmethod
    def execute_command_in_a_pod(
        namespace: str,
        pod_name: str,
        container_name: str,
        command: str,
        log_command: bool = True,
        log_error: bool = True,
    ) -> str:
        """Executes shell command in a given pod."""
        shell_command = [
            "kubectl",
            "exec",
            "-t",
            "-n",
            namespace,
            pod_name,
            "-c",
            container_name,
            "--",
            "bash",
            "-c",
            command,
        ]
        return Command.run_shell_command(
            shell_command, log_command=log_command, log_error=log_error
        )

    @staticmethod
    def read_env_variable_from_container(
        namespace: str,
        pod_name: str,
        container_name: str,
        env_name: str,
        log_env_var_value: bool = True,
    ) -> str:
        """Reads environment variable from a given container."""
        value = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"echo ${env_name}",
            log_command=log_env_var_value,
        )
        logger.info(
            'Fetch environment variable: %s = "%s"',
            env_name,
            value if log_env_var_value else "[HIDDEN]",
        )
        return value

    @staticmethod
    def grant_permissions_to_the_bucket(
        service_account: str,
        bucket_name: str,
        namespace: str,
        pod_name: str,
        container_name: str,
    ) -> None:
        """Grants objectAdmin permission to a given bucket."""
        logger.info(
            "Granting permissions for %s to access %s...", service_account, bucket_name
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"gsutil iam ch serviceAccount:{service_account}:"
            f"legacyBucketWriter,legacyObjectOwner gs://{bucket_name}",
        )
        logger.info(output)

    @staticmethod
    def revoke_permissions_to_the_bucket(
        service_account: str,
        bucket_name: str,
        namespace: str,
        pod_name: str,
        container_name: str,
    ) -> None:
        """Revokes objectAdmin permission to a given bucket."""
        logger.info(
            "Revoking permissions for %s to access %s...", service_account, bucket_name
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"gsutil iam ch -d serviceAccount:{service_account}:"
            f"legacyBucketWriter,legacyObjectOwner gs://{bucket_name}",
        )
        logger.info(output)

    @staticmethod
    def create_database_through_exising_workload(
        namespace: str,
        pod_name: str,
        container_name: str,
        sql_instance: str,
        project: str,
        database_name: str,
    ) -> str:
        """Creates new database in existing CloudSQL instance."""
        command = (
            f"gcloud sql databases create {database_name} -i {sql_instance} "
            f"--charset=utf-8 --project {project}"
        )
        return EnvironmentUtils.execute_command_in_a_pod(
            namespace, pod_name, container_name, command
        )

    @staticmethod
    def run_database_creation_workload_for_source_version(
        namespace: str,
        image: str,
        bucket: str,
        temporary_database_name: str,
        customer_project: str,
        unique_id: str,
        sql_proxy: str,
    ) -> str:
        """Runs airflow-database-init-job job on environment's GKE cluster."""
        workload_definition = f"""apiVersion: batch/v1
kind: Job
metadata:
  name: airflow-database-init-job-{unique_id}
  namespace: {namespace}
  labels:
    run: airflow-database-init-job
spec:
  backoffLimit: 12
  template:
    metadata:
      name: airflow-database-init-job-{unique_id}
    spec:
      priorityClassName: high-priority
      volumes:
      - name: airflow-config
        configMap:
          name: airflow-configmap
      containers:
      - image: {image}
        imagePullPolicy: IfNotPresent
        command:
        - /var/local/db_init.sh
        name: airflow-database-init-job
        securityContext:
          privileged: true
        env:
        - name: GCS_BUCKET
          value: {bucket}
        - name: AIRFLOW_HOME
          value: /etc/airflow
        - name: DAGS_FOLDER
          value: /home/airflow/gcs/dags
        - name: SQL_DATABASE
          value: {temporary_database_name}
        - name: SQL_USER
          value: root
        - name: SQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: airflow-secrets
              key: sql_password
        - name: AIRFLOW__CORE__SQL_ALCHEMY_CONN
          value: "postgresql+psycopg2://$(SQL_USER):$(SQL_PASSWORD)@{sql_proxy}:3306/$(SQL_DATABASE)"
        - name: AIRFLOW__CORE__FERNET_KEY
          valueFrom:
            secretKeyRef:
              name: airflow-secrets
              key: fernet_key
        - name: GCP_PROJECT
          value: {customer_project}
        - name: COMPOSER_PYTHON_VERSION
          value: "3"
        volumeMounts:
        - name: airflow-config
          mountPath: /etc/airflow/airflow_cfg
      dnsPolicy: ClusterFirst
      restartPolicy: Never
      securityContext: {{}}
      terminationGracePeriodSeconds: 30
"""
        return EnvironmentUtils.create_gke_worfload(workload_definition, unique_id)


class DatabasePorter:
    """Common routines for exporter and importer."""

    def __init__(self: typing.Any, expected_airflow_database_version: str) -> None:
        self._expected_airflow_database_version = expected_airflow_database_version

    def _check_environment(self: typing.Any) -> None:
        """Gathers information about the Composer environment."""
        logger.info("*** Inspecting Composer environment...")
        self.unique_id = EnvironmentUtils.unique_id()
        self._access_gke_cluster()
        self.pods_config = EnvironmentUtils.get_pods_config()
        self._read_environment_variables_from_monitoring_pod()
        self._find_worker_pod()
        self._check_drs_and_select_db_storage_bucket()
        self._read_fernet_key()
        self.sql_service_account = (
            DatabaseUtils.fetch_cloudsql_service_account_through_the_workload(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                self.sql_instance_name,
                self.tenant_project_name,
            )
        )
        self._check_database_version()
        self._check_composer_system_namespace()
        self._check_cloud_sql_proxy()

    def _access_gke_cluster(self: typing.Any) -> None:
        """Exports custom KUBECTL and requests credentials to the GKE cluster."""
        self._kubeconfig_file_name = f"kubeconfig-{self.unique_id}"
        os.environ["KUBECONFIG"] = self._kubeconfig_file_name
        EnvironmentUtils.access_gke_cluster(
            self.project_name, self.environment_name, self.location
        )

    def _remove_temporary_kubeconfig(self: typing.Any) -> None:
        """Removes temporary kubeconfig file."""
        if os.path.isfile(self._kubeconfig_file_name):
            os.remove(self._kubeconfig_file_name)

    def _grant_permissions(self: typing.Any) -> None:
        """Grants required permissions."""
        if not self.is_drs_enabled:
            logger.info("*** Granting required permissions...")
            EnvironmentUtils.grant_permissions_to_the_bucket(
                self.sql_service_account,
                self.gcs_bucket_name,
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
            )

    def _revoke_permissions(self: typing.Any) -> None:
        """Revokes no longer required permissions."""
        logger.info("*** Revoking no longer needed permissions...")
        if not self.is_drs_enabled:
            EnvironmentUtils.revoke_permissions_to_the_bucket(
                self.sql_service_account,
                self.gcs_bucket_name,
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
            )

    def _find_worker_pod(self: typing.Any) -> None:
        """Finds namespace and name of a worker pod existing in an environment."""
        self.worker_container_name = "airflow-worker"
        pod_desc = EnvironmentUtils.get_pod_with_label(
            self.pods_config, self.worker_container_name
        )
        (
            self.worker_pod_namespace,
            self.worker_pod_name,
        ) = EnvironmentUtils.get_namespace_and_name_from_pod(pod_desc)
        self.worker_pod_desc = pod_desc

    def _read_environment_variables_from_monitoring_pod(self: typing.Any) -> None:
        """Reads relevant environment variables from airflow-monitoring."""
        logger.info("*** Reading environment variables from airflow-monitoring pod...")
        pod_desc = EnvironmentUtils.get_pod_with_label(
            self.pods_config, "airflow-monitoring"
        )
        (
            monitoring_pod_namespace,
            monitoring_pod_name,
        ) = EnvironmentUtils.get_namespace_and_name_from_pod(pod_desc)
        self.airflow_database_version = (
            EnvironmentUtils.read_env_variable_from_container(
                monitoring_pod_namespace,
                monitoring_pod_name,
                "airflow-monitoring",
                "AIRFLOW_DATABASE_VERSION",
            )
        )
        self.sql_instance_name = EnvironmentUtils.read_env_variable_from_container(
            monitoring_pod_namespace,
            monitoring_pod_name,
            "airflow-monitoring",
            "SQL_INSTANCE_NAME",
        ).split(":")[1]
        self.sql_database = EnvironmentUtils.read_env_variable_from_container(
            monitoring_pod_namespace,
            monitoring_pod_name,
            "airflow-monitoring",
            "SQL_DATABASE",
        )
        self.gcs_bucket_name = EnvironmentUtils.read_env_variable_from_container(
            monitoring_pod_namespace,
            monitoring_pod_name,
            "airflow-monitoring",
            "GCS_BUCKET",
        )
        self.cp_bucket_name = self.gcs_bucket_name
        self.tenant_project_name = EnvironmentUtils.read_env_variable_from_container(
            monitoring_pod_namespace,
            monitoring_pod_name,
            "airflow-monitoring",
            "TENANT_PROJECT",
        )

    def _read_fernet_key(self: typing.Any) -> None:
        self.fernet_key = EnvironmentUtils.read_env_variable_from_container(
            self.worker_pod_namespace,
            self.worker_pod_name,
            "airflow-worker",
            "AIRFLOW__CORE__FERNET_KEY",
            log_env_var_value=False,
        )

    def _check_database_version(self: typing.Any) -> None:
        """Checks database version in the environment."""
        logger.info("*** Veryfying database version...")
        if self.airflow_database_version != self._expected_airflow_database_version:
            raise Exception(
                "This operation is meant for Composer environments"
                f" with {self._expected_airflow_database_version}."
            )

    def _check_composer_system_namespace(self: typing.Any) -> None:
        """Checks existence of composer-system namespace."""
        logger.info("*** Checking if composer-system namespace exists...")
        try:
            Command.run_shell_command(
                ["kubectl", "get", "namespace", "composer-system"],
                log_command=False,
                log_error=False,
            )
            self.composer_system_namespace_exists = True
        except Exception:
            self.composer_system_namespace_exists = False
        if self.composer_system_namespace_exists:
            raise Exception(
                "'composer-system' namespace has been detected in your GKE cluster. "
                "It means that your environment is newer than this script. Please "
                "check if newer version of this script is available."
            )

    def _check_cloud_sql_proxy(self: typing.Any) -> None:
        """Sets sql proxy."""
        namespace = (
            "composer-system" if self.composer_system_namespace_exists else "default"
        )
        self.sql_proxy = f"airflow-sqlproxy-service.{namespace}.svc.cluster.local"
        logger.info(
            "composer-system %s -> sql proxy: %s",
            "exists" if self.composer_system_namespace_exists else "does not exist",
            self.sql_proxy,
        )

    def _check_drs_and_select_db_storage_bucket(self: typing.Any) -> None:
        """Checks if the environment is DRS-compliant."""
        logger.info("*** Checking if DRS is enabled...")
        self.is_drs_enabled = False
        bucket_name_prefix = self.cp_bucket_name[: -len("-bucket")]
        agent_bucket_name = f"{bucket_name_prefix}-agent"
        try:
            EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                f"gsutil ls gs://{agent_bucket_name}",
                log_command=False,
                log_error=False,
            )
            self.is_drs_enabled = True
            logger.info(
                "%s bucket has been found -> DRS is enabled.", agent_bucket_name
            )
        except Exception as e:  # pylint: disable=broad-except
            logger.info(
                "%s bucket has not been found -> DRS is disabled. (%s)",
                agent_bucket_name,
                e,
            )
        if self.is_drs_enabled:
            self.gcs_bucket_name = agent_bucket_name
        logger.info("Bucket in customer project:  %s.", self.cp_bucket_name)
        logger.info("Bucket accessible from tenant project:  %s.", self.gcs_bucket_name)


class DatabaseImporter(DatabasePorter):
    """Handles import of Airflow database from CSV files."""

    EXPECTED_AIRFLOW_DATABASE_VERSION = "POSTGRES_13"
    DATABASE_CREATION_JOB_IMAGE_VERSION = "1.10.14"
    DATABASE_CREATION_JOB_IMAGE_TAG = "cloud_composer_service_2021-03-07-RC1"

    def __init__(
        self: typing.Any,
        project_name: str,
        environment_name: str,
        location: str,
        fernet_key_file: str,
    ) -> None:
        super().__init__(DatabaseImporter.EXPECTED_AIRFLOW_DATABASE_VERSION)
        self.project_name = project_name
        self.environment_name = environment_name
        self.location = location
        self.fernet_key_file = fernet_key_file

    def _read_source_fernet_key(self: typing.Any) -> None:
        """Reads fernet key from source environment."""
        with open(self.fernet_key_file, mode="r") as file:
            self.fernet_key_from_source_environment = file.read().strip()

    def _fail_fast_if_path_is_not_available(self: typing.Any, path: str) -> None:
        """Fails if given path is not available in the bucket in CP."""
        command = f"gsutil ls gs://{self.cp_bucket_name}{path}"
        EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )

    def _fail_fast_if_there_are_no_files_to_import(self: typing.Any) -> None:
        """Fails if import files do not exist..."""
        logger.info(
            "Checking if required files exist in the bucket: %s.", self.cp_bucket_name
        )
        self._fail_fast_if_path_is_not_available("/import/tables")
        for table_name, _, _ in tables:
            self._fail_fast_if_path_is_not_available(f"/import/tables/{table_name}.csv")
        self._fail_fast_if_path_is_not_available("/import/dirs")

    def _cloud_storage_path_to_imported_table(self: typing.Any, table: str) -> None:
        """Translates table name into a path to CSV file."""
        return f"gs://{self.gcs_bucket_name}/import/tables/{table}.csv"

    def _copy_csv_files_to_tp_if_drs_is_enabled(self: typing.Any) -> None:
        """Copies CSV files to tenant project if DRS is enabled."""
        if self.is_drs_enabled:
            logger.info("*** Copying CSV files to tenant project...")
            command = (
                f"gsutil -m cp -r gs://{self.cp_bucket_name}/import/tables/* "
                f"gs://{self.gcs_bucket_name}/import/tables"
            )
            output = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )
            logger.info(output)

    def _create_new_database(self: typing.Any) -> None:
        """Creates new database in target environment."""
        logger.info("*** Creating new database...")
        self.temporary_database_name = f"temporary-database-{self.unique_id}"
        EnvironmentUtils.create_database_through_exising_workload(
            self.worker_pod_namespace,
            self.worker_pod_name,
            "airflow-worker",
            self.sql_instance_name,
            self.tenant_project_name,
            self.temporary_database_name,
        )

    def _get_image_for_db_creation_job(self: typing.Any) -> None:
        """Gets suitable image to generate a new database with 1.10.14 schema."""
        logger.info("Checking airflow-worker image in existing worker pod...")
        ar_path = re.compile(
            "[a-z-]+.pkg.dev/cloud-airflow-releaser/"
            "(airflow-worker-scheduler-[0-9-]+)/"
            "airflow-worker-scheduler-[0-9-]+:(.*)"
        )
        gcr_path = re.compile(
            "[a-z.]*gcr.io/cloud-airflow-releaser/"
            "(airflow-worker-scheduler-[0-9.]+):(.*)"
        )
        for container in self.worker_pod_desc["spec"]["containers"]:
            container_image = container["image"]
            logger.info("  Checking %s...", container_image)
            if ar_path.match(container_image):
                image, tag = ar_path.match(container_image).groups()
                image_version = (
                    DatabaseImporter.DATABASE_CREATION_JOB_IMAGE_VERSION.replace(
                        ".", "-"
                    )
                )
                new_image = f"airflow-worker-scheduler-{image_version}"
                image = container_image.replace(image, new_image).replace(
                    tag, DatabaseImporter.DATABASE_CREATION_JOB_IMAGE_TAG
                )
                break
            elif gcr_path.match(container_image):
                image, tag = gcr_path.match(container_image).groups()
                new_image = (
                    "airflow-worker-scheduler"
                    f"-{DatabaseImporter.DATABASE_CREATION_JOB_IMAGE_VERSION}"
                )
                image = container_image.replace(image, new_image).replace(
                    tag, DatabaseImporter.DATABASE_CREATION_JOB_IMAGE_TAG
                )
                break
        else:
            raise Exception(
                "Could not find any Airflow worker container in worker pod."
            )
        logger.info(
            "The following image will be used for database " "initialization: %s.",
            image,
        )
        return image

    def _initialize_new_database(self: typing.Any) -> None:
        """Creates a new database with a schema consistent with Airflow 1.10.14."""
        logger.info("*** Setting up new database...")
        EnvironmentUtils.run_database_creation_workload_for_source_version(
            self.worker_pod_namespace,
            self._get_image_for_db_creation_job(),
            self.gcs_bucket_name,
            self.temporary_database_name,
            self.project_name,
            self.unique_id,
            self.sql_proxy,
        )
        logger.info("Waiting for job completion...")
        Command.run_shell_command(
            [
                "kubectl",
                "wait",
                "--for=condition=complete",
                "--timeout=300s",
                f"job/airflow-database-init-job-{self.unique_id}",
                "-n",
                self.worker_pod_namespace,
            ]
        )

    def _clean_prepopulated_tables(self: typing.Any) -> None:
        """Removes default entries from the new database to avoid key collision."""
        logger.info(
            "*** Removing automatically created entries in the new " "database..."
        )
        for table in [
            "alembic_version",
            "chart",
            "connection",
            "job",
            "known_event_type",
            "kube_resource_version",
            "kube_worker_uuid",
            "serialized_dag",
            "slot_pool",
            "task_instance",
        ]:
            logger.info('*** Removing entries from the table "%s"...', table)
            output = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                "psql postgres://root:${SQL_PASSWORD}"
                f"@{self.sql_proxy}/{self.temporary_database_name} "
                f"-p 3306 -t -c 'DELETE FROM {table};'",
            )
            logger.info(output)

    def _import_tables(self: typing.Any) -> None:
        """Imports CSV files to temporary database."""
        logger.info("*** Importing tables...")
        for table, _, _ in tables:
            logger.info('*** Importing table "%s"...', table)
            command = (
                f"gcloud sql import csv {self.sql_instance_name} "
                f"{self._cloud_storage_path_to_imported_table(table)} "
                f"--database={self.temporary_database_name} "
                f"--project {self.tenant_project_name} "
                f"--table={table} -q --async"
            )
            operation_id = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )
            logger.info('*** Waiting for table "%s" to be imported...', table)
            command = (
                f"gcloud sql operations wait {operation_id} --timeout=3600 "
                f"--project {self.tenant_project_name}"
            )
            EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )

    def _rotate_fernet_key(self: typing.Any) -> None:
        """Rotates fernet key used to encrypt the secrets in the database."""
        logger.info("*** Rotating fernet key in the new database...")
        command = (
            "export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://"
            "${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:3306"
            f"/{self.temporary_database_name} && "
            "export AIRFLOW__CORE__FERNET_KEY="
            f"{self.fernet_key},{self.fernet_key_from_source_environment} "
            "&& airflow rotate-fernet-key"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
            log_command=False,
        )
        logger.info(output)

    def _fix_sequence_numbers_in_db(self: typing.Any) -> None:
        """Fixes sequence numbers used to generate sequential keys in the db."""
        logger.info("*** Fixing sequence numbers for primary keys...")
        for table, columns, fix_sequence_numbers in tables:
            if fix_sequence_numbers:
                logger.info('Fixing sequence numbers for table "%s"...', table)
                key = columns[0]
                command = (
                    "psql postgres://root:${SQL_PASSWORD}@"
                    f"{self.sql_proxy}/{self.temporary_database_name} -p 3306 -t -c "
                    f"\"SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('{table}', "
                    f"'{key}')), (SELECT (MAX({key}) + 1) FROM {table}), FALSE);\""
                )
                output = EnvironmentUtils.execute_command_in_a_pod(
                    self.worker_pod_namespace,
                    self.worker_pod_name,
                    self.worker_container_name,
                    command,
                )
                logger.info(output)

    def _apply_migrations(self: typing.Any) -> None:
        """Applies database migrations (1.10.15->2.0.1) to the new database."""
        logger.info("*** Applying migrations...")
        command = (
            "export "
            "AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2:"
            "//${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:3306/{self.temporary_database_name} "
            "&& airflow db upgrade"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _delete_old_database(self: typing.Any) -> None:
        """Deletes empty database created with the environment."""
        logger.info(
            "*** Deleting empty database created with the environment (%s)...",
            self.sql_database,
        )
        try:
            output = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                "psql postgres://root:${SQL_PASSWORD}"
                f"@{self.sql_proxy}/postgres -p 3306 -t -c "
                f"'drop database \"{self.sql_database}\" WITH (FORCE);'",
            )
            logger.info(output)
        except Command.CommandExecutionError:
            logger.warning(
                "Deleting empty database failed, but trying to proceed anyway. "
                "If the database does not exist, the database transfer might still "
                "succeed."
            )

    def _import_dags_plugins_and_data(self: typing.Any) -> None:
        """Imports DAGs, plugins and data."""
        logger.info("Importing DAGs, plugins and data...")
        command = (
            f"gsutil -m cp -r gs://{self.cp_bucket_name}/import/dirs/* "
            f"gs://{self.cp_bucket_name}"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _switch_database_to_the_new_one(self: typing.Any) -> None:
        """Renames the new database to match name configured in the environment."""
        logger.info("*** Switching to the new database...")
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            "psql postgres://root:${SQL_PASSWORD}"
            f"@{self.sql_proxy}/postgres -p 3306 -t -c "
            f'\'ALTER DATABASE "{self.temporary_database_name}" '
            f'RENAME TO "{self.sql_database}";\'',
        )
        logger.info(output)

    def import_database(self: typing.Any) -> None:
        """Imports database from CSV files in environment's bucket."""
        self._check_environment()
        self._read_source_fernet_key()
        self._fail_fast_if_there_are_no_files_to_import()
        self._grant_permissions()
        self._copy_csv_files_to_tp_if_drs_is_enabled()
        self._create_new_database()
        self._initialize_new_database()
        self._clean_prepopulated_tables()
        self._import_tables()
        self._revoke_permissions()
        self._fix_sequence_numbers_in_db()
        self._apply_migrations()
        self._rotate_fernet_key()
        self._delete_old_database()
        self._import_dags_plugins_and_data()
        self._switch_database_to_the_new_one()
        self._remove_temporary_kubeconfig()
        logger.info("*** Database transfer completed.")


class DatabaseExporter(DatabasePorter):
    """Handles export of Airflow database to CSV files."""

    EXPECTED_AIRFLOW_DATABASE_VERSION = "MYSQL_5_7"

    WHAT_TO_DO_NEXT = """\
Exported database, DAGs, plugins and data are now stored in
gs://{cp_bucket_name}/export.
You may now copy exported files to the target environment, e.g. with:
gsutil -m cp -r gs://{cp_bucket_name}/export gs://[TARGET ENV BUCKET NAME]/import

Once the files are copied, you may import the data through
python3 composer_db_transfer.py import ...
"""

    def __init__(
        self: typing.Any,
        project_name: str,
        environment_name: str,
        location: str,
        fernet_key_file: str,
    ) -> None:
        super().__init__(DatabaseExporter.EXPECTED_AIRFLOW_DATABASE_VERSION)
        self.project_name = project_name
        self.environment_name = environment_name
        self.location = location
        self.fernet_key_file = fernet_key_file

    def _cloud_storage_path_to_exported_table(self: typing.Any, table: str) -> str:
        """Translates table name into a path to CSV file in a bucket."""
        return f"gs://{self.gcs_bucket_name}/export/tables/{table}.csv"

    def _mounted_path_to_exported_table(self: typing.Any, table: str) -> str:
        """Translates table name into a path to CSV file available in worker pod."""
        return f"/home/airflow/gcsfuse/export/tables/{table}.csv"

    def _export_table_to_csv_with_custom_query(
        self: typing.Any, table: str, select_query: str
    ) -> None:
        """Exports a given table to CSV file through provided SELECT query."""
        logger.info("Exporting table %s...", table)
        command = (
            f"gcloud sql export csv {self.sql_instance_name} "
            f"{self._cloud_storage_path_to_exported_table(table)} "
            f"--database={self.sql_database} --project {self.tenant_project_name} "
            f"'--query={select_query}'"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _post_process_exported_table(self: typing.Any, table: str) -> None:
        """Performs post processing of exported CSV files."""
        logger.info("Postprocessing exported table: %s...", table)
        command = (
            f"sed -e s/'\"{DatabaseUtils.null_string}\"'//g "
            f"-i {self._mounted_path_to_exported_table(table)}"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _export_tables(self: typing.Any) -> None:
        """Exports all tables to CSV files in the environment's bucket."""
        logger.info("Exporting tables...")
        for table, columns, _ in tables:
            columns_expression = ", ".join(columns)
            select_query = f"SELECT {columns_expression} from {table};"
            self._export_table_to_csv_with_custom_query(table, select_query)

    def _postprocess_tables(self: typing.Any) -> None:
        """Performs postprocessing of exported tables."""
        logger.info("Exporting tables...")
        for table, _, _ in tables:
            self._post_process_exported_table(table)

    def _copy_csv_files_to_cp_if_drs_is_enabled(self: typing.Any) -> None:
        """Copies CSV files to customer's project if DRS is enabled."""
        if self.is_drs_enabled:
            logger.info("*** Copying CSV files to customer's project...")
            command = (
                f"gsutil -m cp -r gs://{self.gcs_bucket_name}/export/tables/* "
                f"gs://{self.cp_bucket_name}/export/tables"
            )
            output = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )
            logger.info(output)

    def _export_dags_plugins_and_data(self: typing.Any) -> None:
        """Exports DAGs, plugins and data."""
        logger.info("Exporting DAGs, plugins and data...")
        bucket = self.cp_bucket_name
        command = (
            f"gsutil -m cp -r gs://{bucket}/dags "
            f"gs://{bucket}/export/dirs/dags && "
            f"gsutil -m cp -r gs://{bucket}/plugins "
            f"gs://{bucket}/export/dirs/plugins"
            f" && gsutil -m cp -r gs://{bucket}/data "
            f"gs://{bucket}/export/dirs/data"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _save_fernet_key(self: typing.Any) -> None:
        logger.info("Saving fernet key to the file: %s", self.fernet_key_file)
        with open(self.fernet_key_file, "w") as file:
            file.write(self.fernet_key)

    def _let_them_know_about_next_steps(self: typing.Any) -> None:
        """Prints guidance about next steps to the log."""
        logger.info("*** Database export completed.")
        logger.info(
            "%s",
            DatabaseExporter.WHAT_TO_DO_NEXT.format(cp_bucket_name=self.cp_bucket_name),
        )

    def export_database(self: typing.Any) -> None:
        """Exports the database to CSV files in the environment's bucket."""
        self._check_environment()
        self._grant_permissions()
        self._export_tables()
        self._revoke_permissions()
        self._copy_csv_files_to_cp_if_drs_is_enabled()
        self._postprocess_tables()
        self._export_dags_plugins_and_data()
        self._remove_temporary_kubeconfig()
        self._save_fernet_key()
        self._let_them_know_about_next_steps()


class ComposerDatabaseMigration:
    """Triggers selected operation (import/export)."""

    @staticmethod
    def export_database(
        project_name: str, environment_name: str, location: str, fernet_key_file: str
    ) -> None:
        """Exports Airflow database to the bucket in customer's project."""
        database_importer = DatabaseExporter(
            project_name, environment_name, location, fernet_key_file
        )
        database_importer.export_database()

    @staticmethod
    def import_database(
        project_name: str, environment_name: str, location: str, fernet_key_file: str
    ) -> None:
        """Imports Airflow database from the bucket in customer's project."""
        database_importer = DatabaseImporter(
            project_name, environment_name, location, fernet_key_file
        )
        database_importer.import_database()

    @staticmethod
    def trigger_operation(
        operation: str,
        project: str,
        environment: str,
        location: str,
        fernet_key_file: str,
    ) -> None:
        """Triggers selected operation (import/export)."""
        logger.info("Database migration script for Cloud Composer")
        if operation == "export":
            ComposerDatabaseMigration.export_database(
                project, environment, location, fernet_key_file
            )
        elif operation == "import":
            ComposerDatabaseMigration.import_database(
                project, environment, location, fernet_key_file
            )
        else:
            logger.error("Operation %s is not supported.", operation)

    @staticmethod
    def main(
        operation: str,
        project: str,
        environment: str,
        location: str,
        fernet_key_file: str,
    ) -> None:
        logger.info("Database transfer tool for Cloud Composer v.%s", SCRIPT_VERSION)
        try:
            ComposerDatabaseMigration.trigger_operation(
                operation, project, environment, location, fernet_key_file
            )
            exit(0)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(
                "*** Operation %s failed due to the following error:\n\n%s\n\n",
                operation,
                e,
            )
            logger.info(
                'Check "Troubleshooting" section of the script manual for '
                "troubleshooting guidance."
            )
            exit(1)


def parse_arguments() -> typing.Dict[typing.Any, typing.Any]:
    """Parses command line parameters."""
    argument_parser = argparse.ArgumentParser(
        usage=f"Database transfer tool for Cloud Composer v.{SCRIPT_VERSION}.\n\n"
        + USAGE
        + "\n"
    )
    argument_parser.add_argument("operation", type=str, choices=["import", "export"])
    argument_parser.add_argument("--project", type=str, required=True)
    argument_parser.add_argument("--environment", type=str, required=True)
    argument_parser.add_argument("--location", type=str, required=True)
    argument_parser.add_argument("--fernet-key-file", type=str, required=True)
    return argument_parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    ComposerDatabaseMigration.main(
        args.operation,
        args.project,
        args.environment,
        args.location,
        args.fernet_key_file,
    )
