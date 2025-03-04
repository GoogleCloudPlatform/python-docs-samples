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

import pytest

from create_zone import create_zone


@pytest.mark.flaky
def test_create_zone(project_id: str, zone_name: str, zone_dns_name: str, zone_description: str) -> None:
    zone = create_zone(
        project_id, zone_name, zone_dns_name, zone_description
    )

    assert zone.name == zone_name
    assert zone.dns_name == zone_dns_name
    assert zone.description == zone_description
