# Copyright 2019 Google LLC
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

import typing

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def load_table_dataframe(table_id: str) -> "bigquery.Table":

    # [START bigquery_load_table_dataframe]
    import datetime

    from google.cloud import bigquery
    import pandas
    import pytz

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    records = [
        {
            "title": "The Meaning of Life",
            "release_year": 1983,
            "length_minutes": 112.5,
            "release_date": pytz.timezone("Europe/Paris")
            .localize(datetime.datetime(1983, 5, 9, 13, 0, 0))
            .astimezone(pytz.utc),
            # Assume UTC timezone when a datetime object contains no timezone.
            "dvd_release": datetime.datetime(2002, 1, 22, 7, 0, 0),
        },
        {
            "title": "Monty Python and the Holy Grail",
            "release_year": 1975,
            "length_minutes": 91.5,
            "release_date": pytz.timezone("Europe/London")
            .localize(datetime.datetime(1975, 4, 9, 23, 59, 2))
            .astimezone(pytz.utc),
            "dvd_release": datetime.datetime(2002, 7, 16, 9, 0, 0),
        },
        {
            "title": "Life of Brian",
            "release_year": 1979,
            "length_minutes": 94.25,
            "release_date": pytz.timezone("America/New_York")
            .localize(datetime.datetime(1979, 8, 17, 23, 59, 5))
            .astimezone(pytz.utc),
            "dvd_release": datetime.datetime(2008, 1, 14, 8, 0, 0),
        },
        {
            "title": "And Now for Something Completely Different",
            "release_year": 1971,
            "length_minutes": 88.0,
            "release_date": pytz.timezone("Europe/London")
            .localize(datetime.datetime(1971, 9, 28, 23, 59, 7))
            .astimezone(pytz.utc),
            "dvd_release": datetime.datetime(2003, 10, 22, 10, 0, 0),
        },
    ]
    dataframe = pandas.DataFrame(
        records,
        # In the loaded table, the column order reflects the order of the
        # columns in the DataFrame.
        columns=[
            "title",
            "release_year",
            "length_minutes",
            "release_date",
            "dvd_release",
        ],
        # Optionally, set a named index, which can also be written to the
        # BigQuery table.
        index=pandas.Index(
            ["Q24980", "Q25043", "Q24953", "Q16403"], name="wikidata_id"
        ),
    )
    job_config = bigquery.LoadJobConfig(
        # Specify a (partial) schema. All columns are always written to the
        # table. The schema is used to assist in data type definitions.
        schema=[
            # Specify the type of columns whose type cannot be auto-detected. For
            # example the "title" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField("title", bigquery.enums.SqlTypeNames.STRING),
            # Indexes are written if included in the schema by name.
            bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING),
        ],
        # Optionally, set the write disposition. BigQuery appends loaded rows
        # to an existing table by default, but with WRITE_TRUNCATE write
        # disposition it replaces the table with the loaded data.
        write_disposition="WRITE_TRUNCATE",
    )

    job = client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )
    # [END bigquery_load_table_dataframe]
    return table
