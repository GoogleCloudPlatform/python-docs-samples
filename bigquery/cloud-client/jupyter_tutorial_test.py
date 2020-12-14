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
import IPython
from IPython.terminal import interactiveshell
from IPython.testing import tools
import matplotlib
import pytest


# Ignore semicolon lint warning because semicolons are used in notebooks
# flake8: noqa E703


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


def _strip_region_tags(sample_text):
    """Remove blank lines and region tags from sample text"""
    magic_lines = [line for line in sample_text.split('\n')
                   if len(line) > 0 and '# [' not in line]
    return '\n'.join(magic_lines)


def test_jupyter_tutorial(ipython):
    matplotlib.use('agg')
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')

    sample = """
    # [START bigquery_jupyter_magic_gender_by_year]
    %%bigquery
    SELECT
        source_year AS year,
        COUNT(is_male) AS birth_count
    FROM `bigquery-public-data.samples.natality`
    GROUP BY year
    ORDER BY year DESC
    LIMIT 15
    # [END bigquery_jupyter_magic_gender_by_year]
    """
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.

    sample = """
    # [START bigquery_jupyter_magic_gender_by_year_var]
    %%bigquery total_births
    SELECT
        source_year AS year,
        COUNT(is_male) AS birth_count
    FROM `bigquery-public-data.samples.natality`
    GROUP BY year
    ORDER BY year DESC
    LIMIT 15
    # [END bigquery_jupyter_magic_gender_by_year_var]
    """
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.

    if 'total_births' not in ip.user_ns:
        raise AssertionError
    total_births = ip.user_ns['total_births']
    # [START bigquery_jupyter_plot_births_by_year]
    total_births.plot(kind='bar', x='year', y='birth_count');
    # [END bigquery_jupyter_plot_births_by_year]

    sample = """
    # [START bigquery_jupyter_magic_gender_by_weekday]
    %%bigquery births_by_weekday
    SELECT
        wday,
        SUM(CASE WHEN is_male THEN 1 ELSE 0 END) AS male_births,
        SUM(CASE WHEN is_male THEN 0 ELSE 1 END) AS female_births
    FROM `bigquery-public-data.samples.natality`
    WHERE wday IS NOT NULL
    GROUP BY wday
    ORDER BY wday ASC
    # [END bigquery_jupyter_magic_gender_by_weekday]
    """
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.

    if 'births_by_weekday' not in ip.user_ns:
        raise AssertionError
    births_by_weekday = ip.user_ns['births_by_weekday']
    # [START bigquery_jupyter_plot_births_by_weekday]
    births_by_weekday.plot(x='wday');
    # [END bigquery_jupyter_plot_births_by_weekday]

    # [START bigquery_jupyter_import_and_client]
    from google.cloud import bigquery
    client = bigquery.Client()
    # [END bigquery_jupyter_import_and_client]

    # [START bigquery_jupyter_query_plurality_by_year]
    sql = """
    SELECT
        plurality,
        COUNT(1) AS count,
        year
    FROM
        `bigquery-public-data.samples.natality`
    WHERE
        NOT IS_NAN(plurality) AND plurality > 1
    GROUP BY
        plurality, year
    ORDER BY
        count DESC
    """
    df = client.query(sql).to_dataframe()
    df.head()
    # [END bigquery_jupyter_query_plurality_by_year]

    # [START bigquery_jupyter_plot_plurality_by_year]
    pivot_table = df.pivot(index='year', columns='plurality', values='count')
    pivot_table.plot(kind='bar', stacked=True, figsize=(15, 7));
    # [END bigquery_jupyter_plot_plurality_by_year]

    # [START bigquery_jupyter_query_births_by_gestation]
    sql = """
    SELECT
        gestation_weeks,
        COUNT(1) AS count
    FROM
        `bigquery-public-data.samples.natality`
    WHERE
        NOT IS_NAN(gestation_weeks) AND gestation_weeks <> 99
    GROUP BY
        gestation_weeks
    ORDER BY
        gestation_weeks
    """
    df = client.query(sql).to_dataframe()
    # [END bigquery_jupyter_query_births_by_gestation]

    # [START bigquery_jupyter_plot_births_by_gestation]
    ax = df.plot(kind='bar', x='gestation_weeks', y='count', figsize=(15,7))
    ax.set_title('Count of Births by Gestation Weeks')
    ax.set_xlabel('Gestation Weeks')
    ax.set_ylabel('Count');
    # [END bigquery_jupyter_plot_births_by_gestation]
