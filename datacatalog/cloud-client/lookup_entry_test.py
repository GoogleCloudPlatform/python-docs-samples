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

import os

from gcp_devrel.testing import eventually_consistent

import lookup_entry

PROJECT = os.environ['GCLOUD_PROJECT']
BIGQUERY_DATASET = os.environ['GCLOUD_BIGQUERY_DATASET']
BIGQUERY_TABLE = os.environ['GCLOUD_BIGQUERY_TABLE']
PUBSUB_TOPIC = os.environ['GCLOUD_PUBSUB_TOPIC']


def test_lookup_bigquery_dataset():
    @eventually_consistent.call
    def _():
        assert lookup_entry.lookup_bigquery_dataset(PROJECT, BIGQUERY_DATASET)


def test_lookup_bigquery_table():
    @eventually_consistent.call
    def _():
        assert lookup_entry.lookup_bigquery_table(PROJECT, BIGQUERY_DATASET, BIGQUERY_TABLE)


def test_lookup_pubsub_topic():
    @eventually_consistent.call
    def _():
        assert lookup_entry.lookup_pubsub_topic(PROJECT, PUBSUB_TOPIC)
