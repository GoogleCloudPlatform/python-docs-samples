# Copyright 2016 Google LLC
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

"""Samples embedded in the Usage Guide (docs/usage.rst)

Each example function takes a ``client`` argument (which must be an instance
of :class:`google.cloud.logging.client.Client`) and uses it to perform a task
with the API.

To facilitate running the examples as system tests, each example is also passed
a ``to_delete`` list;  the function adds to the list any objects created which
need to be deleted during teardown.
"""

import os
import time

from google.cloud.logging import Client


def snippet(func):
    """Mark ``func`` as a snippet example function."""
    func._snippet = True
    return func


def _millis():
    return time.time() * 1000


def do_something_with(item):  # pylint: disable=unused-argument
    pass


# pylint: enable=reimported,unused-variable,unused-argument


@snippet
def client_list_entries(client, to_delete):  # pylint: disable=unused-argument
    """List entries via client."""

    # [START client_list_entries_default]
    for entry in client.list_entries():  # API call(s)
        do_something_with(entry)
        # [END client_list_entries_default]
        break

    # [START client_list_entries_filter]
    filter_str = "logName:log_name AND textPayload:simple"
    for entry in client.list_entries(filter_=filter_str):  # API call(s)
        do_something_with(entry)
        # [END client_list_entries_filter]
        break

    # [START client_list_entries_order_by]
    from google.cloud.logging import DESCENDING

    for entry in client.list_entries(order_by=DESCENDING):  # API call(s)
        do_something_with(entry)
        # [END client_list_entries_order_by]
        break


@snippet
def logger_usage(client, to_delete):
    """Logger usage."""
    log_name = "logger_usage_%d" % (_millis())

    # [START logger_create]
    logger = client.logger(log_name)
    # [END logger_create]
    to_delete.append(logger)

    # [START logger_log_text]
    logger.log_text("A simple entry")  # API call
    # [END logger_log_text]

    # [START logger_log_struct]
    logger.log_struct(
        {"message": "My second entry", "weather": "partly cloudy"}
    )  # API call
    # [END logger_log_struct]

    # [START logger_log_resource_text]
    from google.cloud.logging import Resource

    res = Resource(
        type="generic_node",
        labels={
            "location": "us-central1-a",
            "namespace": "default",
            "node_id": "10.10.10.1",
        },
    )
    logger.log_struct(
        {"message": "My first entry", "weather": "partly cloudy"}, resource=res
    )
    # [END logger_log_resource_text]

    # [START logger_list_entries]
    from google.cloud.logging import DESCENDING

    for entry in logger.list_entries(order_by=DESCENDING):  # API call(s)
        do_something_with(entry)
    # [END logger_list_entries]

    def _logger_delete():
        # [START logger_delete]
        logger.delete()  # API call
        # [END logger_delete]

    _backoff_not_found(_logger_delete)
    to_delete.remove(logger)


@snippet
def metric_crud(client, to_delete):
    """Metric CRUD."""
    metric_name = "robots-%d" % (_millis(),)
    description = "Robots all up in your server"
    filter = "logName:apache-access AND textPayload:robot"
    updated_filter = "textPayload:robot"
    updated_description = "Danger, Will Robinson!"

    # [START client_list_metrics]
    for metric in client.list_metrics():  # API call(s)
        do_something_with(metric)
    # [END client_list_metrics]

    # [START metric_create]
    metric = client.metric(metric_name, filter_=filter, description=description)
    assert not metric.exists()  # API call
    metric.create()  # API call
    assert metric.exists()  # API call
    # [END metric_create]
    to_delete.append(metric)

    # [START metric_reload]
    existing_metric = client.metric(metric_name)
    existing_metric.reload()  # API call
    # [END metric_reload]
    assert existing_metric.filter_ == filter
    assert existing_metric.description == description

    # [START metric_update]
    existing_metric.filter_ = updated_filter
    existing_metric.description = updated_description
    existing_metric.update()  # API call
    # [END metric_update]
    existing_metric.reload()
    assert existing_metric.filter_ == updated_filter
    assert existing_metric.description == updated_description

    def _metric_delete():
        # [START metric_delete]
        metric.delete()
        # [END metric_delete]

    _backoff_not_found(_metric_delete)
    to_delete.remove(metric)


def _sink_storage_setup(client):
    from google.cloud import storage

    bucket_name = "sink-storage-%d" % (_millis(),)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    bucket.create()

    # [START sink_bucket_permissions]
    bucket.acl.reload()  # API call
    logs_group = bucket.acl.group("cloud-logs@google.com")
    logs_group.grant_owner()
    bucket.acl.add_entity(logs_group)
    bucket.acl.save()  # API call
    # [END sink_bucket_permissions]

    return bucket


@snippet
def sink_storage(client, to_delete):
    """Sink log entries to storage."""
    bucket = _sink_storage_setup(client)
    to_delete.append(bucket)
    sink_name = "robots-storage-%d" % (_millis(),)
    filter = "textPayload:robot"

    # [START sink_storage_create]
    destination = "storage.googleapis.com/%s" % (bucket.name,)
    sink = client.sink(sink_name, filter_=filter, destination=destination)
    assert not sink.exists()  # API call
    sink.create()  # API call
    assert sink.exists()  # API call
    # [END sink_storage_create]
    to_delete.insert(0, sink)  # delete sink before bucket


def _sink_bigquery_setup(client):
    from google.cloud import bigquery

    dataset_name = "sink_bigquery_%d" % (_millis(),)
    client = bigquery.Client()
    dataset = client.create_dataset(dataset_name)

    # [START sink_dataset_permissions]
    from google.cloud.bigquery.dataset import AccessEntry

    entry_list = dataset.access_entries
    entry_list.append(AccessEntry("WRITER", "groupByEmail", "cloud-logs@google.com"))
    dataset.access_entries = entry_list
    client.update_dataset(dataset, ["access_entries"])  # API call
    # [END sink_dataset_permissions]

    return dataset


@snippet
def sink_bigquery(client, to_delete):
    """Sink log entries to bigquery."""
    dataset = _sink_bigquery_setup(client)
    sink_name = "robots-bigquery-%d" % (_millis(),)
    filter_str = "textPayload:robot"

    # [START sink_bigquery_create]
    destination = "bigquery.googleapis.com%s" % (dataset.path,)
    sink = client.sink(sink_name, filter_=filter_str, destination=destination)
    assert not sink.exists()  # API call
    sink.create()  # API call
    assert sink.exists()  # API call
    # [END sink_bigquery_create]
    to_delete.insert(0, sink)  # delete sink before dataset


def _sink_pubsub_setup(client):
    from google.cloud import pubsub

    client = pubsub.PublisherClient()

    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = "sink-pubsub-%d" % (_millis(),)

    # [START sink_topic_permissions]
    topic_path = client.topic_path(project_id, topic_id)
    topic = client.create_topic(request={"name": topic_path})

    policy = client.get_iam_policy(request={"resource": topic_path})  # API call
    policy.bindings.add(role="roles/owner", members=["group:cloud-logs@google.com"])

    client.set_iam_policy(
        request={"resource": topic_path, "policy": policy}
    )  # API call
    # [END sink_topic_permissions]

    return topic


@snippet
def sink_pubsub(client, to_delete):
    """Sink log entries to pubsub."""
    topic = _sink_pubsub_setup(client)
    sink_name = "robots-pubsub-%d" % (_millis(),)
    filter_str = "logName:apache-access AND textPayload:robot"
    updated_filter = "textPayload:robot"

    # [START sink_pubsub_create]
    destination = "pubsub.googleapis.com/%s" % (topic.name,)
    sink = client.sink(sink_name, filter_=filter_str, destination=destination)
    assert not sink.exists()  # API call
    sink.create()  # API call
    assert sink.exists()  # API call
    # [END sink_pubsub_create]
    created_sink = sink

    # [START client_list_sinks]
    for sink in client.list_sinks():  # API call(s)
        do_something_with(sink)
    # [END client_list_sinks]

    # [START sink_reload]
    existing_sink = client.sink(sink_name)
    existing_sink.reload()
    # [END sink_reload]
    assert existing_sink.filter_ == filter_str
    assert existing_sink.destination == destination

    # [START sink_update]
    existing_sink.filter_ = updated_filter
    existing_sink.update()
    # [END sink_update]
    existing_sink.reload()
    assert existing_sink.filter_ == updated_filter

    sink = created_sink
    # [START sink_delete]
    sink.delete()
    # [END sink_delete]


@snippet
def logging_handler(client):
    # [START create_default_handler]
    import logging

    handler = client.get_default_handler()
    cloud_logger = logging.getLogger("cloudLogger")
    cloud_logger.setLevel(logging.INFO)
    cloud_logger.addHandler(handler)
    cloud_logger.error("bad news")
    # [END create_default_handler]

    # [START create_cloud_handler]
    from google.cloud.logging.handlers import CloudLoggingHandler

    handler = CloudLoggingHandler(client)
    cloud_logger = logging.getLogger("cloudLogger")
    cloud_logger.setLevel(logging.INFO)
    cloud_logger.addHandler(handler)
    cloud_logger.error("bad news")
    # [END create_cloud_handler]

    # [START create_named_handler]
    handler = CloudLoggingHandler(client, name="mycustomlog")
    # [END create_named_handler]


@snippet
def setup_logging(client):
    import logging

    # [START setup_logging]
    client.setup_logging(log_level=logging.INFO)
    # [END setup_logging]

    # [START setup_logging_excludes]
    client.setup_logging(log_level=logging.INFO, excluded_loggers=("werkzeug",))
    # [END setup_logging_excludes]


def _line_no(func):
    return func.__code__.co_firstlineno


def _find_examples():
    funcs = [obj for obj in globals().values() if getattr(obj, "_snippet", False)]
    for func in sorted(funcs, key=_line_no):
        yield func


def _name_and_doc(func):
    return func.__name__, func.__doc__


def _backoff_not_found(deleter):
    from google.cloud.exceptions import NotFound

    timeouts = [1, 2, 4, 8, 16]
    while timeouts:
        try:
            deleter()
        except NotFound:
            time.sleep(timeouts.pop(0))
        else:
            break


def main():
    client = Client()
    for example in _find_examples():
        to_delete = []
        print("%-25s: %s" % _name_and_doc(example))
        try:
            example(client, to_delete)
        except AssertionError as failure:
            print("   FAIL: %s" % (failure,))
        except Exception as error:  # pylint: disable=broad-except
            print("  ERROR: %r" % (error,))
        for item in to_delete:
            _backoff_not_found(item.delete)


if __name__ == "__main__":
    main()
