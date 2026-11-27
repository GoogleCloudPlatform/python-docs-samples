#!/usr/bin/env python
#  Copyright 2026 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# [START dataflow_batch_process_storage]
import argparse
from typing import List, Optional, Tuple

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


def parse_record(line: str) -> Tuple[str, float]:
    """Parses a CSV line into a (product, amount) tuple."""
    _, product, amount = line.split(",")
    return product, float(amount)


def run(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="Bucket path or glob, such as gs://bucket/input/*.csv",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Bucket path prefix, such as gs://bucket/output/sales",
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as pipeline:
        (
            pipeline
            | "ReadFromGCS"
            >> beam.io.ReadFromText(known_args.input, skip_header_lines=1)
            | "Parse" >> beam.Map(parse_record)
            | "SumByProduct" >> beam.CombinePerKey(sum)
            | "Format" >> beam.MapTuple(lambda product, total: f"{product},{total:.2f}")
            | "WriteToGCS"
            >> beam.io.WriteToText(
                known_args.output,
                file_name_suffix=".csv",
                header="product,total_sales",
            )
        )


if __name__ == "__main__":
    run()
# [END dataflow_batch_process_storage]
