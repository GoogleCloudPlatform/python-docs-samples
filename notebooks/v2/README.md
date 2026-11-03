# Workbench Instance Samples (Notebooks API v2)

This directory contains atomic Python code samples demonstrating how to manage **Workbench instances** using the `google-cloud-notebooks` (`google.cloud.notebooks_v2`) client library.

## Prerequisites

1. Enable the **Notebooks API** (`notebooks.googleapis.com`) in your Google Cloud project:
   ```bash
   gcloud services enable notebooks.googleapis.com
   ```
2. Configure Application Default Credentials (ADC):
   ```bash
   gcloud auth application-default login
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

## Samples

### Core Instance Lifecycle & Read Operations
- [`list_instances.py`](list_instances.py) — Lists Workbench instances in a zone (`notebooks_v2_list_instances`).
- [`get_instance.py`](get_instance.py) — Gets metadata and health state for a Workbench instance (`notebooks_v2_get_instance`).
- [`create_instance.py`](create_instance.py) — Creates a new Workbench instance with default VM settings (`notebooks_v2_create_instance`).
- [`stop_instance.py`](stop_instance.py) — Stops a running Workbench instance (`notebooks_v2_stop_instance`).
- [`start_instance.py`](start_instance.py) — Starts a stopped Workbench instance (`notebooks_v2_start_instance`).
- [`reset_instance.py`](reset_instance.py) — Resets (reboots) a Workbench instance (`notebooks_v2_reset_instance`).
- [`delete_instance.py`](delete_instance.py) — Deletes a Workbench instance (`notebooks_v2_delete_instance`).

### Instance Configuration, Maintenance & Diagnostics
- [`update_instance_machine_type.py`](update_instance_machine_type.py) — Updates the Compute Engine machine type of a stopped Workbench instance (`notebooks_v2_update_instance_machine_type`).
- [`update_instance_metadata.py`](update_instance_metadata.py) — Updates custom metadata keys on a Workbench instance (`notebooks_v2_update_instance_metadata`).
- [`update_instance_shielded_config.py`](update_instance_shielded_config.py) — Updates the Shielded VM configuration on a stopped Workbench instance (`notebooks_v2_update_instance_shielded_config`).
- [`check_instance_upgradability.py`](check_instance_upgradability.py) — Checks whether a Workbench instance can be upgraded (`notebooks_v2_check_instance_upgradability`).
- [`upgrade_instance.py`](upgrade_instance.py) — Upgrades a Workbench instance to the latest environment version (`notebooks_v2_upgrade_instance`).
- [`rollback_instance.py`](rollback_instance.py) — Rolls back a Workbench instance to a previous snapshot and revision (`notebooks_v2_rollback_instance`).
- [`diagnose_instance.py`](diagnose_instance.py) — Runs a diagnostic bundle export to Cloud Storage for a Workbench instance (`notebooks_v2_diagnose_instance`).

### Specialized Creation, Security Blueprint Hardening & Access Control
- [`create_instance_gpu.py`](create_instance_gpu.py) — Creates a GPU-accelerated Workbench instance (`notebooks_v2_create_instance_gpu`).
- [`create_instance_custom_container.py`](create_instance_custom_container.py) — Creates a Workbench instance from a custom container image (`notebooks_v2_create_instance_custom_container`).
- [`create_instance_cmek.py`](create_instance_cmek.py) — Creates a Workbench instance encrypted with a customer-managed encryption key (`notebooks_v2_create_instance_cmek`).
- [`create_instance_confidential.py`](create_instance_confidential.py) — Creates a Shielded VM Workbench instance (`notebooks_v2_create_instance_confidential`).
- [`create_instance_private_vpc.py`](create_instance_private_vpc.py) — Creates a private-IP Workbench instance in a custom VPC network and subnet (`notebooks_v2_create_instance_private_vpc`).
- [`create_instance_single_user.py`](create_instance_single_user.py) — Creates a single-user Workbench instance with a custom least-privilege service account (`notebooks_v2_create_instance_single_user`).
- [`create_instance_hardened.py`](create_instance_hardened.py) — Creates a security-hardened Workbench instance disabling root, downloads, terminal, and public IP (`notebooks_v2_create_instance_hardened`).
- [`get_instance_iam_policy.py`](get_instance_iam_policy.py) — Gets the IAM policy for a Workbench instance (`notebooks_v2_get_instance_iam_policy`).
- [`set_instance_iam_policy.py`](set_instance_iam_policy.py) — Sets an IAM policy binding on a Workbench instance (`notebooks_v2_set_instance_iam_policy`).
- [`test_instance_iam_permissions.py`](test_instance_iam_permissions.py) — Tests IAM permissions on a Workbench instance (`notebooks_v2_test_instance_iam_permissions`).

## Running Tests

```bash
.venv/bin/pip install -r requirements-test.txt
.venv/bin/pytest instances_test.py
```
