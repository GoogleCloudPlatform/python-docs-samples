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

"""Sample Airflow DAG demonstrating TerraformApplyOperator usage in Google Cloud Composer."""

# [START composer_terraform_dag]

from datetime import datetime, timedelta
import os
import sys

from airflow import DAG

# Ensure the local DAG directory is available for module imports
DAG_DIR = os.path.dirname(os.path.abspath(__file__))
if DAG_DIR not in sys.path:
    sys.path.insert(0, DAG_DIR)

from terraform_apply_operator import TerraformApplyOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="composer_terraform_apply_dag",
    default_args=default_args,
    description="Sample DAG executing TerraformApplyOperator to provision Google Cloud infrastructure",
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["terraform", "gcp", "composer"],
) as dag:

    # TODO(developer): Update with your GCP Project ID and desired terraform configuration path
    PROJECT_ID = "your-project-id"
    TERRAFORM_CONFIG_DIR = os.path.join(DAG_DIR, "terraform_sample")

    apply_terraform_infra = TerraformApplyOperator(
        task_id="apply_terraform_infrastructure",
        terraform_dir=TERRAFORM_CONFIG_DIR,
        variables={
            "project_id": PROJECT_ID,
            "bucket_name_prefix": "composer-tf-sample-bucket",
            "location": "US",
        },
        terraform_version="1.5.7",
        auto_approve=True,
    )

# [END composer_terraform_dag]
