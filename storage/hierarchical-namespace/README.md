# GCS HNS Folder Management Scripts

This directory contains scripts for managing folders in Google Cloud Storage
(GCS) Hierarchical Namespace (HNS) enabled buckets.

## Scripts

### `delete_empty_folders.py`

This script recursively deletes empty folders within a specified GCS bucket and
(optional) prefix.

**Features:**

*   **Recursive Deletion:** Traverses and deletes nested empty folders.
*   **Depth-First Deletion:** Deletes the deepest folders first to ensure parent
    folders are empty before deletion attempts.
*   **Parallel Execution:** Uses a thread pool to delete folders concurrently
    for improved performance.
*   **Configurable:** Allows setting the target bucket, folder prefix, and
    number of workers.
*   **Error Handling:** Retries on transient errors and logs failures.
*   **Progress Reporting:** Periodically logs deletion statistics.

**Usage:**

1.  **Authenticate:** `bash gcloud auth application-default login`
2.  **Configure:** Update the variables at the top of the script:
    *   `BUCKET_NAME`: The name of your GCS HNS bucket.
    *   `FOLDER_PREFIX`: (Optional) The prefix to limit deletion scope (e.g.,
        `archive/`). Leave empty to scan the whole bucket. Must end with `/` if
        specified.
    *   `MAX_WORKERS`: Number of concurrent deletion threads.
3.  **Run:** `bash python3 delete_empty_folders.py`

**Note:** This script *only* deletes folders. Folders containing any objects
will not be deleted, and a "Failed Precondition" warning will be logged.
