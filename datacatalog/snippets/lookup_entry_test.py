#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import lookup_entry

BIGQUERY_PROJECT = "bigquery-public-data"
BIGQUERY_DATASET = "new_york_taxi_trips"
BIGQUERY_TABLE = "taxi_zone_geom"

PUBSUB_PROJECT = "pubsub-public-data"
PUBSUB_TOPIC = "taxirides-realtime"


def test_lookup_entry(capsys):
    override_values = {
        "bigquery_project_id": BIGQUERY_PROJECT,
        "dataset_id": BIGQUERY_DATASET,
        "table_id": BIGQUERY_TABLE,
        "pubsub_project_id": PUBSUB_PROJECT,
        "topic_id": PUBSUB_TOPIC,
    }
    dataset_resource = f"//bigquery.googleapis.com/projects/{BIGQUERY_PROJECT}/datasets/{BIGQUERY_DATASET}"
    table_resource = f"//bigquery.googleapis.com/projects/{BIGQUERY_PROJECT}/datasets/{BIGQUERY_DATASET}/tables/{BIGQUERY_TABLE}"
    topic_resource = (
        f"//pubsub.googleapis.com/projects/{PUBSUB_PROJECT}/topics/{PUBSUB_TOPIC}"
    )
    lookup_entry.lookup_entry(override_values)
    out, err = capsys.readouterr()
    assert re.search(
        f"(Retrieved entry .+ for BigQuery Dataset resource {dataset_resource})", out
    )
    assert re.search(
        f"(Retrieved entry .+ for BigQuery Table resource {table_resource})", out
    )
    assert re.search(
        f"(Retrieved entry .+ for Pub/Sub Topic resource {topic_resource})", out
    )
