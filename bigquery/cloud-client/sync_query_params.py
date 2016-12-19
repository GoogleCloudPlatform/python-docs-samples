#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

"""Command-line app to perform synchronous queries with parameters in BigQuery.

For more information, see the README.md under /bigquery.

Example invocation:
    $ python sync_query_params.py --use-named-params 'romeoandjuliet' 100
    $ python sync_query_params.py --use-positional-params 'romeoandjuliet' 100
"""

import argparse
import datetime

from google.cloud import bigquery
import pytz


def print_results(query_results):
    """Print the query results by requesting a page at a time."""
    page_token = None

    while True:
        rows, total_rows, page_token = query_results.fetch_data(
            max_results=10,
            page_token=page_token)

        for row in rows:
            print(row)

        if not page_token:
            break


def sync_query_positional_params(corpus, min_word_count):
    client = bigquery.Client()
    query = """SELECT word, word_count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = ?
    AND word_count >= ?
    ORDER BY word_count DESC;
    """
    query_results = client.run_sync_query(
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter(
                # Set the name to None to use positional parameters (? symbol
                # in the query).  Note that you cannot mix named and positional
                # parameters.
                None,
                'STRING',
                corpus),
            bigquery.ScalarQueryParameter(None, 'INT64', min_word_count)))

    # Only standard SQL syntax supports parameters in queries.
    # See: https://cloud.google.com/bigquery/sql-reference/
    query_results.use_legacy_sql = False
    query_results.run()
    print_results(query_results)


def sync_query_named_params(corpus, min_word_count):
    client = bigquery.Client()
    query = """SELECT word, word_count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = @corpus
    AND word_count >= @min_word_count
    ORDER BY word_count DESC;
    """
    query_results = client.run_sync_query(
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter('corpus', 'STRING', corpus),
            bigquery.ScalarQueryParameter(
                'min_word_count',
                'INT64',
                min_word_count)))
    query_results.use_legacy_sql = False
    query_results.run()
    print_results(query_results)


def sync_query_array_params(gender, states):
    client = bigquery.Client()
    query = """SELECT name, sum(number) as count
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE gender = @gender
    AND state IN UNNEST(@states)
    GROUP BY name
    ORDER BY count DESC
    LIMIT 10;
    """
    query_results = client.run_sync_query(
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter('gender', 'STRING', gender),
            bigquery.ArrayQueryParameter('states', 'STRING', states)))
    query_results.use_legacy_sql = False
    query_results.run()
    print_results(query_results)


def sync_query_timestamp_params(year, month, day, hour, minute):
    client = bigquery.Client()
    query = 'SELECT TIMESTAMP_ADD(@ts_value, INTERVAL 1 HOUR);'
    query_results = client.run_sync_query(
        query,
        query_parameters=[
            bigquery.ScalarQueryParameter(
                'ts_value',
                'TIMESTAMP',
                datetime.datetime(
                    year, month, day, hour, minute, tzinfo=pytz.UTC))])
    query_results.use_legacy_sql = False
    query_results.run()
    print_results(query_results)


def sync_query_struct_params(x, y):
    client = bigquery.Client()
    query = 'SELECT @struct_value AS s;'
    query_results = client.run_sync_query(
        query,
        query_parameters=[
            bigquery.StructQueryParameter(
                'struct_value',
                bigquery.ScalarQueryParameter('x', 'INT64', x),
                bigquery.ScalarQueryParameter('y', 'STRING', y))])
    query_results.use_legacy_sql = False
    query_results.run()
    print_results(query_results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='sample', help='samples')
    named_parser = subparsers.add_parser(
        'named',
        help='Run a query with named parameters.')
    named_parser.add_argument(
        'corpus',
        help='Corpus to search from Shakespeare dataset.')
    named_parser.add_argument(
        'min_word_count',
        help='Minimum count of words to query.',
        type=int)
    positional_parser = subparsers.add_parser(
        'positional',
        help='Run a query with positional parameters.')
    positional_parser.add_argument(
        'corpus',
        help='Corpus to search from Shakespeare dataset.')
    positional_parser.add_argument(
        'min_word_count',
        help='Minimum count of words to query.',
        type=int)
    array_parser = subparsers.add_parser(
        'array',
        help='Run a query with an array parameter.')
    array_parser.add_argument(
        'gender',
        choices=['F', 'M'],
        help='Gender of baby in the Social Security baby names database.')
    array_parser.add_argument(
        'states',
        help='U.S. States to consider for popular baby names.',
        nargs='+')
    timestamp_parser = subparsers.add_parser(
        'timestamp',
        help='Run a query with a timestamp parameter.')
    timestamp_parser.add_argument('year', type=int)
    timestamp_parser.add_argument('month', type=int)
    timestamp_parser.add_argument('day', type=int)
    timestamp_parser.add_argument('hour', type=int)
    timestamp_parser.add_argument('minute', type=int)
    struct_parser = subparsers.add_parser(
        'struct',
        help='Run a query with a struct parameter.')
    struct_parser.add_argument('x', help='Integer for x', type=int)
    struct_parser.add_argument('y', help='String for y')
    args = parser.parse_args()

    if args.sample == 'named':
        sync_query_named_params(args.corpus, args.min_word_count)
    elif args.sample == 'positional':
        sync_query_positional_params(args.corpus, args.min_word_count)
    elif args.sample == 'array':
        sync_query_array_params(args.gender, args.states)
    elif args.sample == 'timestamp':
        sync_query_timestamp_params(
                args.year, args.month, args.day, args.hour, args.minute)
    elif args.sample == 'struct':
        sync_query_struct_params(args.x, args.y)
    else:
        print('Unexpected value for sample')
