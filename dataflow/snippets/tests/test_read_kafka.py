#  Copyright 2024 Google LLC
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

from pathlib import Path
import time
import uuid

import docker

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable

import pytest


BOOTSTRAP_SERVER = 'localhost:9092'
TOPIC_NAME = f'topic-{uuid.uuid4()}'
CONTAINER_IMAGE_NAME = 'kafka-pipeline:1'


@pytest.fixture(scope='module', autouse=True)
def kafka_container() -> None:
    # Start a containerized Kafka server.
    docker_client = docker.from_env()
    container = docker_client.containers.run('apache/kafka:3.7.0', network_mode='host', detach=True)
    try:
        create_topic()
        yield
    finally:
        container.stop()


def create_topic() -> None:
    # Try to create a Kafka topic. We might need to wait for the Kafka service to start.
    for _ in range(1, 10):
        try:
            client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVER)
            topics = []
            topics.append(NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1))
            client.create_topics(topics)
            break
        except NoBrokersAvailable:
            time.sleep(5)


def test_read_from_kafka(tmp_path: Path) -> None:

    file_name_prefix = f'output-{uuid.uuid4()}'
    file_name = f'{tmp_path}/{file_name_prefix}-00000-of-00001.txt'

    # Send some messages to Kafka
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    for i in range(0, 5):
        message = f'event-{i}'
        producer.send(TOPIC_NAME, message.encode())

    # Build a container image for the pipeline.
    client = docker.from_env()
    client.images.build(path='./', tag=CONTAINER_IMAGE_NAME)

    # Run the pipeline.
    client.containers.run(
        image=CONTAINER_IMAGE_NAME,
        command=f'/pipeline/read_kafka.py --output /out/{file_name_prefix} --bootstrap_server {BOOTSTRAP_SERVER} --topic {TOPIC_NAME}',
        volumes=['/var/run/docker.sock:/var/run/docker.sock', f'{tmp_path}/:/out'],
        network_mode='host',
        entrypoint='python')

    # Verify the pipeline wrote the Kafka messages to the output file.
    with open(file_name, 'r') as f:
        text = f.read()
        for i in range(0, 5):
            assert f'event-{i}' in text


if __name__ == "__main__":
    test_read_from_kafka()
