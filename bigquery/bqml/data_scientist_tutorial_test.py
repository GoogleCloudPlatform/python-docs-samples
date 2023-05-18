# Copyright 2018 Google Inc. All Rights Reserved.
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

import uuid

# [START bqml_data_scientist_tutorial_import_and_client]
from google.cloud import bigquery
# [END bqml_data_scientist_tutorial_import_and_client]
import pytest


# [START bqml_data_scientist_tutorial_import_and_client]
client = bigquery.Client()
# We use a unique dataset ID for this example to avoid collisions with
# other invocations of this tutorial.  In practice, you could leverage
# a persistent dataset and not create/destroy it with each invocation.
dataset_id = f"bqml_tutorial_{str(uuid.uuid4().hex)}"
full_dataset_id = f"{client.project}.{dataset_id}"
# [END bqml_data_scientist_tutorial_import_and_client]


@pytest.fixture
def delete_dataset():
    yield
    client.delete_dataset(full_dataset_id, delete_contents=True)


def test_data_scientist_tutorial(delete_dataset):
    # [START bqml_data_scientist_tutorial_create_dataset]
    dataset = bigquery.Dataset(full_dataset_id)
    dataset.location = 'US'
    client.create_dataset(dataset)
    # [END bqml_data_scientist_tutorial_create_dataset]

    # [START bqml_data_scientist_tutorial_create_model]
    sql = """
        CREATE OR REPLACE MODEL `{}.sample_model`
        OPTIONS(model_type='logistic_reg') AS
        SELECT
            IF(totals.transactions IS NULL, 0, 1) AS label,
            IFNULL(device.operatingSystem, "") AS os,
            device.isMobile AS is_mobile,
            IFNULL(geoNetwork.country, "") AS country,
            IFNULL(totals.pageviews, 0) AS pageviews
        FROM
            `bigquery-public-data.google_analytics_sample.ga_sessions_*`
        WHERE
            _TABLE_SUFFIX BETWEEN '20160801' AND '20170630'
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_data_scientist_tutorial_create_model]

    # [START bqml_data_scientist_tutorial_get_training_statistics]
    sql = """
        SELECT
        *
        FROM
        ML.TRAINING_INFO(MODEL `{}.sample_model`)
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_data_scientist_tutorial_get_training_statistics]

    # [START bqml_data_scientist_tutorial_evaluate_model]
    sql = """
        SELECT
            *
        FROM ML.EVALUATE(MODEL `{}.sample_model`, (
            SELECT
                IF(totals.transactions IS NULL, 0, 1) AS label,
                IFNULL(device.operatingSystem, "") AS os,
                device.isMobile AS is_mobile,
                IFNULL(geoNetwork.country, "") AS country,
                IFNULL(totals.pageviews, 0) AS pageviews
            FROM
                `bigquery-public-data.google_analytics_sample.ga_sessions_*`
            WHERE
                _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_data_scientist_tutorial_evaluate_model]

    # [START bqml_data_scientist_tutorial_predict_transactions]
    sql = """
        SELECT
            country,
            SUM(predicted_label) as total_predicted_purchases
        FROM ML.PREDICT(MODEL `{}.sample_model`, (
            SELECT
                IFNULL(device.operatingSystem, "") AS os,
                device.isMobile AS is_mobile,
                IFNULL(totals.pageviews, 0) AS pageviews,
                IFNULL(geoNetwork.country, "") AS country
            FROM
                `bigquery-public-data.google_analytics_sample.ga_sessions_*`
            WHERE
                _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
            GROUP BY country
            ORDER BY total_predicted_purchases DESC
            LIMIT 10
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_data_scientist_tutorial_predict_transactions]

    # [START bqml_data_scientist_tutorial_predict_purchases]
    sql = """
        SELECT
            fullVisitorId,
            SUM(predicted_label) as total_predicted_purchases
        FROM ML.PREDICT(MODEL `{}.sample_model`, (
            SELECT
                IFNULL(device.operatingSystem, "") AS os,
                device.isMobile AS is_mobile,
                IFNULL(totals.pageviews, 0) AS pageviews,
                IFNULL(geoNetwork.country, "") AS country,
                fullVisitorId
            FROM
                `bigquery-public-data.google_analytics_sample.ga_sessions_*`
            WHERE
                _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
            GROUP BY fullVisitorId
            ORDER BY total_predicted_purchases DESC
            LIMIT 10
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_data_scientist_tutorial_predict_purchases]
