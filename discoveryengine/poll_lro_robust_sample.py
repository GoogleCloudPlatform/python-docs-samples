# Copyright 2026 Google LLC
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

"""Robust Long-Running Operation (LRO) polling sample for Agent Search."""

# [START genappbuilder_poll_lro_robust]
import random
import time

from google.cloud import discoveryengine_v1 as discoveryengine
from google.longrunning import operations_pb2


def poll_long_running_operation_robust(
    operation_name: str,
    initial_delay_seconds: float = 5.0,
    max_delay_seconds: float = 60.0,
    backoff_factor: float = 1.5,
    timeout_seconds: float = 600.0,
) -> operations_pb2.Operation:
  """Polls a long-running operation with exponential backoff and error diagnosis.

  Asynchronous operations (e.g., document ingestion, schema updates, data store
  provisioning) often take several minutes. Best practices for reliable polling
  include:
  1. Exponential backoff and jitter to prevent quota exhaustion and rate
  limiting.
  2. Detailed error inspection when `operation.done` is True and
  `operation.error`
     contains failure status details.
  3. Inspecting metadata for partial failure counts and GCS error logs.

  Args:
      operation_name: Full resource name of the operation (e.g.,
        'projects/.../locations/.../operations/...').
      initial_delay_seconds: Starting backoff delay in seconds.
      max_delay_seconds: Maximum backoff delay cap.
      backoff_factor: Multiplier for exponential backoff.
      timeout_seconds: Maximum total duration before raising a TimeoutError.

  Returns:
      The completed operations_pb2.Operation proto.

  Raises:
      TimeoutError: If the operation does not finish within `timeout_seconds`.
      RuntimeError: If the operation finishes with an error status.
  """
  # Use DocumentServiceClient's underlying operations client or OperationsClient
  client = discoveryengine.DocumentServiceClient()
  operations_client = client.transport.operations_client

  start_time = time.time()
  current_delay = initial_delay_seconds
  attempt = 1

  print(f"Starting robust polling for operation: {operation_name}")

  while True:
    elapsed = time.time() - start_time
    if elapsed > timeout_seconds:
      raise TimeoutError(
          f"Operation '{operation_name}' exceeded timeout of {timeout_seconds}"
          " seconds."
      )

    operation = operations_client.get_operation(name=operation_name)

    if operation.done:
      print(f"\n[Attempt {attempt}] Operation completed in {elapsed:.1f}s!")

      # 1. Check for fatal operation error
      if operation.HasField("error") and (
          operation.error.code != 0 or operation.error.message
      ):
        error = operation.error
        raise RuntimeError(
            f"Operation failed with Code {error.code}: {error.message}"
        )

      # 2. Check for operation metadata details
      if operation.HasField("metadata"):
        print("Operation Metadata Details:")
        print(f"  Type: {operation.metadata.type_url}")

      # 3. Check for operation response
      if operation.HasField("response"):
        print("Operation Response:")
        print(f"  Type: {operation.response.type_url}")

      return operation

    print(
        f"[Attempt {attempt} - {elapsed:.1f}s elapsed] Operation still in"
        f" progress... Waiting {current_delay:.1f}s."
    )

    time.sleep(current_delay)

    # Exponential backoff with jitter (+/- 10%)
    jitter = random.uniform(0.9, 1.1)
    current_delay = min(
        current_delay * backoff_factor * jitter, max_delay_seconds
    )
    attempt += 1


# [END genappbuilder_poll_lro_robust]
