# Terraform Operator Sample for Managed Service for Apache Airflow

This sample demonstrates how to run a Terraform configuration on an Airflow worker in [Managed Service for Apache Airflow (formerly Cloud Composer)](https://cloud.google.com/composer). The sample applies Terraform configuration from the specified sub-directory in the DAGs folder and streams real-time logs.

## Files

- `../terraform_apply_operator.py`: Custom Airflow operator that downloads or uses a provided Terraform binary, stages `.tf` files to an isolated local container path (to avoid Cloud Storage FUSE locking issues), and streams real-time logs.
- `../terraform_dag.py`: Example Airflow DAG invoking `TerraformApplyOperator`.
- `../terraform_dag_test.py`: DAG validation tests.
- `../terraform_apply_operator_test.py`: Unit tests for the operator.
- `main.tf`: Example Terraform configuration that provisions a Cloud Storage bucket with labels.

## Execution Approaches & Security

### 1. Provided Binary (Recommended for Private IP Environments)
In Managed Airflow environments with Private IP (no direct internet egress), you can provide a Terraform binary:
- Upload the Linux binary to the environment's `data/` folder in Cloud Storage (e.g., `gs://<your-environment-bucket>/data/binaries/terraform`). This folder is synchronized to `/home/airflow/gcs/data/` across all workers.
- Pass `binary_path="/home/airflow/gcs/data/binaries/terraform"` to `TerraformApplyOperator`.

### 2. Verified Dynamic Download
If no provided binary is configured or found in `PATH`, `TerraformApplyOperator` downloads the official HashiCorp release binary and **cryptographically verifies its SHA-256 checksum** against HashiCorp's signed `SHA256SUMS` manifest before extraction and execution.

### 3. Containerized Alternative
For workloads requiring dedicated execution environments with complex provider dependencies, consider executing Terraform in an isolated container using `GKEStartPodOperator` or `KubernetesPodOperator`.

## Deploying to Managed Airflow

1. Update the `PROJECT_ID` variable in `terraform_dag.py` with your Google Cloud project ID.
2. Copy `terraform_apply_operator.py`, `terraform_dag.py`, and the `terraform_sample/` directory into your environment's `dags/` folder (or sync via Cloud Storage `gs://<your-environment-bucket>/dags/`).
3. Trigger the `composer_terraform_apply_dag` DAG from the Airflow UI or Cloud Console.
