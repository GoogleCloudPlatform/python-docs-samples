#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Integration tests for Dataproc samples.

Creates a Dataproc cluster, uploads a pyspark file to Google Cloud Storage,
submits a job to Dataproc that runs the pyspark file, then downloads
the output logs from Cloud Storage and verifies the expected output."""

import os

import submit_job_to_cluster

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
CLUSTER_NAME = "testcluster3"
ZONE = "us-central1-b"


def test_e2e():
    output = submit_job_to_cluster.main(PROJECT, ZONE, CLUSTER_NAME, BUCKET)
    assert b"['Hello,', 'dog', 'elephant', 'panther', 'world!']" in output
