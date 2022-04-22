#!/usr/bin/env python
# # Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from resource_cleanup_manager import (
    ResourceCleanupManager,
    DatasetResourceCleanupManager,
    EndpointResourceCleanupManager,
    ModelResourceCleanupManager,
)


def run_cleanup_managers(managers: List[ResourceCleanupManager], is_dry_run: bool):
    for manager in managers:
        type_name = manager.type_name

        print(f"Fetching {type_name}'s...")
        resources = manager.list()
        print(f"Found {len(resources)} {type_name}'s")
        for resource in resources:
            if not manager.is_deletable(resource):
                continue

            if is_dry_run:
                resource_name = manager.resource_name(resource)
                print(f"Will delete '{type_name}': {resource_name}")
            else:
                try:
                    manager.delete(resource)
                except Exception as exception:
                    print(exception)


is_dry_run = False

# List of all cleanup managers
managers = [
    DatasetResourceCleanupManager(),
    EndpointResourceCleanupManager(),
    ModelResourceCleanupManager(),
]

run_cleanup_managers(managers=managers, is_dry_run=is_dry_run)
