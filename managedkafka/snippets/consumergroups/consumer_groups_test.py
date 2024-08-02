# Copyright 2024 Google LLC
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

from unittest import mock
from unittest.mock import MagicMock

import delete_consumer_group
import get_consumer_group
from google.cloud import managedkafka_v1
import list_consumer_groups
import pytest
import update_consumer_group

PROJECT_ID = "test-project-id"
REGION = "us-central1"
CLUSTER_ID = "test-cluster-id"
CONSUMER_GROUP_ID = "test-consumer-group-id"


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.get_consumer_group")
def test_get_consumer_group(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    consumer_group = managedkafka_v1.ConsumerGroup()
    consumer_group.name = managedkafka_v1.ManagedKafkaClient.consumer_group_path(
        PROJECT_ID, REGION, CLUSTER_ID, CONSUMER_GROUP_ID
    )
    mock_method.return_value = consumer_group

    get_consumer_group.get_consumer_group(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        consumer_group_id=CONSUMER_GROUP_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got consumer group" in out
    assert CONSUMER_GROUP_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.update_consumer_group")
def test_update_consumer_group(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    new_partition_offsets = {10: 10}
    topic_path = managedkafka_v1.ManagedKafkaClient.topic_path(
        PROJECT_ID, REGION, CLUSTER_ID, "test-topic-id"
    )
    consumer_group = managedkafka_v1.ConsumerGroup()
    consumer_group.name = managedkafka_v1.ManagedKafkaClient.consumer_group_path(
        PROJECT_ID, REGION, CLUSTER_ID, CONSUMER_GROUP_ID
    )
    topic_metadata = managedkafka_v1.ConsumerTopicMetadata()
    for partition, offset in new_partition_offsets.items():
        partition_metadata = managedkafka_v1.ConsumerPartitionMetadata(offset=offset)
        topic_metadata.partitions = {partition: partition_metadata}
    consumer_group.topics = {
        topic_path: topic_metadata,
    }
    mock_method.return_value = consumer_group

    update_consumer_group.update_consumer_group(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        consumer_group_id=CONSUMER_GROUP_ID,
        topic_path=topic_path,
        partition_offsets=new_partition_offsets,
    )

    out, _ = capsys.readouterr()
    assert "Updated consumer group" in out
    assert topic_path in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.list_consumer_groups")
def test_list_consumer_groups(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    consumer_group = managedkafka_v1.ConsumerGroup()
    consumer_group.name = managedkafka_v1.ManagedKafkaClient.consumer_group_path(
        PROJECT_ID, REGION, CLUSTER_ID, CONSUMER_GROUP_ID
    )
    response = [consumer_group]
    mock_method.return_value = response

    list_consumer_groups.list_consumer_groups(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got consumer group" in out
    assert CONSUMER_GROUP_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.delete_consumer_group")
def test_delete_consumer_group(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    mock_method.return_value = None

    delete_consumer_group.delete_consumer_group(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        consumer_group_id=CONSUMER_GROUP_ID,
    )

    out, _ = capsys.readouterr()
    assert "Deleted consumer group" in out
    mock_method.assert_called_once()
