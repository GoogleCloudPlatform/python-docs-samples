#!/usr/bin/env python

# Copyright 2022 Google LLC
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

"""Pyspark Hudi example."""

import sys
# pylint: disable=import-error
from pyspark.sql import SparkSession


def create_hudi_table(spark, table_name, table_uri):
    """Creates Hudi table."""
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            uuid string,
            begin_lat double,
            begin_lon double,
            end_lat double,
            end_lon double,
            driver string,
            rider string,
            fare double,
            partitionpath string,
            ts long
        ) USING hudi
        LOCATION '{table_uri}'
        TBLPROPERTIES (
            type = 'cow',
            primaryKey = 'uuid',
            preCombineField = 'ts'
        )
        PARTITIONED BY (partitionpath)
    """
    spark.sql(create_table_sql)


def generate_test_dataframe(spark, n_rows):
    """Generates test dataframe with Hudi's built-in data generator."""
    spark_context = spark.sparkContext
    # pylint: disable=protected-access
    utils = spark_context._jvm.org.apache.hudi.QuickstartUtils
    data_generator = utils.DataGenerator()
    inserts = utils.convertToStringList(data_generator.generateInserts(n_rows))
    return spark.read.json(spark_context.parallelize(inserts, 2))


def write_hudi_table(table_name, table_uri, dataframe):
    """Writes Hudi table."""
    options = {
            'hoodie.table.name': table_name,
            'hoodie.datasource.write.recordkey.field': 'uuid',
            'hoodie.datasource.write.partitionpath.field': 'partitionpath',
            'hoodie.datasource.write.table.name': table_name,
            'hoodie.datasource.write.operation': 'upsert',
            'hoodie.datasource.write.precombine.field': 'ts',
            'hoodie.upsert.shuffle.parallelism': 2,
            'hoodie.insert.shuffle.parallelism': 2,
    }
    dataframe.write \
      .format('hudi').options(**options).mode('append').save(table_uri)


def query_commit_history(spark, table_name, table_uri):
    """Query commit history."""
    tmp_table = f'{table_name}_commit_history'
    spark.read.format('hudi').load(table_uri).createOrReplaceTempView(tmp_table)
    query = f"""
        SELECT DISTINCT(_hoodie_commit_time)
        FROM {tmp_table}
        ORDER BY _hoodie_commit_time
        DESC
    """
    return spark.sql(query)


def read_hudi_table(spark, table_name, table_uri, commit_ts=''):
    """Reads Hudi table at the given commit timestamp."""
    if commit_ts:
        options = {'as.of.instant': commit_ts}
    else:
        options = {}
    tmp_table = f'{table_name}_snapshot'
    spark.read.format('hudi').options(**options).load(
            table_uri
    ).createOrReplaceTempView(tmp_table)
    query = f"""
        SELECT _hoodie_commit_time, begin_lat, begin_lon,
                driver, end_lat, end_lon, fare, partitionpath,
                rider, ts, uuid
        FROM {tmp_table}
    """
    return spark.sql(query)


def main():
    """Test create write and read Hudi table."""
    if len(sys.argv) != 3:
        raise Exception('Expected arguments: <table_name> <table_uri>')

    table_name = sys.argv[1]
    table_uri = sys.argv[2]

    app_name = f'pyspark-hudi-test_{table_name}'
    print(f'Creating Spark session {app_name} ...')
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    print(f'Creating Hudi table {table_name} at {table_uri} ...')
    create_hudi_table(spark, table_name, table_uri)

    print('Generating test data batch 1...')
    n_rows1 = 10
    input_df1 = generate_test_dataframe(spark, n_rows1)
    input_df1.show(truncate=False)

    print('Writing Hudi table, batch 1 ...')
    write_hudi_table(table_name, table_uri, input_df1)

    print('Generating test data batch 2...')
    n_rows2 = 10
    input_df2 = generate_test_dataframe(spark, n_rows2)
    input_df2.show(truncate=False)

    print('Writing Hudi table, batch 2 ...')
    write_hudi_table(table_name, table_uri, input_df2)

    print('Querying commit history ...')
    commits_df = query_commit_history(spark, table_name, table_uri)
    commits_df.show(truncate=False)
    # pylint: disable=protected-access
    previous_commit = commits_df.collect()[1]._hoodie_commit_time

    print('Reading the Hudi table snapshot at the latest commit ...')
    output_df1 = read_hudi_table(spark, table_name, table_uri)
    output_df1.show(truncate=False)

    print(f'Reading the Hudi table snapshot at {previous_commit} ...')
    output_df2 = read_hudi_table(spark, table_name, table_uri, previous_commit)
    output_df2.show(truncate=False)

    print('Stopping Spark session ...')
    spark.stop()

    print('All done')


main()
