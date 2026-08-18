# Terraform Operator Sample for Cloud Composer

This sample demonstrates how to run Terraform configurations directly within an Apache Airflow DAG in [Cloud Composer](https://cloud.google.com/composer).

## Files

- `../terraform_apply_operator.py`: Custom Airflow operator that downloads the Terraform binary, stages `.tf` files to an isolated local container path (to avoid GCSFuse locking issues), and streams real-time logs.
- `../terraform_dag.py`: Example Airflow DAG invoking `TerraformApplyOperator`.
- `../terraform_dag_test.py`: DAG validation tests.
- `../terraform_apply_operator_test.py`: Unit tests for the operator.
- `main.tf`: Example Terraform configuration that provisions a Google Cloud Storage bucket with labels.

## Prerequisites

1. A Google Cloud project with the Cloud Composer API enabled.
2. A Cloud Composer 2 / 3 environment.
3. IAM permissions: Ensure the Cloud Composer environment service account has appropriate IAM roles (e.g. `roles/storage.admin`) to provision the desired resources.

## Deploying to Cloud Composer

1. Copy `terraform_apply_operator.py`, `terraform_dag.py`, and the `terraform_sample/` directory into your Cloud Composer environment's `dags/` folder (or sync via Cloud Storage `gs://<your-composer-bucket>/dags/`).
2. Update the `PROJECT_ID` variable in `terraform_dag.py` with your GCP project ID.
3. Trigger the `composer_terraform_apply_dag` from the Airflow web UI.
