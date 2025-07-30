# Copyright 2025 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

import concurrent.futures
import logging
import threading
import time

from google.api_core import exceptions as google_exceptions
from google.api_core import retry
from google.cloud import storage_control_v2
import grpc

ThreadPoolExecutor = concurrent.futures.ThreadPoolExecutor

# This script may be used to recursively delete a large number of nested empty
# folders in a GCS HNS bucket. Overview of the algorithm:
# 1. Folder Discovery:
#    - Lists all folders under the BUCKET_NAME and FOLDER_PREFIX (if set).
#    - Partitions all discovered folders into a map, keyed by depth
#      (e.g. {1: [foo1/ foo2/], 2: [foo1/bar1/, foo1/bar2/, foo2/bar3/], ...}
# 2. Folder Deletion:
#    - Processes depths in reverse order (from deepest to shallowest).
#    - For each depth level, submits all folders at that level to a thread pool
#      for parallel deletion.
#    - Only moves to the next depth level once all folders at the current depth
#      have been processed. This ensures that child folders are removed before
#      their parents, respecting hierarhical constraints.
#
# Note: This script only deletes folders, not objects; any folders with child
# objects (immediate or nested) will fail to be deleted.
#
# Usage: See README.md for instructions.

# --- Configuration ---
BUCKET_NAME = "do-not-delete-mabsaleh-hns-test"

# e.g. "archive/old_data/" or "" to delete all folders in the bucket.
# If specified, must end with '/'.
FOLDER_PREFIX = "chain_103/"

# Max number of concurrent threads to use for deleting folders.
MAX_WORKERS = 100

# How often to log statistics during deletion, in seconds.
STATS_REPORT_INTERVAL = 5

# --- Data Structures & Globals ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(threadName)s - %(message)s"
)

# Global map to store folders by their depth
# { depth (int) -> set of full_resource_names (str) }
folders_by_depth = {}

# Stats for monitoring progress
stats = {
    "found_total": 0,
    "successful_deletes": 0,
    "failed_deletes_precondition": 0,
    "failed_deletes_internal": 0,
}
stats_lock = threading.Lock()

# Initialize the Storage Control API client
storage_control_client = storage_control_v2.StorageControlClient()


def _get_simple_path_and_depth(full_resource_name: str) -> tuple[str, int]:
  """Extracts bucket-relative path and depth from a GCS folder resource name.

  The "simple path" is relative to the bucket (e.g., 'archive/logs/' for
  'projects/_/buckets/my-bucket/folders/archive/logs/').

  The "depth" is the number of '/' in the simple path (e.g. 'archive/logs/' is
  depth 2).

  Args:
    full_resource_name: The full resource name of the GCS folder, e.g.,
      'projects/_/buckets/your-bucket-name/folders/path/to/folder/'.

  Returns:
    A tuple (simple_path: str, depth: int).

  Raises:
    ValueError: If the resource name does not match the expected format
      (i.e. start with 'projects/_/buckets/BUCKET_NAME/folders/FOLDER_PREFIX'
      and ends with a trailing slash).
  """
  base_folders_prefix = f"projects/_/buckets/{BUCKET_NAME}/folders/"
  # The full prefix to validate against, including the global FOLDER_PREFIX.
  # If FOLDER_PREFIX is "", this is equivalent to base_folders_prefix.
  expected_validation_prefix = base_folders_prefix + FOLDER_PREFIX

  if not full_resource_name.startswith(
      expected_validation_prefix
  ) or not full_resource_name.endswith("/"):
    raise ValueError(
        f"Folder resource name '{full_resource_name}' does not match expected"
        f" prefix '{expected_validation_prefix}' or missing trailing slash."
    )

  simple_path = full_resource_name[len(base_folders_prefix) :]
  depth = simple_path.count("/")
  if depth < 1:
    raise ValueError(
        f"Folder resource name '{full_resource_name}' has invalid depth"
        f" {depth} (expected at least 1)."
    )
  return simple_path, depth


def discover_and_partition_folders():
  """Discovers all folders in the bucket and partitions them by depth.

  Result is stored in the global folders_by_depth dictionary.
  """
  parent_resource = f"projects/_/buckets/{BUCKET_NAME}"

  logging.info(
      "Starting folder discovery and partitioning for bucket '%s'."
      " Using prefix filter: '%s'.",
      BUCKET_NAME,
      FOLDER_PREFIX if FOLDER_PREFIX else "NONE (all folders)",
  )

  list_folders_request = storage_control_v2.ListFoldersRequest(
      parent=parent_resource, prefix=FOLDER_PREFIX
  )

  num_folders_found = 0
  try:
    for folder in storage_control_client.list_folders(
        request=list_folders_request
    ):
      full_resource_name = folder.name
      _, depth = _get_simple_path_and_depth(full_resource_name)

      if depth not in folders_by_depth:
        folders_by_depth[depth] = set()
      folders_by_depth[depth].add(full_resource_name)

      num_folders_found += 1
      with stats_lock:
        stats["found_total"] = num_folders_found

  except Exception as e:
    logging.error("Failed to list folders: %s", e, exc_info=True)
    return

  logging.info(
      "Finished discovery. Total folders found: %s.", num_folders_found
  )
  if not folders_by_depth:
    logging.info("No folders found in the bucket.")
  else:
    logging.info("Folders partitioned by depth:")
    for depth_val in sorted(folders_by_depth.keys()):
      logging.info(
          "  Depth %s: %s folders", depth_val, len(folders_by_depth[depth_val])
      )


# Defines retriable error codes for the DeleteFolder API call.
def should_retry(exception):
  if not isinstance(
      exception, (google_exceptions.GoogleAPICallError, grpc.RpcError)
  ):
    return False

  # gRPC status codes to retry on, matching the JSON
  retryable_grpc_codes = [
      grpc.StatusCode.RESOURCE_EXHAUSTED,
      grpc.StatusCode.UNAVAILABLE,
      grpc.StatusCode.INTERNAL,
      grpc.StatusCode.UNKNOWN,
  ]

  status_code = None
  if isinstance(exception, google_exceptions.GoogleAPICallError):
    status_code = exception.code
  elif isinstance(exception, grpc.RpcError):
    # For grpc.RpcError, code() returns the status code enum
    status_code = exception.code()

  return status_code in retryable_grpc_codes


def delete_folder(folder_full_resource_name: str):
  """Attempts to delete a single GCS HNS folder.

  Includes retry logic for transient errors.

  Stores stats in the global stats dictionary.

  Args:
      folder_full_resource_name: The full resource name of the GCS folder to
        delete, e.g.,
        'projects/_/buckets/your-bucket-name/folders/path/to/folder/'.
  """
  simple_path, _ = _get_simple_path_and_depth(folder_full_resource_name)

  retry_policy = retry.Retry(
      predicate=should_retry,
      initial=1.0,  # Initial backoff: 1s
      maximum=60.0,  # Max backoff: 60s
      multiplier=2.0,  # Backoff multiplier: 2
      deadline=120.0,  # Total time allowed for all retries and calls
  )

  try:
    request = storage_control_v2.DeleteFolderRequest(
        name=folder_full_resource_name
    )
    storage_control_client.delete_folder(request=request, retry=retry_policy)

    with stats_lock:
      stats["successful_deletes"] += 1
    return  # Success

  except google_exceptions.NotFound:
    # This can happen if the folder was deleted by another process.
    logging.warning(
        "Folder not found for deletion (already gone?): %s", simple_path
    )
    return  # Not a retriable error
  except google_exceptions.FailedPrecondition as e:
    # This typically means the folder contains objects.
    logging.warning("Deletion failed for '%s': %s.", simple_path, e.message)
    with stats_lock:
      stats["failed_deletes_precondition"] += 1
    return  # Not a retriable error
  except Exception as e:
    logging.error(
        "Failed to delete '%s': %s",
        simple_path,
        e,
        exc_info=True,
    )
    with stats_lock:
      stats["failed_deletes_internal"] += 1
    return  # All retries exhausted


# --- STATS REPORTER THREAD ---
def stats_reporter_thread_logic(stop_event: threading.Event, start_time: float):
  """Logs current statistics periodically."""
  logging.info("Stats Reporter: Started.")
  while not stop_event.wait(STATS_REPORT_INTERVAL):
    with stats_lock:
      elapsed = time.time() - start_time
      rate = stats["successful_deletes"] / elapsed if elapsed > 0 else 0
      logging.info(
          "[STATS] Total Folders Found: %s | Successful Deletes: %s | Failed"
          " Deletes (precondition): %s | Failed Deletes (internal): %s | Rate:"
          " %.2f folders/sec",
          stats["found_total"],
          stats["successful_deletes"],
          stats["failed_deletes_precondition"],
          stats["failed_deletes_internal"],
          rate,
      )
  logging.info("Stats Reporter: Shutting down.")


# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
  if BUCKET_NAME == "your-gcs-bucket-name":
    print(
        "\nERROR: Please update the BUCKET_NAME variable in the script before"
        " running."
    )
    exit(1)

  if FOLDER_PREFIX and not FOLDER_PREFIX.endswith("/"):
    print("\nERROR: FOLDER_PREFIX must end with a '/' if specified.")
    exit(1)

  start_time = time.time()

  logging.info("Starting GCS HNS folder deletion for bucket: %s", BUCKET_NAME)

  # Event to signal threads to stop gracefully.
  stop_event = threading.Event()

  # Start the stats reporter thread.
  stats_thread = threading.Thread(
      target=stats_reporter_thread_logic,
      args=(stop_event, start_time),
      name="StatsReporter",
      daemon=True,
  )
  stats_thread.start()

  # Step 1: Discover and Partition Folders.
  discover_and_partition_folders()

  if not folders_by_depth:
    logging.info("No folders found to delete. Exiting.")
    exit(0)

  # Prepare for multi-threaded deletion within each depth level.
  deletion_executor = ThreadPoolExecutor(
      max_workers=MAX_WORKERS, thread_name_prefix="DeleteFolderWorker"
  )

  try:
    # Step 2: Iterate and delete by depth (from max to min).
    sorted_depths = sorted(folders_by_depth.keys(), reverse=True)
    for current_depth in sorted_depths:
      folders_at_current_depth = folders_by_depth.get(current_depth, set())

      if not folders_at_current_depth:
        logging.info(
            "Skipping depth %s: No folders found at this depth.", current_depth
        )
        continue

      logging.info(
          "\nProcessing depth %s: Submitting %s folders for deletion...",
          current_depth,
          len(folders_at_current_depth),
      )

      # Submit deletion tasks to the executor.
      futures = [
          deletion_executor.submit(delete_folder, folder_path)
          for folder_path in folders_at_current_depth
      ]

      # Wait for all tasks at the current depth to complete.
      # This is critical: we must ensure all nested folders are gone before
      # tackling their parents.
      concurrent.futures.wait(futures)

      logging.info(
          "Finished processing all folders at depth %s.", current_depth
      )

  except KeyboardInterrupt:
    logging.info(
        "Main: Keyboard interrupt received. Attempting graceful shutdown..."
    )
  except Exception as e:
    logging.error(
        "An unexpected error occurred in the main loop: %s", e, exc_info=True
    )
  finally:
    # Signal all threads to stop.
    stop_event.set()

    # Shut down deletion executor and wait for any pending tasks to complete.
    logging.info(
        "Main: Shutting down deletion workers. Waiting for any final tasks..."
    )
    deletion_executor.shutdown(wait=True)

    # Wait for the stats reporter to finish.
    if stats_thread.is_alive():
      stats_thread.join(
          timeout=STATS_REPORT_INTERVAL + 2
      )  # Give it a bit more time.

    # Log final statistics.
    final_elapsed_time = time.time() - start_time
    logging.info("\n--- FINAL SUMMARY ---")
    with stats_lock:
      final_rate = (
          stats["successful_deletes"] / final_elapsed_time
          if final_elapsed_time > 0
          else 0
      )
      logging.info(
          "  - Total Folders Found (Initial Scan): %s\n  - Successful Folder"
          " Deletes: %s\n  - Failed Folder Deletes (Precondition): %s\n  -"
          " Failed Folder Deletes (Internal): %s\n  - Total Runtime: %.2f"
          " seconds\n  - Average Deletion Rate: %.2f folders/sec",
          stats["found_total"],
          stats["successful_deletes"],
          stats["failed_deletes_precondition"],
          stats["failed_deletes_internal"],
          final_elapsed_time,
          final_rate,
      )
    logging.info("Script execution finished.")
