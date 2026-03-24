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


def test_call_python_udf(project_id: str, location: str):
    import bigframes.pandas as bpd

    bpd.close_session()

    # [START bigquery_dataframes_call_python_udf]
    import bigframes.pandas as bpd

    # Set the billing project to use for queries. This step is optional, as the
    # project can be inferred from your environment in many cases.
    bpd.options.bigquery.project = project_id  # "your-project-id"

    # Since this example works with local data, set a processing location.
    bpd.options.bigquery.location = location  # "US"

    # Create a sample series.
    xml_series = bpd.Series(
        [
            """
            <book id="1">
                <title>The Great Gatsby</title>
                <author>F. Scott Fitzgerald</author>
            </book>
            """,
            """
            <book id="2">
                <title>1984</title>
                <author>George Orwell</author>
            </book>
            """,
            """
            <book id="3">
                <title>Brave New World</title>
                <author>Aldous Huxley</author>
            </book>
            """,
        ]
    )

    # This example uses a function that has been deployed to bigquery-utils for
    # demonstration purposes. To use in production, deploy the function at
    # https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/udfs/community/cw_xml_extract.sqlx
    # to your own project.
    cw_xml_extract = bpd.read_gbq_function("bqutil.fn.cw_xml_extract")

    xpath_query = "//title/text()"
    titles = xml_series.apply(cw_xml_extract, args=(xpath_query,))
    result = titles.to_pandas()
    # [END bigquery_dataframes_call_python_udf]
    print(result)
    assert len(result.index) == 3


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str)
    parser.add_argument("--location", default="US", type=str)
    args = parser.parse_args()
    test_call_python_udf(project_id=args.project_id, location=args.location)
