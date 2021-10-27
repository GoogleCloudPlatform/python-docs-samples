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

This SQL statement queries the bigquery-public-data.ml_datasets.ulb_fraud_detection to get a sample for the test dataset

It uses the FARM FINGERPRINT method and uses the row number as a unique id.

FARM FINGERPRINT allows you to randomly select rows from your BigQuery tables; but at the same time like to ensure you keep getting the same set of rows every time you work with the dataset

We have used inspiration from the following blog - https://datarunsdeep.com.au/blog/flying-beagle/how-consistently-select-randomly-distributed-sample-rows-bigquery-table

The MOD (or modulo) function takes an argument to determine how many equal portions you will end up with. 

5 is chosen because there are ~5 lots of 56,687 rows (equal to 20% for our test sample) in our table of 284807 rows. We want to break the 284807 rows into 5 equally sized lots , of which we will pick one lot of 56,687 random rows. 

The way we pick that lot is to choose a random number between 1 and 5 - in this case 4 (but it could be 1,2,3 or 5) - and filter out every row that is not in this ‘lot number’.

*/

SELECT
  *
FROM (
  SELECT
    *,
    CAST(ROW_NUMBER() OVER() AS STRING ) AS row_number
  FROM
    `bigquery-public-data.ml_datasets.ulb_fraud_detection`)
WHERE
  MOD(ABS(FARM_FINGERPRINT(row_number)), 5) = 4