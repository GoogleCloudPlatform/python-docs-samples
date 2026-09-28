# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

import uuid

from google.api_core import exceptions
from google.cloud import storage
import pytest

import storage_create_bucket_ip_filtering
import storage_delete_ip_filtering_rules
import storage_disable_ip_filtering
import storage_enable_ip_filtering
import storage_get_ip_filtering
import storage_list_buckets_ip_filtering


@pytest.fixture
def test_bucket():
    storage_client = storage.Client()
    bucket_name = f"ipfilter-test-{uuid.uuid4().hex[:10]}"
    yield bucket_name
    try:
        bucket = storage_client.get_bucket(bucket_name)
        bucket.delete(force=True)
    except Exception:
        pass


def test_ip_filter_lifecycle(test_bucket, capsys):
    public_range = "0.0.0.0/0"
    project_id = storage.Client().project
    vpc_network = f"projects/{project_id}/global/networks/default"
    vpc_range = "10.0.0.0/24"

    # 1. Create with IP filtering
    try:
        created = storage_create_bucket_ip_filtering.create_bucket_ip_filtering(
            test_bucket, public_range
        )
    except (exceptions.Forbidden, exceptions.BadRequest) as e:
        pytest.skip(f"Skipping test due to insufficient permissions on project: {e}")

    assert created.ip_filter is not None
    assert created.ip_filter.mode == "Disabled"

    # 2. Enable IP filtering
    enabled = storage_enable_ip_filtering.enable_ip_filtering(
        test_bucket, public_range, vpc_network, vpc_range
    )
    assert enabled.ip_filter.mode == "Enabled"

    # 3. Get IP filtering
    fetched = storage_get_ip_filtering.get_ip_filtering(test_bucket)
    assert fetched.mode == "Enabled"

    # 4. Disable IP filtering
    disabled = storage_disable_ip_filtering.disable_ip_filtering(test_bucket)
    assert disabled.ip_filter.mode == "Disabled"

    # 5. Delete IP filtering rules
    modified = storage_delete_ip_filtering_rules.delete_ip_filtering_rules(
        test_bucket,
        public_range_to_delete=public_range,
        vpc_network_to_delete=vpc_network,
    )
    assert (
        public_range
        not in modified.ip_filter.public_network_source.allowed_ip_cidr_ranges
    )
    assert not any(
        v.network == vpc_network for v in modified.ip_filter.vpc_network_sources
    )

    # 6. List buckets with IP filtering
    storage_list_buckets_ip_filtering.list_buckets_ip_filtering()
    out, _ = capsys.readouterr()
    assert test_bucket in out
