# 🚀 Composer DAG Linter & Parsing Profiler

## Overview
This Airflow DAG is a specialized **parsing performance profiler** designed to safeguard and optimize your Google Cloud Composer environment.

When triggered, it offloads the resource-intensive DAG parsing process to a temporary, isolated Kubernetes Pod. Its primary goal is to detect **parsing latency issues** and identify heavy top-level code execution without impacting your environment's workload resources. As a byproduct of this analysis, it also validates DAG integrity and catches syntax errors.

## 🌟 Key Features
* **Isolated Execution:** Offloads parsing logic to a separate Pod, protecting the Scheduler from resource contention and crashes.
* **Top-Level Code Profiling:** Detects DAGs that exceed a configurable parse-time threshold and generates a `cProfile` report to identify the specific calls causing delays (e.g., database connections, heavy imports).
* **Smart Image Detection:** Automatically detects the correct worker image for environments with **extra PyPI packages**, ensuring accurate replication of dependencies and **Airflow overrides**.
    * *Note:* If a "Vanilla" (Default) environment is detected, the task will **Skip** gracefully and request manual configuration.
* **Parallel Processing:** Leverages multiprocessing to analyze the entire DAG repository efficiently.
* **Cross-Environment Diagnostics:** Capable of scanning unstable or crashing environments by running this tool from a separate, stable Composer instance.

---

## ⚙️ Quick Setup

### 1. Installation
Upload both files to your Composer environment's `dags/` folder:
* `dag_linter_kubernetes_pod.py` (The Orchestrator)
* `linter_core.py` (The Logic Script)

### 2. Configuration
Open `dag_linter_kubernetes_pod.py`. The tool automatically detects your bucket and image, but you can configure limits:

| Variable | Description |
| :--- | :--- |
| `_CONFIG_GCS_BUCKET_NAME` | The bucket containing your DAGs/Plugins. Set to `None` for auto-detection. |
| `_CONFIG_POD_IMAGE` | **CRITICAL:** Path to your Composer Worker image. Set to `None` for auto-detection.<br><br>**Manual Retrieval (for Vanilla envs or troubleshooting):**<br>1. Check Cloud Build logs.<br>2. Inspect `airflow-worker` YAML in GKE (`image:` field).<br>3. **Support:** Customers with a valid package can contact Google Cloud Support for assistance. |
| `_CONFIG_POD_DISK_SIZE` | Ephemeral storage size for the Pod (ensure this fits your repo size). |
| `_CONFIG_PARSE_TIME_THRESHOLD_SECONDS` | Time limit before a DAG is flagged as "slow". |

### 3. Execution
Trigger the DAG **`composer_dag_parser_profile`** manually from the Airflow UI.

Check the Task Logs for the **`profile_and_check_linter`** task to view the integrity report and performance profiles.