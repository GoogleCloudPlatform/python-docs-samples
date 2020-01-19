#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
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

import lookup_entry

BIGQUERY_PROJECT = 'bigquery-public-data'
BIGQUERY_DATASET = 'new_york_taxi_trips'
BIGQUERY_TABLE = 'taxi_zone_geom'

PUBSUB_PROJECT = 'pubsub-public-data'
PUBSUB_TOPIC = 'taxirides-realtime'


def test_lookup_bigquery_dataset():
    assert lookup_entry.lookup_bigquery_dataset(
        BIGQUERY_PROJECT, BIGQUERY_DATASET)


def test_lookup_bigquery_dataset_sql_resource():
    assert lookup_entry.lookup_bigquery_dataset_sql_resource(
        BIGQUERY_PROJECT, BIGQUERY_DATASET)


def test_lookup_bigquery_table():
    assert lookup_entry.lookup_bigquery_table(
        BIGQUERY_PROJECT, BIGQUERY_DATASET, BIGQUERY_TABLE)


def test_lookup_bigquery_table_sql_resource():
    assert lookup_entry.lookup_bigquery_table_sql_resource(
        BIGQUERY_PROJECT, BIGQUERY_DATASET, BIGQUERY_TABLE)


def test_lookup_pubsub_topic():
    assert lookup_entry.lookup_pubsub_topic(PUBSUB_PROJECT, PUBSUB_TOPIC)


def test_lookup_pubsub_topic_sql_resource():
    assert lookup_entry.lookup_pubsub_topic_sql_resource(
        PUBSUB_PROJECT, PUBSUB_TOPIC)
