/*

# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


This SQL statement queries difference between bigquery-public-data.ml_datasets.ulb_fraud_detection and test sample view

It uses the row_number to check which rows are in the sample, and leaves the remainder as an output to the query which are then saved to the training view

*/


SELECT
  *
FROM (
  SELECT
    *,
    CAST(ROW_NUMBER() OVER()AS STRING) AS row_number
  FROM
    `bigquery-public-data.ml_datasets.ulb_fraud_detection`) AS a
WHERE
  a.row_number NOT IN (
  SELECT
    row_number
  FROM
    `rp_demo_cmek.ulb_fraud_test_sample_table`)