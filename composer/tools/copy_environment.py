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

# [START composer_copy_environment]
"""Script to create a copy of an existing Cloud Composer Environment.

Creates a clone of a Composer Environment, copying Environment Configurations,
DAGs/data/plugins/logs, and DAG run history. This script can be useful when
migrating to new Cloud Composer releases.

To use:
* Upload to cloudshell
* Run
    `python copy_environment.py PROJECT LOCATION EXISTING_ENV_NAME NEW_ENV_NAME
    [--running_as_service_account]`
"""
from __future__ import print_function

import argparse
import ast
import base64
import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

from cryptography import fernet
import google.auth
from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient import discovery, errors
from kubernetes import client, config
from mysql import connector
import six
from six.moves import configparser

DEFAULT_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Clone a composer environment."
    )
    parser.add_argument(
        "project",
        help="Google Cloud Project containing existing Composer Environment.",
    )
    parser.add_argument(
        "location",
        help="Google Cloud region containing existing Composer Environment. "
        "For example `us-central1`.",
    )
    parser.add_argument(
        "existing_env_name",
        help="The name of the existing Composer Environment.",
    )
    parser.add_argument(
        "new_env_name",
        help="The name to use for the new Composer Environment.",
    )
    parser.add_argument(
        "--running_as_service_account",
        action="store_true",
        help="Set this flag if the script is running on a VM with same "
        "service account as used in the Composer Environment. This avoids "
        "creating extra credentials.",
    )
    parser.add_argument(
        "--override_machine_type",
        default=None,
        help="Optional. Overrides machine type used for Cloud Composer "
        "Environment. Must be a fully specified machine type URI.",
    )
    parser.add_argument(
        "--override_disk_size_gb",
        type=int,
        default=0,
        help="Optional. Overrides the disk size in GB used for Cloud Composer "
        "Environment.",
    )
    parser.add_argument(
        "--override_network",
        default=None,
        help="Optional. Overrides the network used for Cloud Composer "
        "Environment.",
    )
    parser.add_argument(
        "--override_subnetwork",
        default=None,
        help="Optional. Overrides the subnetwork used for Cloud Composer "
        "Environment.",
    )
    return parser.parse_args()


def get_composer_env(composer_client, project_id, location, name):
    request = (
        composer_client.projects()
        .locations()
        .environments()
        .get(
            name="projects/{}/locations/{}/environments/{}".format(
                project_id, location, name
            )
        )
    )
    return request.execute()


def wait_composer_operation(
    composer_client, operation_name, exit_on_error=True
):
    while True:
        request = (
            composer_client.projects()
            .locations()
            .operations()
            .get(name=operation_name)
        )
        operation = request.execute()
        if operation.get("done"):
            if operation.get("error"):
                print("Composer Operation Failed: {}".format(str(operation)))
                if exit_on_error:
                    sys.exit(1)
            else:
                print("Composer operation successful.")
            return operation
        time.sleep(10)


def wait_sql_operation(
    sql_client, sql_project, operation_name, exit_on_error=True
):
    while True:
        request = sql_client.operations().get(
            operation=operation_name, project=sql_project
        )
        operation = request.execute()
        if operation.get("status", "") == "DONE":
            if operation.get("error"):
                print("SQL Operation Failed: {}".format(str(operation)))
                if exit_on_error:
                    sys.exit(1)
            else:
                print("SQL operation successful.")
            return operation
        time.sleep(5)


def create_composer_env_if_not_exist(
    composer_client, existing_env, project, location, new_env_name, overrides
):
    existing_config = existing_env.get("config", {})
    existing_node_config = existing_config.get("nodeConfig", {})
    existing_software_config = existing_config.get("softwareConfig", {})

    expected_env = {
        "name": "projects/{}/locations/{}/environments/{}".format(
            project, location, new_env_name
        ),
        "config": {
            "nodeCount": existing_config.get("nodeCount", 0),
            "nodeConfig": {
                "location": existing_node_config.get("location", ""),
                "machineType": overrides["machineType"]
                or existing_node_config.get("machineType", ""),
                "network": overrides["network"]
                or existing_node_config.get("network", ""),
                "subnetwork": overrides["subnetwork"]
                or existing_node_config.get("subnetwork", ""),
                "diskSizeGb": overrides["diskSizeGb"]
                or existing_node_config.get("diskSizeGb", 0),
                "oauthScopes": existing_node_config.get("oauthScopes", []),
                "serviceAccount": existing_node_config.get(
                    "serviceAccount", ""
                ),
                "tags": existing_node_config.get("tags", []),
            },
            "softwareConfig": {
                "airflowConfigOverrides": existing_software_config.get(
                    "airflowConfigOverrides", {}
                ),
                "envVariables": existing_software_config.get(
                    "envVariables", {}
                ),
            },
        },
        "labels": existing_env.get("labels", {}),
    }

    try:
        new_env = get_composer_env(
            composer_client, project, location, new_env_name
        )
        print(
            "Attempting to use existing Composer Environment `{}`. If "
            "Environment was not created using this script, configs may "
            "differ.".format(new_env_name)
        )
        if new_env.get("state") != "RUNNING":
            print("Error: Composer Environment {} is not in a RUNNING state.")
            sys.exit(1)
    except errors.HttpError as error:
        if error.resp.status == 404:
            print(
                "Starting Composer Environment Create Operation. This "
                "takes 20 - 60 mins."
            )
            request = (
                composer_client.projects()
                .locations()
                .environments()
                .create(
                    parent="projects/{}/locations/{}".format(
                        project, location
                    ),
                    body=expected_env,
                )
            )
            operation = request.execute()
            wait_composer_operation(composer_client, operation.get("name"))
        else:
            raise error


def update_pypi_packages(composer_client, existing_env, new_env):
    existing_config = existing_env.get("config", {})
    existing_software_config = existing_config.get("softwareConfig", {})
    if existing_software_config.get(
        "pypiPackages"
    ) and existing_software_config.get("pypiPackages") != new_env.get(
        "config", {}
    ).get(
        "softwareConfig", {}
    ).get(
        "pypiPackages"
    ):
        body = {
            "name": new_env.get("name"),
            "config": {
                "softwareConfig": {
                    "pypiPackages": existing_software_config.get(
                        "pypiPackages", {}
                    )
                }
            },
        }
        print(
            "Starting Composer Update PyPI Packages Operation. This takes "
            "20 - 30 mins"
        )
        request = (
            composer_client.projects()
            .locations()
            .environments()
            .patch(
                name=new_env.get("name"),
                body=body,
                updateMask="config.softwareConfig.pypiPackages",
            )
        )
        operation = request.execute()
        wait_composer_operation(composer_client, operation.get("name"))


def create_service_account_key(iam_client, project, service_account_name):
    service_account_key = (
        iam_client.projects()
        .serviceAccounts()
        .keys()
        .create(
            name="projects/{}/serviceAccounts/{}".format(
                project, service_account_name
            ),
            body={},
        )
        .execute()
    )
    service_account_key_decoded = ast.literal_eval(
        base64.b64decode(service_account_key.get("privateKeyData", ""))
    )
    time.sleep(5)
    return service_account_key_decoded


def create_temp_bucket(storage_client, project):
    # Bucket names need to start with lowercase letter, end with lowercase
    # letter, and contain only lowercase letters, numbers, and dashes
    temp_bucket_name = "temp" + str(uuid.uuid4()) + "a"
    return storage_client.create_bucket(temp_bucket_name, project=project)


def get_sql_project_and_instance(env):
    gke_cluster = env.get("config", {}).get("gkeCluster")
    airflow_uri = env.get("config", {}).get("airflowUri")
    sql_project = re.match(
        "https://([^.]*).appspot.com", airflow_uri
    ).groups()[0]
    sql_instance = (
        re.match(
            "projects/[^/]*/zones/[^/]*/clusters/([^/]*)", gke_cluster
        ).groups()[0][:-3]
        + "sql"
    )
    return sql_project, sql_instance


def get_sql_instance_service_account(sql_client, project, instance):
    return (
        sql_client.instances()
        .get(project=project, instance=instance)
        .execute()
        .get("serviceAccountEmailAddress")
    )


def grant_rw_permissions(gcs_bucket, service_account):
    if subprocess.call(
        [
            "gsutil",
            "acl",
            "ch",
            "-u",
            service_account + ":O",
            "gs://" + gcs_bucket.name,
        ]
    ):
        print(
            "Failed to set acls for service account {} on bucket {}.".format(
                service_account, gcs_bucket.name
            )
        )
        sys.exit(1)
    time.sleep(5)


def export_data(sql_client, project, instance, gcs_bucket_name, filename):
    operation = (
        sql_client.instances()
        .export(
            project=project,
            instance=instance,
            body={
                "exportContext": {
                    "kind": "sql#exportContext",
                    "fileType": "SQL",
                    "uri": "gs://" + gcs_bucket_name + "/" + filename,
                }
            },
        )
        .execute()
    )
    print(
        "Starting to export Cloud SQL database from old Environment. This "
        "takes about 2 mins."
    )
    wait_sql_operation(sql_client, project, operation.get("name"))


def get_fernet_key(composer_env):
    print("Retrieving fernet key for Composer Environment {}.".format(
        composer_env.get('name', '')))
    gke_cluster_resource = composer_env.get("config", {}).get("gkeCluster")
    project_zone_cluster = re.match(
        "projects/([^/]*)/zones/([^/]*)/clusters/([^/]*)", gke_cluster_resource
    ).groups()
    tmp_dir_name = None
    try:
        print("Getting cluster credentials {} to retrieve fernet key.".format(
            gke_cluster_resource))
        tmp_dir_name = tempfile.mkdtemp()
        kubeconfig_file = tmp_dir_name + "/config"
        os.environ["KUBECONFIG"] = kubeconfig_file
        if subprocess.call(
            [
                "gcloud",
                "container",
                "clusters",
                "get-credentials",
                project_zone_cluster[2],
                "--zone",
                project_zone_cluster[1],
                "--project",
                project_zone_cluster[0]
            ]
        ):
            print("Failed to retrieve cluster credentials: {}.".format(
                gke_cluster_resource))
            sys.exit(1)

        kubernetes_client = client.CoreV1Api(
            api_client=config.new_client_from_config(
                config_file=kubeconfig_file))
        airflow_configmap = kubernetes_client.read_namespaced_config_map(
            "airflow-configmap", "default")
        config_str = airflow_configmap.data['airflow.cfg']
        with contextlib.closing(six.StringIO(config_str)) as config_buffer:
            config_parser = configparser.ConfigParser()
            config_parser.readfp(config_buffer)
            return config_parser.get("core", "fernet_key")
    except Exception as exc:
        print("Failed to get fernet key for cluster: {}.".format(str(exc)))
        sys.exit(1)
    finally:
        if tmp_dir_name:
            shutil.rmtree(tmp_dir_name)


def reencrypt_variables_connections(old_fernet_key_str, new_fernet_key_str):
    old_fernet_key = fernet.Fernet(old_fernet_key_str.encode("utf-8"))
    new_fernet_key = fernet.Fernet(new_fernet_key_str.encode("utf-8"))
    db = connector.connect(
        host="127.0.0.1",
        user="root",
        database="airflow-db",
    )
    variable_cursor = db.cursor()
    variable_cursor.execute("SELECT id, val, is_encrypted FROM variable")
    rows = variable_cursor.fetchall()
    for row in rows:
        id = row[0]
        val = row[1]
        is_encrypted = row[2]
        if is_encrypted:
            updated_val = new_fernet_key.encrypt(
                old_fernet_key.decrypt(bytes(val))).decode()
            variable_cursor.execute(
                "UPDATE variable SET val=%s WHERE id=%s", (updated_val, id))
    db.commit()

    conn_cursor = db.cursor()
    conn_cursor.execute(
        "SELECT id, password, extra, is_encrypted, is_extra_encrypted FROM "
        "connection")
    rows = conn_cursor.fetchall()
    for row in rows:
        id = row[0]
        password = row[1]
        extra = row[2]
        is_encrypted = row[3]
        is_extra_encrypted = row[4]
        if is_encrypted:
            updated_password = new_fernet_key.encrypt(
                old_fernet_key.decrypt(bytes(password))).decode()
            conn_cursor.execute(
                "UPDATE connection SET password=%s WHERE id=%s",
                (updated_password, id))
        if is_extra_encrypted:
            updated_extra = new_fernet_key.encrypt(
                old_fernet_key.decrypt(bytes(extra))).decode()
            conn_cursor.execute(
                "UPDATE connection SET extra=%s WHERE id=%s",
                (updated_extra, id))
    db.commit()


def import_data(
    sql_client,
    service_account_key,
    project,
    instance,
    gcs_bucket,
    filename,
    old_fernet_key,
    new_fernet_key
):
    tmp_dir_name = None
    fuse_dir = None
    proxy_subprocess = None
    try:
        print("Locally fusing Cloud Storage bucket to access database dump.")
        tmp_dir_name = tempfile.mkdtemp()
        fuse_dir = tmp_dir_name + "/fuse"
        if subprocess.call(["mkdir", fuse_dir]):
            print("Failed to make temporary subdir {}.".format(fuse_dir))
            sys.exit(1)
        if subprocess.call(["gcsfuse", gcs_bucket, fuse_dir]):
            print(
                "Failed to fuse bucket {} with temp local directory {}".format(
                    gcs_bucket, fuse_dir
                )
            )
            sys.exit(1)
        instance_connection = (
            sql_client.instances()
            .get(project=project, instance=instance)
            .execute()
            .get("connectionName")
        )
        proxy_cmd = [
            "cloud_sql_proxy",
            "-instances=" + instance_connection + "=tcp:3306",
        ]

        if service_account_key:
            key_file = tmp_dir_name + "/key.json"
            fh = open(key_file, "w")
            fh.write(json.dumps(service_account_key))
            fh.close()
            proxy_cmd.append("-credential_file=" + key_file)

        print("Starting proxy to new database.")
        proxy_subprocess = subprocess.Popen(proxy_cmd, close_fds=True)
        time.sleep(2)
        if proxy_subprocess.poll() is not None:
            print(
                "Proxy subprocess failed to start or terminated prematurely."
            )
            sys.exit(1)
        print("Importing database.")
        if subprocess.call(
            ["mysql", "-u", "root", "--host", "127.0.0.1"],
            stdin=open(fuse_dir + "/" + filename),
        ):
            print("Failed to import database.")
            sys.exit(1)
        print("Reencrypting variables and connections.")
        reencrypt_variables_connections(old_fernet_key, new_fernet_key)
        print("Database import succeeded.")
    except Exception as exc:
        print("Failed to copy database: {}".format(str(exc)))
        sys.exit(1)
    finally:
        if proxy_subprocess:
            proxy_subprocess.kill()
        if fuse_dir:
            subprocess.call(["fusermount", "-u", fuse_dir])
        if tmp_dir_name:
            shutil.rmtree(tmp_dir_name)


def delete_service_account_key(
    iam_client, project, service_account_name, service_account_key
):
    iam_client.projects().serviceAccounts().keys().delete(
        name="projects/{}/serviceAccounts/{}/keys/{}".format(
            project,
            service_account_name,
            service_account_key["private_key_id"],
        )
    ).execute()


def delete_bucket(gcs_bucket):
    gcs_bucket.delete(force=True)


def copy_database(project, existing_env, new_env, running_as_service_account):
    print("Starting database transfer.")
    gke_service_account_name = None
    gke_service_account_key = None
    gcs_db_dump_bucket = None
    try:
        # create default creds clients
        default_credentials, _ = google.auth.default(scopes=DEFAULT_SCOPES)
        storage_client = storage.Client(credentials=default_credentials)
        iam_client = discovery.build(
            "iam", "v1", credentials=default_credentials
        )

        # create service account creds sql client
        gke_service_account_name = (
            new_env.get("config", {})
            .get("nodeConfig", {})
            .get("serviceAccount")
        )
        gke_service_account_credentials = None
        # Only the service account used for Composer Environment has access to
        # hidden SQL database. If running in a VM as the service account, use
        # default credentials, otherwise create a key and authenticate as the
        # service account.
        if running_as_service_account:
            gke_service_account_credentials = default_credentials
        else:
            print(
                "Obtaining service account `{}` credentials to access SQL "
                "database.".format(gke_service_account_name)
            )
            gke_service_account_key = create_service_account_key(
                iam_client, project, gke_service_account_name
            )
            gke_service_account_credentials = (
                service_account.Credentials.from_service_account_info(
                    gke_service_account_key
                )
            ).with_scopes(DEFAULT_SCOPES)
        sql_client = discovery.build(
            "sqladmin", "v1beta4", credentials=gke_service_account_credentials
        )

        # create a bucket, export data from existing env to bucket, import data
        # to new env
        print("Creating temporary Cloud Storage bucket for database dump.")
        gcs_db_dump_bucket = create_temp_bucket(storage_client, project)
        prev_sql_project, prev_sql_instance = get_sql_project_and_instance(
            existing_env
        )
        new_sql_project, new_sql_instance = get_sql_project_and_instance(
            new_env
        )

        print("Granting permissions on bucket to enable database dump.")
        grant_rw_permissions(
            gcs_db_dump_bucket,
            get_sql_instance_service_account(
                sql_client, prev_sql_project, prev_sql_instance
            ),
        )
        print("Exporting database from old Environment.")
        export_data(
            sql_client,
            prev_sql_project,
            prev_sql_instance,
            gcs_db_dump_bucket.name,
            "db_dump.sql",
        )
        print("Obtaining fernet keys for Composer Environments.")
        old_fernet_key = get_fernet_key(existing_env)
        new_fernet_key = get_fernet_key(new_env)
        print("Preparing database import to new Environment.")
        import_data(
            sql_client,
            gke_service_account_key,
            new_sql_project,
            new_sql_instance,
            gcs_db_dump_bucket.name,
            "db_dump.sql",
            old_fernet_key,
            new_fernet_key,
        )
    finally:
        if gke_service_account_key:
            print("Deleting temporary service account key.")
            delete_service_account_key(
                iam_client,
                project,
                gke_service_account_name,
                gke_service_account_key,
            )
        if gcs_db_dump_bucket:
            print("Deleting temporary Cloud Storage bucket.")
            delete_bucket(gcs_db_dump_bucket)


def copy_gcs_bucket(existing_env, new_env):
    print("Starting to transfer Cloud Storage artifacts.")
    existing_bucket = existing_env["config"]["dagGcsPrefix"][:-4]
    new_bucket = new_env["config"]["dagGcsPrefix"][:-4]
    for subdir in ["dags", "plugins", "data", "logs"]:
        subprocess.call(
            [
                "gsutil",
                "-m",
                "cp",
                "-r",
                existing_bucket + subdir + "/*",
                new_bucket + subdir,
            ]
        )


def clone_environment(
    project,
    location,
    existing_env_name,
    new_env_name,
    running_as_service_account,
    overrides,
):
    default_credentials, _ = google.auth.default(scopes=DEFAULT_SCOPES)
    composer_client = discovery.build(
        "composer", "v1", credentials=default_credentials
    )

    existing_env = get_composer_env(
        composer_client, project, location, existing_env_name
    )
    create_composer_env_if_not_exist(
        composer_client,
        existing_env,
        project,
        location,
        new_env_name,
        overrides,
    )
    new_env = get_composer_env(
        composer_client, project, location, new_env_name
    )
    update_pypi_packages(composer_client, existing_env, new_env)
    new_env = get_composer_env(
        composer_client, project, location, new_env_name
    )
    copy_database(project, existing_env, new_env, running_as_service_account)
    copy_gcs_bucket(existing_env, new_env)
    print(
        "Composer Environment copy completed. Please check new environment "
        "correctness and delete old Environment to avoid incurring "
        "additional costs."
    )


if __name__ == "__main__":
    args = parse_args()
    clone_environment(
        args.project,
        args.location,
        args.existing_env_name,
        args.new_env_name,
        args.running_as_service_account,
        {
            "machineType": args.override_machine_type,
            "network": args.override_network,
            "subnetwork": args.override_subnetwork,
            "diskSizeGb": args.override_disk_size_gb,
        },
    )

# [END composer_copy_environment]
