# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud.dns import ManagedZone

import pytest

from conftest import delay_rerun
from get_zone import get_zone


@pytest.mark.flaky(max_runs=3, min_passes=1, rerun_filter=delay_rerun)
def test_get_zone(
    zone: ManagedZone, project_id: str, zone_name: str,
    zone_dns_name: str, zone_description: str
) -> None:
    zone = get_zone(project_id, zone_name)

    assert zone.name == zone_name
    assert zone.dns_name == zone_dns_name
    assert zone.description == zone_description
