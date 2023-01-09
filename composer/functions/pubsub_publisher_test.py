# Copyright 2023 Google LLC.
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

import pytest
import mock

import pubsub_publisher


@pytest.fixture()
def dump_request_args():
    class Request:
        args = {"message": "test with args"}
        def get_json(self):
            return self.args

    return Request()


@pytest.fixture()
def dump_request():
    class Request:
        args = None
        def get_json(self):
            return {"message": "test with no args"}

    return Request()

@pytest.fixture()
def dump_request_no_message():
    class Request:
        args = None
        def get_json(self):
            return {"no_message": "test with no message key"}

    return Request()


# Pass None, an input that is not valid request
def test_request_with_none():
    request = None
    with pytest.raises(Exception):
        pubsub_publisher.pubsub_publisher(request)


def test_content_not_found(dump_request_no_message):
    output = "Message content not found! Use 'message' key to specify"
    assert pubsub_publisher.pubsub_publisher(dump_request_no_message) == output, f"The function didn't return '{output}'"


@mock.patch("pubsub_publisher.pubsub_v1.PublisherClient.publish")
@mock.patch("pubsub_publisher.pubsub_v1.PublisherClient.topic_path")
def test_topic_path_args(topic_path, _, dump_request_args):
    pubsub_publisher.pubsub_publisher(dump_request_args)

    topic_path.assert_called_once_with(
        "<PROJECT_ID>",
        "dag-topic-trigger",
    )


@mock.patch("pubsub_publisher.pubsub_v1.PublisherClient.publish")
def test_publish_args(publish, dump_request_args):
    pubsub_publisher.pubsub_publisher(dump_request_args)

    publish.assert_called_once_with(
        "projects/<PROJECT_ID>/topics/dag-topic-trigger",
        dump_request_args.args.get("message").encode("utf-8"),
        message_length=str(len(dump_request_args.args.get("message"))),
    )


@mock.patch("pubsub_publisher.pubsub_v1.PublisherClient.publish")
@mock.patch("pubsub_publisher.pubsub_v1.PublisherClient.topic_path")
def test_topic_path(topic_path, _, dump_request):
    pubsub_publisher.pubsub_publisher(dump_request)

    topic_path.assert_called_once_with(
        "<PROJECT_ID>",
        "dag-topic-trigger",
    )


@mock.patch("pubsub_publisher.pubsub_v1.PublisherClient.publish")
def test_publish(publish, dump_request):
    pubsub_publisher.pubsub_publisher(dump_request)

    publish.assert_called_once_with(
        "projects/<PROJECT_ID>/topics/dag-topic-trigger",
        dump_request.get_json().get("message").encode("utf-8"),
        message_length=str(len(dump_request.get_json().get("message"))),
    )
