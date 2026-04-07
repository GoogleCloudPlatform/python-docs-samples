# Copyright 2026 Google LLC
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


# [START bigquery_dataframes_call_python_udf]
import textwrap
from typing import Tuple

import bigframes.pandas as bpd
import pandas as pd
import pyarrow as pa


# Using partial ordering mode enables more efficient query optimizations.
bpd.options.bigquery.ordering_mode = "partial"


def call_python_udf(
    project_id: str, location: str,
) -> Tuple[pd.Series, bpd.Series]:
    # Set the billing project to use for queries. This step is optional, as the
    # project can be inferred from your environment in many cases.
    bpd.options.bigquery.project = project_id  # "your-project-id"

    # Since this example works with local data, set a processing location.
    bpd.options.bigquery.location = location  # "US"

    # Create a sample series.
    xml_series = pd.Series(
        [
            textwrap.dedent(
                """
                <book id="1">
                    <title>The Great Gatsby</title>
                    <author>F. Scott Fitzgerald</author>
                </book>
                """
            ),
            textwrap.dedent(
                """
                <book id="2">
                    <title>1984</title>
                    <author>George Orwell</author>
                </book>
                """
            ),
            textwrap.dedent(
                """
                <book id="3">
                    <title>Brave New World</title>
                    <author>Aldous Huxley</author>
                </book>
                """
            ),
        ],
        dtype=pd.ArrowDtype(pa.string()),
    )
    df = pd.DataFrame({"xml": xml_series})

    # Use the BigQuery Accessor, which is automatically registered on pandas
    # DataFrames when you import bigframes.  This example uses a function that
    # has been deployed to bigquery-utils for demonstration purposes. To use in
    # production, deploy the function at
    # https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/udfs/community/cw_xml_extract.sqlx
    # to your own project.
    titles_pandas = df.bigquery.sql_scalar(
        "`bqutil`.`fn`.cw_xml_extract({xml}, '//title/text()')",
    )

    # Alternatively, call read_gbq_function to get a pointer to the function
    # that can be applied on BigQuery DataFrames objects.
    cw_xml_extract = bpd.read_gbq_function("bqutil.fn.cw_xml_extract")
    xml_bigframes = bpd.read_pandas(xml_series)

    xpath_query = "//title/text()"
    titles_bigframes = xml_bigframes.apply(cw_xml_extract, args=(xpath_query,))
    return titles_pandas, titles_bigframes
    # [END bigquery_dataframes_call_python_udf]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    # Note: GCP project ID can be inferred from the environment if Application
    # Default Credentials are set, so None is perfectly valid for --project_id.
    parser.add_argument("--project_id", type=str)
    parser.add_argument("--location", default="US", type=str)
    args = parser.parse_args()

    pddf, bfdf = call_python_udf(project_id=args.project_id, location=args.location)
    print(pddf)
    print(bfdf.to_pandas())
