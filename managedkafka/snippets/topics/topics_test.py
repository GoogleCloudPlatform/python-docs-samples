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

import create_topic
import delete_topic
import get_topic
from google.cloud import managedkafka_v1
import list_topics
import pytest
import update_topic

PROJECT_ID = "test-project-id"
REGION = "us-central1"
CLUSTER_ID = "test-cluster-id"
TOPIC_ID = "test-topic-id"


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.create_topic")
def test_create_topic(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    partition_count = 10
    replication_factor = 3
    configs = {"min.insync.replicas": "1"}
    topic = managedkafka_v1.Topic()
    topic.name = managedkafka_v1.ManagedKafkaClient.topic_path(
        PROJECT_ID, REGION, CLUSTER_ID, TOPIC_ID
    )
    topic.partition_count = partition_count
    topic.replication_factor = replication_factor
    topic.configs = configs
    mock_method.return_value = topic

    create_topic.create_topic(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        topic_id=TOPIC_ID,
        partition_count=partition_count,
        replication_factor=replication_factor,
        configs=configs,
    )

    out, _ = capsys.readouterr()
    assert "Created topic" in out
    assert TOPIC_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.get_topic")
def test_get_topic(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    topic = managedkafka_v1.Topic()
    topic.name = managedkafka_v1.ManagedKafkaClient.topic_path(
        PROJECT_ID, REGION, CLUSTER_ID, TOPIC_ID
    )
    mock_method.return_value = topic

    get_topic.get_topic(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        topic_id=TOPIC_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got topic" in out
    assert TOPIC_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.update_topic")
def test_update_topic(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    new_partition_count = 20
    new_configs = {"min.insync.replicas": "2"}
    topic = managedkafka_v1.Topic()
    topic.name = managedkafka_v1.ManagedKafkaClient.topic_path(
        PROJECT_ID, REGION, CLUSTER_ID, TOPIC_ID
    )
    topic.partition_count
    topic.configs = new_configs
    mock_method.return_value = topic

    update_topic.update_topic(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        topic_id=TOPIC_ID,
        partition_count=new_partition_count,
        configs=new_configs,
    )

    out, _ = capsys.readouterr()
    assert "Updated topic" in out
    assert TOPIC_ID in out
    assert 'min.insync.replicas"\n  value: "2"' in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.list_topics")
def test_list_topics(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    topic = managedkafka_v1.Topic()
    topic.name = managedkafka_v1.ManagedKafkaClient.topic_path(
        PROJECT_ID, REGION, CLUSTER_ID, TOPIC_ID
    )
    response = [topic]
    mock_method.return_value = response

    list_topics.list_topics(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got topic" in out
    assert TOPIC_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.delete_topic")
def test_delete_topic(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    mock_method.return_value = None

    delete_topic.delete_topic(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        topic_id=TOPIC_ID,
    )

    out, _ = capsys.readouterr()
    assert "Deleted topic" in out
    mock_method.assert_called_once()
