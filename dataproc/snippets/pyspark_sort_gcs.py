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

""" Sample pyspark script to be uploaded to Cloud Storage and run on
Cloud Dataproc.

Note this file is not intended to be run directly, but run inside a PySpark
environment.

This file demonstrates how to read from a GCS bucket. See README.md for more
information.
"""

# [START dataproc_pyspark_sort_gcs]
import pyspark

sc = pyspark.SparkContext()
rdd = sc.textFile("gs://path-to-your-GCS-file")
print(sorted(rdd.collect()))
# [END dataproc_pyspark_sort_gcs]
