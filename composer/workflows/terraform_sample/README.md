# Terraform Operator Sample for Cloud Composer

This sample demonstrates how to run Terraform configurations directly within an Apache Airflow DAG in [Cloud Composer](https://cloud.google.com/composer).

## Files

- `../terraform_apply_operator.py`: Custom Airflow operator that downloads the Terraform binary, stages `.tf` files to an isolated local container path (to avoid GCSFuse locking issues), and streams real-time logs.
- `../terraform_dag.py`: Example Airflow DAG invoking `TerraformApplyOperator`.
- `../terraform_dag_test.py`: DAG validation tests.
- `../terraform_apply_operator_test.py`: Unit tests for the operator.
- `main.tf`: Example Terraform configuration that provisions a Google Cloud Storage bucket with labels.

## Execution Approaches & Security

### 1. Pre-installed Binary (Recommended for Private IP Environments)
In enterprise Cloud Composer environments with Private IP (no direct internet egress) or custom worker images, you can provide a pre-installed `terraform` binary:
- Place `terraform` in the system `PATH` (e.g. `/usr/local/bin/terraform`).
- Or pass `binary_path="/opt/bin/terraform"` to `TerraformApplyOperator`.

### 2. Verified Dynamic Download
If no pre-installed binary is detected, `TerraformApplyOperator` downloads the official HashiCorp release binary and **cryptographically verifies its SHA-256 checksum** against HashiCorp's signed `SHA256SUMS` manifest before extraction and execution.

### 3. Containerized Alternative
For workloads requiring dedicated execution environments with complex provider dependencies, consider executing Terraform in an isolated container using `GKEStartPodOperator` or `KubernetesPodOperator`.

## Deploying to Cloud Composer


1. Copy `terraform_apply_operator.py`, `terraform_dag.py`, and the `terraform_sample/` directory into your Cloud Composer environment's `dags/` folder (or sync via Cloud Storage `gs://<your-composer-bucket>/dags/`).
2. Update the `PROJECT_ID` variable in `terraform_dag.py` with your GCP project ID.
3. Trigger the `composer_terraform_apply_dag` from the Airflow web UI.
