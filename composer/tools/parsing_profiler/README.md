# 🚀 Composer DAG Linter & Parsing Profiler

## Overview
This Airflow DAG provides an **on-demand performance profiling** tool for your DAG parsing logic, designed to help you optimize your Google Cloud Composer environment.

When triggered, it executes a **one-off** analysis inside an isolated Kubernetes Pod. This mimics the standard parsing process but runs independently, ensuring that **parsing latency** and resource-heavy **top-level code** can be identified without interrupting your environment's normal operations. Additionally, it validates DAG integrity and detects syntax errors.

## 🌟 Key Features
* **Isolated Execution:** Executes the diagnostic parsing logic in a dedicated Pod to ensure no resource contention with your live environment.
* **Top-Level Code Profiling:** Detects DAGs that exceed a configurable parse-time threshold and generates a `cProfile` report to identify the specific calls causing delays (e.g., database connections, heavy imports).
* **Smart Image Detection:** Automatically detects the correct worker image for environments with **extra PyPI packages**, ensuring accurate replication of dependencies.
    * *Note:* If a "Vanilla" (Default) environment is detected, the task will **Skip** gracefully and request manual configuration.
* **Parallel Processing:** Leverages multiprocessing to analyze the entire DAG repository efficiently.
* **Cross-Environment Diagnostics:** Capable of scanning unstable or crashing environments by running this tool from a separate, stable Composer instance.

---

## ⚙️ Quick Setup

### 1. Installation
Upload both files to your Composer environment's `dags/` folder:
* `dag_linter_kubernetes_pod.py` (The Orchestrator)
* `linter_core.py` (The Logic Script)

> **Note:** The orchestrator expects `linter_core.py` to be in the **same directory** as the DAG file.

### 2. Configuration
Open `dag_linter_kubernetes_pod.py`. The tool automatically detects your bucket and image, but you can configure limits:

| Variable | Description |
| :--- | :--- |
| `_CONFIG_GCS_BUCKET_NAME` | The bucket containing your DAGs/Plugins. Set to `None` for auto-detection. |
| `_CONFIG_POD_IMAGE` | **CRITICAL:** Path to your Composer Worker image. Set to `None` for auto-detection.<br><br>**Manual Retrieval Options (for Vanilla or Cross Environment):**<br>**Option 1: Cloud Build Logs (Composer 2 & 3)**<br>Check the logs of the most recent successful build in Cloud Build.<br>**Option 2: GKE Workloads (Composer 2 Only)**<br>Navigate to Environment's GKE > Workloads > airflow-worker > YAML tab and look for `image:` under the 'spec.containers' section.<br>**Option 3: Customer Support**<br>Customers with a valid support package can contact Google Cloud Support for assistance. |
| `_CONFIG_POD_DISK_SIZE` | Ephemeral storage size for the Pod (ensure this fits your repo size). |
| `_CONFIG_PARSE_TIME_THRESHOLD_SECONDS` | Time limit before a DAG is flagged as "slow". |

#### ⚠️ Cross-Environment Diagnostics (Advanced)
If you are using this tool in a **Stable** environment to debug a **different** environment, you must set `_CONFIG_GCS_BUCKET_NAME` and `_CONFIG_POD_IMAGE` manually.

**Strict Prerequisites:**
1.  **Same Service Project:** Both environments must reside in the same Service Project.
2.  **Same Service Account:** The Stable environment must run as the **same Service Account** as the target environment to ensure correct IAM permissions for GCP resources.
3.  **Same Major Version:** You must troubleshoot Composer 2 with Composer 2, or Composer 3 with Composer 3.

### 3. Execution
Trigger the DAG **`composer_dag_parser_profile`** manually from the Airflow UI.

Check the Task Logs for the **`profile_and_check_linter`** task to view the integrity report and performance profiles.