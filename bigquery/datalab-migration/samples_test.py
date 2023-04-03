# Copyright 2018 Google Inc.
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

import time

from google.api_core.retry import Retry
import google.auth
import google.datalab
import IPython
from IPython.terminal import interactiveshell
from IPython.testing import tools
import pytest

# Get default project
_, PROJECT_ID = google.auth.default()
# Set Datalab project ID
context = google.datalab.Context.default()
context.set_project_id(PROJECT_ID)


@pytest.fixture(scope='session')
def ipython_interactive():
    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = interactiveshell.TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture
def to_delete():
    from google.cloud import bigquery
    client = bigquery.Client()
    doomed = []
    yield doomed
    for dataset_id in doomed:
        dataset = client.get_dataset(dataset_id)
        client.delete_dataset(dataset, delete_contents=True)


def _set_up_ipython(extension):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension(extension)
    return ip


def _strip_region_tags(sample_text):
    """Remove blank lines and region tags from sample text"""
    magic_lines = [line for line in sample_text.split('\n')
                   if len(line) > 0 and '# [' not in line]
    return '\n'.join(magic_lines)


def test_datalab_query_magic(ipython_interactive):
    import google.datalab.bigquery as bq

    ip = _set_up_ipython('google.datalab.kernel')

    sample = """
    # [START bigquery_migration_datalab_query_magic]
    %%bq query
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY word
    ORDER BY count ASC
    LIMIT 100
    # [END bigquery_migration_datalab_query_magic]
    """
    ip.run_cell(_strip_region_tags(sample))

    results = ip.user_ns["_"]  # Last returned object in notebook session
    assert isinstance(results, bq.QueryResultsTable)
    df = results.to_dataframe()
    assert len(df) == 100

@pytest.mark.skip("datalab is deprecated, remove tests in sept 2023")
def test_client_library_query_magic(ipython_interactive):
    import pandas

    ip = _set_up_ipython('google.cloud.bigquery')

    sample = """
    # [START bigquery_migration_client_library_query_magic]
    %%bigquery
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY word
    ORDER BY count ASC
    LIMIT 100
    # [END bigquery_migration_client_library_query_magic]
    """
    ip.run_cell(_strip_region_tags(sample))

    df = ip.user_ns["_"]  # Last returned object in notebook session
    assert isinstance(df, pandas.DataFrame)
    assert len(df) == 100


@pytest.mark.skip("datalab is deprecated, remove tests in sept 2023")
def test_datalab_query_magic_results_variable(ipython_interactive):
    ip = _set_up_ipython('google.datalab.kernel')

    sample = """
    # [START bigquery_migration_datalab_query_magic_define_query]
    %%bq query -n my_query
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = "TX"
    LIMIT 100
    # [END bigquery_migration_datalab_query_magic_define_query]
    """
    ip.run_cell(_strip_region_tags(sample))

    sample = """
    # [START bigquery_migration_datalab_execute_query]
    import google.datalab.bigquery as bq

    my_variable = my_query.execute().result().to_dataframe()
    # [END bigquery_migration_datalab_execute_query]
    """
    ip.run_cell(_strip_region_tags(sample))

    variable_name = "my_variable"
    assert variable_name in ip.user_ns  # verify that variable exists
    my_variable = ip.user_ns[variable_name]
    assert len(my_variable) == 100
    ip.user_ns.pop(variable_name)  # clean up variable


def test_client_library_query_magic_results_variable(ipython_interactive):
    ip = _set_up_ipython('google.cloud.bigquery')

    sample = """
    # [START bigquery_migration_client_library_query_magic_results_variable]
    %%bigquery my_variable
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = "TX"
    LIMIT 100
    # [END bigquery_migration_client_library_query_magic_results_variable]
    """
    ip.run_cell(_strip_region_tags(sample))

    variable_name = "my_variable"
    assert variable_name in ip.user_ns  # verify that variable exists
    my_variable = ip.user_ns[variable_name]
    assert len(my_variable) == 100
    ip.user_ns.pop(variable_name)  # clean up variable


@pytest.mark.skip("datalab is deprecated, remove tests in sept 2023")
def test_datalab_list_tables_magic(ipython_interactive):
    ip = _set_up_ipython('google.datalab.kernel')

    sample = """
    # [START bigquery_migration_datalab_list_tables_magic]
    %bq tables list --dataset bigquery-public-data.samples
    # [END bigquery_migration_datalab_list_tables_magic]
    """
    ip.run_cell(_strip_region_tags(sample))

    # Retrieves last returned object in notebook session
    html_element = ip.user_ns["_"]
    assert "shakespeare" in html_element.data


@pytest.mark.skip("datalab is deprecated, remove tests in sept 2023")
def test_datalab_query():
    # [START bigquery_migration_datalab_query]
    import google.datalab.bigquery as bq

    sql = """
        SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state = "TX"
        LIMIT 100
    """
    df = bq.Query(sql).execute().result().to_dataframe()
    # [END bigquery_migration_datalab_query]

    assert len(df) == 100


def test_client_library_query():
    # [START bigquery_migration_client_library_query]
    from google.cloud import bigquery

    client = bigquery.Client()
    sql = """
        SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state = "TX"
        LIMIT 100
    """
    df = client.query(sql).to_dataframe()
    # [END bigquery_migration_client_library_query]

    assert len(df) == 100


@pytest.mark.skip("datalab is deprecated, remove tests in sept 2023")
def test_datalab_load_table_from_gcs_csv(to_delete):
    # [START bigquery_migration_datalab_load_table_from_gcs_csv]
    import google.datalab.bigquery as bq

    # Create the dataset
    dataset_id = 'import_sample'
    # [END bigquery_migration_datalab_load_table_from_gcs_csv]
    # Use unique dataset ID to avoid collisions when running tests
    dataset_id = 'test_dataset_{}'.format(int(time.time() * 1000))
    to_delete.append(dataset_id)
    # [START bigquery_migration_datalab_load_table_from_gcs_csv]
    bq.Dataset(dataset_id).create()

    # Create the table
    schema = [
        {'name': 'name', 'type': 'STRING'},
        {'name': 'post_abbr', 'type': 'STRING'},
    ]
    table = bq.Table(
        '{}.us_states'.format(dataset_id)).create(schema=schema)
    table.load(
        'gs://cloud-samples-data/bigquery/us-states/us-states.csv',
        mode='append',
        source_format='csv',
        csv_options=bq.CSVOptions(skip_leading_rows=1)
    )  # Waits for the job to complete
    # [END bigquery_migration_datalab_load_table_from_gcs_csv]

    assert table.length == 50


def test_client_library_load_table_from_gcs_csv(to_delete):
    # [START bigquery_migration_client_library_load_table_from_gcs_csv]
    from google.cloud import bigquery

    client = bigquery.Client(location='US')

    # Create the dataset
    dataset_id = 'import_sample'
    # [END bigquery_migration_client_library_load_table_from_gcs_csv]
    # Use unique dataset ID to avoid collisions when running tests
    dataset_id = 'test_dataset_{}'.format(int(time.time() * 1000))
    to_delete.append(dataset_id)
    # [START bigquery_migration_client_library_load_table_from_gcs_csv]
    dataset = client.create_dataset(dataset_id)

    # Create the table
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField('name', 'STRING'),
            bigquery.SchemaField('post_abbr', 'STRING')
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV
    )
    load_job = client.load_table_from_uri(
        'gs://cloud-samples-data/bigquery/us-states/us-states.csv',
        dataset.table('us_states'),
        job_config=job_config
    )
    load_job.result()  # Waits for table load to complete.
    # [END bigquery_migration_client_library_load_table_from_gcs_csv]

    table = client.get_table(dataset.table('us_states'))
    assert table.num_rows == 50


def test_datalab_load_table_from_dataframe(to_delete):
    """ Wrap test with retries to handle transient errors """
    @Retry()
    def datalab_load_table_from_dataframe(to_delete):
        # [START bigquery_migration_datalab_load_table_from_dataframe]
        import google.datalab.bigquery as bq
        import pandas

        # Create the dataset
        dataset_id = 'import_sample'
        # [END bigquery_migration_datalab_load_table_from_dataframe]
        # Use unique dataset ID to avoid collisions when running tests
        dataset_id = 'test_dataset_{}'.format(int(time.time() * 1000))
        to_delete.append(dataset_id)
        # [START bigquery_migration_datalab_load_table_from_dataframe]
        bq.Dataset(dataset_id).create()

        # Create the table and load the data
        dataframe = pandas.DataFrame([
            {'title': 'The Meaning of Life', 'release_year': 1983},
            {'title': 'Monty Python and the Holy Grail', 'release_year': 1975},
            {'title': 'Life of Brian', 'release_year': 1979},
            {
                'title': 'And Now for Something Completely Different',
                'release_year': 1971
            },
        ])
        schema = bq.Schema.from_data(dataframe)
        table = bq.Table(
            '{}.monty_python'.format(dataset_id)).create(schema=schema)
        table.insert(dataframe)  # Starts steaming insert of data
        # [END bigquery_migration_datalab_load_table_from_dataframe]
        # The Datalab library uses tabledata().insertAll() to load data from
        # pandas DataFrames to tables. Because it can take a long time for the rows
        # to be available in the table, this test does not assert on the number of
        # rows in the destination table after the job is run. If errors are
        # encountered during the insertion, this test will fail.
        # See https://cloud.google.com/bigquery/streaming-data-into-bigquery
    datalab_load_table_from_dataframe(to_delete)


def test_client_library_load_table_from_dataframe(to_delete):
    # [START bigquery_migration_client_library_load_table_from_dataframe]
    import pandas
    from google.cloud import bigquery

    client = bigquery.Client(location='US')

    dataset_id = 'import_sample'
    # [END bigquery_migration_client_library_load_table_from_dataframe]
    # Use unique dataset ID to avoid collisions when running tests
    dataset_id = 'test_dataset_{}'.format(int(time.time() * 1000))
    to_delete.append(dataset_id)
    # [START bigquery_migration_client_library_load_table_from_dataframe]
    dataset = client.create_dataset(dataset_id)

    # Create the table and load the data
    dataframe = pandas.DataFrame([
        {'title': 'The Meaning of Life', 'release_year': 1983},
        {'title': 'Monty Python and the Holy Grail', 'release_year': 1975},
        {'title': 'Life of Brian', 'release_year': 1979},
        {
            'title': 'And Now for Something Completely Different',
            'release_year': 1971
        },
    ])
    table_ref = dataset.table('monty_python')
    load_job = client.load_table_from_dataframe(dataframe, table_ref)
    load_job.result()  # Waits for table load to complete.
    # [END bigquery_migration_client_library_load_table_from_dataframe]

    table = client.get_table(table_ref)
    assert table.num_rows == 4
