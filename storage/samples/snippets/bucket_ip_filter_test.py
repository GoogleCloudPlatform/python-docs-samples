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

from unittest.mock import MagicMock, patch
import uuid

from google.api_core import exceptions
from google.cloud import storage
from google.cloud.storage.ip_filter import (
    IPFilter,
    PublicNetworkSource,
    VpcNetworkSource,
)
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
    public_range = "192.0.2.0/24"
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

    # 4. Delete IP filtering rules
    modified = storage_delete_ip_filtering_rules.delete_ip_filtering_rules(
        test_bucket, public_range_to_delete=public_range
    )
    assert (
        public_range
        not in modified.ip_filter.public_network_source.allowed_ip_cidr_ranges
    )

    # 5. Disable IP filtering
    disabled = storage_disable_ip_filtering.disable_ip_filtering(test_bucket)
    assert disabled.ip_filter.mode == "Disabled"

    # 6. List buckets with IP filtering
    storage_list_buckets_ip_filtering.list_buckets_ip_filtering()
    out, _ = capsys.readouterr()
    assert test_bucket in out


def test_create_bucket_ip_filtering_unit():
    with patch("google.cloud.storage.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket
        mock_created = MagicMock()
        mock_created.name = "test-bucket"
        mock_ip_filter = IPFilter()
        mock_ip_filter.mode = "Disabled"
        mock_created.ip_filter = mock_ip_filter
        mock_client.create_bucket.return_value = mock_created

        result = storage_create_bucket_ip_filtering.create_bucket_ip_filtering(
            "test-bucket", "192.0.2.0/24"
        )
        assert result == mock_created
        mock_client.create_bucket.assert_called_once_with(mock_bucket)
        assert mock_bucket.ip_filter.mode == "Disabled"
        assert (
            "192.0.2.0/24"
            in mock_bucket.ip_filter.public_network_source.allowed_ip_cidr_ranges
        )


def test_enable_ip_filtering_unit():
    with patch("google.cloud.storage.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket"
        mock_bucket.ip_filter = None
        mock_client.get_bucket.return_value = mock_bucket

        result = storage_enable_ip_filtering.enable_ip_filtering(
            "test-bucket",
            "192.0.2.0/24",
            "projects/p/global/networks/n",
            "10.0.0.0/24",
        )
        assert result == mock_bucket
        assert mock_bucket.ip_filter.mode == "Enabled"
        assert (
            "192.0.2.0/24"
            in mock_bucket.ip_filter.public_network_source.allowed_ip_cidr_ranges
        )
        assert len(mock_bucket.ip_filter.vpc_network_sources) == 1
        assert (
            mock_bucket.ip_filter.vpc_network_sources[0].network
            == "projects/p/global/networks/n"
        )
        mock_bucket.patch.assert_called_once()

        # Enable again with same network and additional range
        storage_enable_ip_filtering.enable_ip_filtering(
            "test-bucket",
            "192.0.2.0/24",
            "projects/p/global/networks/n",
            "10.0.1.0/24",
        )
        assert (
            "10.0.1.0/24"
            in mock_bucket.ip_filter.vpc_network_sources[0].allowed_ip_cidr_ranges
        )


def test_get_ip_filtering_unit(capsys):
    with patch("google.cloud.storage.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_bucket = MagicMock()
        mock_bucket.ip_filter = None
        mock_client.get_bucket.return_value = mock_bucket

        assert storage_get_ip_filtering.get_ip_filtering("test-bucket") is None
        out, _ = capsys.readouterr()
        assert "Bucket test-bucket has no IP Filter configured." in out

        ip_filter = IPFilter()
        ip_filter.mode = "Enabled"
        ip_filter.public_network_source = PublicNetworkSource(
            allowed_ip_cidr_ranges=["192.0.2.0/24"]
        )
        ip_filter.vpc_network_sources = [
            VpcNetworkSource(
                network="projects/p/global/networks/n",
                allowed_ip_cidr_ranges=["10.0.0.0/24"],
            )
        ]
        mock_bucket.ip_filter = ip_filter

        res = storage_get_ip_filtering.get_ip_filtering("test-bucket")
        assert res == ip_filter
        out, _ = capsys.readouterr()
        assert "Mode: Enabled" in out
        assert "Public CIDR Ranges: ['192.0.2.0/24']" in out
        assert "VPC Network: projects/p/global/networks/n" in out


def test_delete_ip_filtering_rules_unit(capsys):
    with patch("google.cloud.storage.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket"
        mock_bucket.ip_filter = None
        mock_client.get_bucket.return_value = mock_bucket

        # No filter configured
        storage_delete_ip_filtering_rules.delete_ip_filtering_rules("test-bucket")
        out, _ = capsys.readouterr()
        assert "Bucket test-bucket has no IP Filter configuration." in out

        ip_filter = IPFilter()
        ip_filter.public_network_source = PublicNetworkSource(
            allowed_ip_cidr_ranges=["192.0.2.0/24"]
        )
        ip_filter.vpc_network_sources = [
            VpcNetworkSource(
                network="projects/p/global/networks/n",
                allowed_ip_cidr_ranges=["10.0.0.0/24"],
            )
        ]
        mock_bucket.ip_filter = ip_filter

        # Delete existing range and VPC
        storage_delete_ip_filtering_rules.delete_ip_filtering_rules(
            "test-bucket",
            public_range_to_delete="192.0.2.0/24",
            vpc_network_to_delete="projects/p/global/networks/n",
        )
        assert (
            "192.0.2.0/24"
            not in mock_bucket.ip_filter.public_network_source.allowed_ip_cidr_ranges
        )
        assert len(mock_bucket.ip_filter.vpc_network_sources) == 0
        mock_bucket.patch.assert_called_once()

        # Delete non-existent
        mock_bucket.patch.reset_mock()
        storage_delete_ip_filtering_rules.delete_ip_filtering_rules(
            "test-bucket", public_range_to_delete="non-existent"
        )
        mock_bucket.patch.assert_not_called()


def test_disable_ip_filtering_unit(capsys):
    with patch("google.cloud.storage.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket"
        mock_bucket.ip_filter = None
        mock_client.get_bucket.return_value = mock_bucket

        # No IP filter
        storage_disable_ip_filtering.disable_ip_filtering("test-bucket")
        out, _ = capsys.readouterr()
        assert "No IP filter configuration found" in out

        ip_filter = IPFilter()
        ip_filter.mode = "Enabled"
        mock_bucket.ip_filter = ip_filter
        storage_disable_ip_filtering.disable_ip_filtering("test-bucket")
        assert mock_bucket.ip_filter.mode == "Disabled"
        mock_bucket.patch.assert_called_once()


def test_list_buckets_ip_filtering_unit(capsys):
    with patch("google.cloud.storage.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        b1 = MagicMock()
        b1.name = "b1"
        b1.ip_filter = None
        b2 = MagicMock()
        b2.name = "b2"
        f2 = IPFilter()
        f2.mode = "Enabled"
        b2.ip_filter = f2
        mock_client.list_buckets.return_value = [b1, b2]

        storage_list_buckets_ip_filtering.list_buckets_ip_filtering()
        mock_client.list_buckets.assert_called_once_with(projection="full")
        out, _ = capsys.readouterr()
        assert "Bucket: b1, IP Filter Mode: Not Configured" in out
        assert "Bucket: b2, IP Filter Mode: Enabled" in out
