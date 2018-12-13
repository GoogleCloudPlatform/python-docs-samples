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

import os
import time

from google.cloud import bigquery
import pytest
try:
    import IPython
    from IPython.testing import tools
    from IPython.terminal import interactiveshell
except ImportError:  # pragma: NO COVER
    IPython = None


@pytest.fixture
def temp_dataset():
    client = bigquery.Client()
    dataset_id = "temp_dataset_{}".format(int(time.time() * 1000))
    dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
    dataset = client.create_dataset(bigquery.Dataset(dataset_ref))
    yield dataset
    client.delete_dataset(dataset, delete_contents=True)


@pytest.fixture(scope='session')
def ipython():
    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = interactiveshell.TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture()
def ipython_interactive(request, ipython):
    """Activate IPython's builtin hooks

    for the duration of the test scope.
    """
    with ipython.builtin_trap:
        yield ipython


@pytest.fixture
def to_delete():
    from google.cloud import bigquery
    client = bigquery.Client()
    doomed = []
    yield doomed
    for dataset_id in doomed:
        dataset = bigquery.Dataset.from_string(
            '{}.{}'.format(client.project, dataset_id))
        client.delete_dataset(dataset, delete_contents=True)


def _set_up_ipython():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    return ip


def _strip_region_tags(sample_text):
    """Remove blank lines and region tags from sample text"""
    magic_lines = [line for line in sample_text.split('\n')
                   if len(line) > 0 and '# [' not in line]
    return '\n'.join(magic_lines)


def _run_magic_sample(sample, ip):
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.


@pytest.mark.skipif(IPython is None, reason="Requires `ipython`")
def test_query_magic(ipython):
    ip = _set_up_ipython()

    # Datalab sample
    """
    # [START bigquery_migration_datalab_query_magic]
    %%bq
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY word
    ORDER BY count ASC
    # [END bigquery_migration_datalab_query_magic]
    """

    sample = """
    # [START bigquery_migration_client_library_query_magic]
    %%bigquery
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY word
    ORDER BY count ASC
    # [END bigquery_migration_client_library_query_magic]
    """
    _run_magic_sample(sample, ip)


@pytest.mark.skipif(IPython is None, reason="Requires `ipython`")
def test_query_magic_results_variable(ipython):
    ip = _set_up_ipython()

    # Datalab sample
    """
    # [START bigquery_migration_datalab_query_magic_results_variable]
    %%bq --name my_variable
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY word
    ORDER BY count ASC
    # [END bigquery_migration_datalab_query_magic_results_variable]
    """

    sample = """
    # [START bigquery_migration_client_library_query_magic_results_variable]
    %%bigquery my_variable
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY word
    ORDER BY count ASC
    # [END bigquery_migration_client_library_query_magic_results_variable]
    """
    _run_magic_sample(sample, ip)


@pytest.mark.skipif(IPython is None, reason="Requires `ipython`")
def test_query_magic_parameterized_query(ipython):
    ip = _set_up_ipython()

    # Datalab samples
    """
    # [START bigquery_migration_datalab_magic_parameterized_query_define]
    %%bq query -n my_variable
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = @corpus_name
    GROUP BY word
    ORDER BY count ASC
    # [END bigquery_migration_datalab_magic_parameterized_query_define]

    # [START bigquery_migration_datalab_magic_parameterized_query_execute]
    %%bq execute -q endpoint_stats
    parameters:
    - name: corpus_name
      type: STRING
      value: hamlet
    # [END bigquery_migration_datalab_magic_parameterized_query_execute]
    """

    sample = """
    # [START bigquery_migration_client_library_magic_parameterized_query_define_parameter]
    params = {"corpus_name": "hamlet"}
    # [END bigquery_migration_client_library_magic_parameterized_query_define_parameter]
    """
    _run_magic_sample(sample, ip)

    sample = """
    # [START bigquery_migration_client_library_magic_parameterized_query]
    %%bigquery my_variable --params $params
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = @corpus_name
    GROUP BY word
    ORDER BY count ASC
    # [END bigquery_migration_client_library_magic_parameterized_query]
    """
    _run_magic_sample(sample, ip)


@pytest.mark.skipif(IPython is None, reason="Requires `ipython`")
def test_command_line_interface(ipython):
    ip = IPython.get_ipython()

    # Datalab sample
    """
    # [START bigquery_migration_datalab_list_tables_magic]
    %bq tables list --dataset bigquery-public-data.samples
    # [END bigquery_migration_datalab_list_tables_magic]
    """

    sample = """
    # [START bigquery_migration_datalab_list_tables_magic]
    !bq ls bigquery-public-data:samples
    # [END bigquery_migration_datalab_list_tables_magic]
    """
    _run_magic_sample(sample, ip)

    sample = """
    # [START bigquery_migration_command_line_help]
    !bq help
    # [END bigquery_migration_command_line_help]
    """
    _run_magic_sample(sample, ip)


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
        csv_options=bq.CSVOptions(skip_leading_rows = 1)
    )  # Waits for the job to complete
    # [END bigquery_migration_datalab_load_table_from_gcs_csv]

    assert table.length == 50


def test_client_library_load_table_from_gcs_csv(to_delete):
    # [START bigquery_migration_client_library_load_table_from_gcs_csv]
    from google.cloud import bigquery
    client = bigquery.Client()

    # Create the dataset
    dataset_id = 'import_sample'
    # [END bigquery_migration_client_library_load_table_from_gcs_csv]
    # Use unique dataset ID to avoid collisions when running tests
    dataset_id = 'test_dataset_{}'.format(int(time.time() * 1000))
    to_delete.append(dataset_id)
    # [START bigquery_migration_client_library_load_table_from_gcs_csv]
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = 'US'
    client.create_dataset(dataset)

    # Create the table
    job_config = bigquery.LoadJobConfig(
        schema = [
            bigquery.SchemaField('name', 'STRING'),
            bigquery.SchemaField('post_abbr', 'STRING')
        ],
        skip_leading_rows = 1,
        # The source format defaults to CSV, so the line below is optional.
        source_format = bigquery.SourceFormat.CSV
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
    table = bq.Table('{}.monty_python'.format(dataset_id)).create(schema=schema)
    table.insert(dataframe)  # Starts steaming insert of data
    # [END bigquery_migration_datalab_load_table_from_dataframe]
    # The Datalab library uses tabledata().insertAll() to load data from
    # pandas DataFrames to tables. Because it can take a long time for the rows
    # to be available in the table, this test does not assert on the number of
    # rows in the destination table after the job is run. If errors are
    # encountered during the insertion, this test will fail.
    # See https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability


def test_client_library_load_table_from_dataframe(to_delete):
    # [START bigquery_migration_client_library_load_table_from_dataframe]
    from google.cloud import bigquery
    import pandas

    client = bigquery.Client()

    dataset_id = 'import_sample'
    # [END bigquery_migration_client_library_load_table_from_dataframe]
    # Use unique dataset ID to avoid collisions when running tests
    dataset_id = 'test_dataset_{}'.format(int(time.time() * 1000))
    to_delete.append(dataset_id)
    # [START bigquery_migration_client_library_load_table_from_dataframe]
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = 'US'
    client.create_dataset(dataset)

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
    load_job = client.load_table_from_dataframe(
        dataframe, dataset.table('monty_python'), location='US')
    load_job.result()  # Waits for table load to complete.
    # [END bigquery_migration_client_library_load_table_from_dataframe]

    table = client.get_table(dataset.table('monty_python'))
    assert table.num_rows == 4

