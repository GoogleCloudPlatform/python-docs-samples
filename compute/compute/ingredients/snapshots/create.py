#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa
import sys


from google.cloud import compute_v1


# <INGREDIENT create_snapshot>
def create_snapshot(project_id: str, zone: str, disk_name: str, snapshot_name: str) -> compute_v1.Snapshot:
    """
    Create a snapshot of a disk.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone in which is the disk you want to snapshot.
        disk_name: name of the disk you want to snapshot.
        snapshot_name: name of the snapshot to be created.

    Returns:
        The new snapshot instance.
    """
    disk_client = compute_v1.DisksClient()
    disk = disk_client.get(project=project_id, zone=zone, disk=disk_name)
    snapshot = compute_v1.Snapshot()
    snapshot.source_disk = disk.self_link
    snapshot.name = snapshot_name

    snapshot_client = compute_v1.SnapshotsClient()
    operation = snapshot_client.insert_unary(project=project_id, snapshot_resource=snapshot)
    op_client = compute_v1.GlobalOperationsClient()
    operation = op_client.wait(project=project_id, operation=operation.name)

    if operation.error:
        print("Error during snapshot creation:", operation.error, file=sys.stderr)
        raise RuntimeError(operation.error)
    if operation.warnings:
        print("Warnings during snapshot creation:\n", file=sys.stderr)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr)

    return snapshot_client.get(project=project_id, snapshot=snapshot_name)

# </INGREDIENT>
