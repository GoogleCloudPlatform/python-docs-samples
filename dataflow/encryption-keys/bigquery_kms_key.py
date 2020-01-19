#!/usr/bin/env python
#
# Copyright 2019 Google Inc. All Rights Reserved.
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

import argparse


def run(output_bigquery_table, kms_key, beam_args):
    # [START dataflow_cmek]
    import apache_beam as beam

    # output_bigquery_table = '<project>:<dataset>.<table>'
    # kms_key = 'projects/<project>/locations/<kms-location>/keyRings/<kms-keyring>/cryptoKeys/<kms-key>' # noqa
    # beam_args = [
    #     '--project', 'your-project-id',
    #     '--runner', 'DataflowRunner',
    #     '--temp_location', 'gs://your-bucket/samples/dataflow/kms/tmp',
    #     '--region', 'us-central1',
    # ]

    # Query from the NASA wildfires public dataset:
    # https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=nasa_wildfire&t=past_week&page=table
    query = """
        SELECT latitude,longitude,acq_date,acq_time,bright_ti4,confidence
        FROM `bigquery-public-data.nasa_wildfire.past_week`
        LIMIT 10
    """

    # Schema for the output BigQuery table.
    schema = {
        'fields': [
            {'name': 'latitude', 'type': 'FLOAT'},
            {'name': 'longitude', 'type': 'FLOAT'},
            {'name': 'acq_date', 'type': 'DATE'},
            {'name': 'acq_time', 'type': 'TIME'},
            {'name': 'bright_ti4', 'type': 'FLOAT'},
            {'name': 'confidence', 'type': 'STRING'},
        ],
    }

    options = beam.options.pipeline_options.PipelineOptions(beam_args)
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | 'Read from BigQuery with KMS key' >>
            beam.io.Read(beam.io.BigQuerySource(
                query=query,
                use_standard_sql=True,
                kms_key=kms_key,
            ))
            | 'Write to BigQuery with KMS key' >>
            beam.io.WriteToBigQuery(
                output_bigquery_table,
                schema=schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                kms_key=kms_key,
            )
        )
    # [END dataflow_cmek]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--kms_key',
        required=True,
        help='Cloud Key Management Service key name',
    )
    parser.add_argument(
        '--output_bigquery_table',
        required=True,
        help="Output BigQuery table in the format 'PROJECT:DATASET.TABLE'",
    )
    args, beam_args = parser.parse_known_args()

    run(args.output_bigquery_table, args.kms_key, beam_args)
