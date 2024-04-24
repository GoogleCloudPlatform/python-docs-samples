# Copyright 2016 Google Inc. All Rights Reserved.
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


from google.cloud.logging import Client

import usage_guide


def test_logger_usage():
    client = Client()

    to_delete = []
    usage_guide.logger_usage(client, to_delete)

    for item in to_delete:
        usage_guide._backoff_not_found(item.delete)


def test_metric_crud():
    client = Client()

    to_delete = []
    usage_guide.metric_crud(client, to_delete)

    for item in to_delete:
        usage_guide._backoff_not_found(item.delete)


def test_sink_storage():
    client = Client()

    to_delete = []
    usage_guide.sink_storage(client, to_delete)

    for item in to_delete:
        usage_guide._backoff_not_found(item.delete)


def test_sink_bigquery():
    client = Client()

    to_delete = []
    usage_guide.sink_bigquery(client, to_delete)

    for item in to_delete:
        usage_guide._backoff_not_found(item.delete)


def test_sink_pubsub():
    client = Client()

    to_delete = []
    usage_guide.sink_pubsub(client, to_delete)

    for item in to_delete:
        usage_guide._backoff_not_found(item.delete)


def test_logging_handler():
    client = Client()

    usage_guide.logging_handler(client)


def test_setup_logging():
    client = Client()

    usage_guide.setup_logging(client)


def test_client_list_entries():
    client = Client()

    to_delete = []
    usage_guide.client_list_entries(client, to_delete)

    for item in to_delete:
        usage_guide._backoff_not_found(item.delete)


def test_dict_config():
    client = Client()

    usage_guide.logging_dict_config(client)
