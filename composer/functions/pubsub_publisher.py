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
""" This Cloud Function example creates Pub/Sub messages.

    Usage: Replace <PROJECT_ID> with the project ID of your project.
"""

# [START composer_pubsub_publisher_function]
from google.cloud import pubsub_v1

project = "<PROJECT_ID>"
topic = "dag-topic-trigger"


def pubsub_publisher(request):
    """Publish message from HTTP request to Pub/Sub topic.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text with message published into Pub/Sub topic
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    print(request_json)
    if request.args and 'message' in request.args:
        data_str = request.args.get('message')
    elif request_json and 'message' in request_json:
        data_str = request_json['message']
    else:
        return "Message content not found! Use 'message' key to specify"

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project, topic)

    # The required data format is a bytestring
    data = data_str.encode("utf-8")
    # When you publish a message, the client returns a future.
    message_length = len(data_str)
    future = publisher.publish(topic_path,
                               data,
                               message_length=str(message_length))
    print(future.result())

    return f"Message {data} with message_length {message_length} published to {topic_path}."
