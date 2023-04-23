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

import io
import os
import uuid

# [START bqml_ncaa_tutorial_import_and_client]
from google.cloud import bigquery
# [END bqml_ncaa_tutorial_import_and_client]
import pytest

# [START bqml_ncaa_tutorial_import_and_client]
client = bigquery.Client()
# We use a unique dataset ID for this example to avoid collisions with
# other invocations of this tutorial.  In practice, you could leverage
# a persistent dataset and not create/destroy it with each invocation.
dataset_id = f"bqml_tutorial_{str(uuid.uuid4().hex)}"
full_dataset_id = f"{client.project}.{dataset_id}"
# [END bqml_ncaa_tutorial_import_and_client]


@pytest.fixture
def delete_dataset():

    yield
    client.delete_dataset(full_dataset_id, delete_contents=True)


def test_ncaa_tutorial(delete_dataset):
    # [START bqml_ncaa_tutorial_create_dataset]
    dataset = bigquery.Dataset(full_dataset_id)
    dataset.location = 'US'
    client.create_dataset(dataset)
    # [END bqml_ncaa_tutorial_create_dataset]

    # Create the tables used by the tutorial
    # Note: the queries are saved to a file. This should be updated to use the
    # saved queries once the library supports running saved queries.
    query_files = ['feature_input_query.sql', 'training_data_query.sql']
    resources_directory = os.path.join(os.path.dirname(__file__), 'resources')
    for fname in query_files:
        query_filepath = os.path.join(
            resources_directory, fname)
        sql = open(query_filepath, encoding='utf-8').read().format(dataset_id)
        client.query(sql).result()

    # [START bqml_ncaa_tutorial_create_model]
    sql = """
        CREATE OR REPLACE MODEL `{0}.ncaa_model`
        OPTIONS (
            model_type='linear_reg',
            max_iteration=50 ) AS
        SELECT
            * EXCEPT (
                game_id, season, scheduled_date,
                total_three_points_made,
                total_three_points_att),
            total_three_points_att as label
        FROM
            `{0}.wide_games`
        WHERE
            # remove the game to predict
            game_id != 'f1063e80-23c7-486b-9a5e-faa52beb2d83'
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_ncaa_tutorial_create_model]

    # [START bqml_ncaa_tutorial_get_training_statistics]
    sql = """
        SELECT
            *
        FROM
            ML.TRAINING_INFO(MODEL `{}.ncaa_model`)
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_ncaa_tutorial_get_training_statistics]

    # [START bqml_ncaa_tutorial_evaluate_model]
    sql = """
        WITH eval_table AS (
            SELECT
                *,
                total_three_points_att AS label
            FROM
                `{0}.wide_games` )
        SELECT
            *
        FROM
            ML.EVALUATE(MODEL `{0}.ncaa_model`,
                TABLE eval_table)
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_ncaa_tutorial_evaluate_model]

    # [START bqml_ncaa_tutorial_predict_outcomes]
    sql = """
        WITH game_to_predict AS (
            SELECT
                *
            FROM
                `{0}.wide_games`
            WHERE
                game_id='f1063e80-23c7-486b-9a5e-faa52beb2d83' )
        SELECT
            truth.game_id AS game_id,
            total_three_points_att,
            predicted_total_three_points_att
        FROM (
            SELECT
                game_id,
                predicted_label AS predicted_total_three_points_att
            FROM
                ML.PREDICT(MODEL `{0}.ncaa_model`,
                table game_to_predict) ) AS predict
        JOIN (
            SELECT
                game_id,
                total_three_points_att AS total_three_points_att
            FROM
                game_to_predict) AS truth
        ON
            predict.game_id = truth.game_id
    """.format(dataset_id)
    df = client.query(sql).to_dataframe()
    print(df)
    # [END bqml_ncaa_tutorial_predict_outcomes]
