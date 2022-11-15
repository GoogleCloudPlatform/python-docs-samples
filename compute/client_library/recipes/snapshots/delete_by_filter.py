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

# flake8: noqa

# <REGION compute_snapshot_delete_by_filter>
# <IMPORTS/>

# <INGREDIENT wait_for_extended_operation />

# <INGREDIENT delete_snapshot />

# <INGREDIENT list_snapshots />

def delete_snapshots_by_filter(project_id: str, filter: str):
    """
    Deletes all snapshots in project that meet the filter criteria.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        filter: filter to be applied when looking for snapshots for deletion.
    """
    for snapshot in list_snapshots(project_id, filter):
        delete_snapshot(project_id, snapshot.name)

# </REGION compute_snapshot_delete_by_filter>