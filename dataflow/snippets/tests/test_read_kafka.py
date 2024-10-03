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

from docker import DockerClient
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable

import pytest


BOOTSTRAP_SERVER = 'localhost:9092'
TOPIC_NAMES = ['topic1', 'topic2']
CONTAINER_IMAGE_NAME = 'kafka-pipeline:1'


@pytest.fixture(scope='module')
def docker_client() -> DockerClient:
    # Build a container image for the pipeline.
    client = docker.from_env()
    client.images.build(path='./', tag=CONTAINER_IMAGE_NAME)
    yield client


@pytest.fixture(scope='module', autouse=True)
def kafka_container(docker_client: DockerClient) -> None:
    # Start a containerized Kafka server.
    container = docker_client.containers.run('apache/kafka:3.7.0', network_mode='host', detach=True)
    try:
        create_topics()
        send_messages(TOPIC_NAMES[0])
        send_messages(TOPIC_NAMES[1])
        yield
    finally:
        container.stop()


@pytest.fixture
def file_name_prefix() -> str:
    return f'output-{uuid.uuid4()}'


def create_topics() -> None:
    # Try to create Kafka topics. We might need to wait for the Kafka service to start.
    for _ in range(1, 10):
        try:
            client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVER)
            topics = []
            topics.append(NewTopic(name=TOPIC_NAMES[0], num_partitions=1, replication_factor=1))
            topics.append(NewTopic(name=TOPIC_NAMES[1], num_partitions=1, replication_factor=1))
            client.create_topics(topics)
            break
        except NoBrokersAvailable:
            time.sleep(5)


def send_messages(topic: str) -> None:
    # Send some messages to Kafka
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    for i in range(0, 5):
        message = f'{topic}-{i}'
        producer.send(topic, message.encode())


def verify_output(file_name: str, topic: str) -> None:
    # Verify the pipeline wrote the Kafka messages to the output file.
    with open(file_name, 'r') as f:
        text = f.read()
        for i in range(0, 5):
            assert f'{topic}-{i}' in text


def test_read_kafka(docker_client: DockerClient, tmp_path: Path, file_name_prefix: str) -> None:
    topic = TOPIC_NAMES[0]

    # Run the containerized Dataflow pipeline.
    docker_client.containers.run(
        image=CONTAINER_IMAGE_NAME,
        command=f'/pipeline/read_kafka.py --output /out/{file_name_prefix} --bootstrap_server {BOOTSTRAP_SERVER} --topic {topic}',
        volumes=['/var/run/docker.sock:/var/run/docker.sock', f'{tmp_path}/:/out'],
        network_mode='host',
        entrypoint='python')

    # Verify the pipeline wrote the Kafka messages to the output file.
    verify_output(f'{tmp_path}/{file_name_prefix}-00000-of-00001.txt', topic)


def test_read_kafka_multi_topic(docker_client: DockerClient, tmp_path: Path, file_name_prefix: str) -> None:
    # Run the containerized Dataflow pipeline.
    docker_client.containers.run(
        image=CONTAINER_IMAGE_NAME,
        command=f'/pipeline/read_kafka_multi_topic.py --output /out/{file_name_prefix} --bootstrap_server {BOOTSTRAP_SERVER}',
        volumes=['/var/run/docker.sock:/var/run/docker.sock', f'{tmp_path}/:/out'],
        network_mode='host',
        entrypoint='python')

    # Verify the pipeline wrote the Kafka messages to the output files.
    # This code snippet writes outputs to separate directories based on the topic name.
    for topic in TOPIC_NAMES:
        verify_output(f'{tmp_path}/{file_name_prefix}/{topic}/output-00000-of-00001.txt', topic)
