# Copyright 2021 Google LLC
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


def pandas_date_and_time():
    # [START bigquery_pandas_date_create]

    import datetime

    import pandas as pd

    import db_dtypes  # noqa import to register dtypes

    dates = pd.Series([datetime.date(2021, 9, 17), "2021-9-18"], dtype="dbdate")

    # [END bigquery_pandas_date_create]
    # [START bigquery_pandas_date_as_datetime]

    datetimes = dates.astype("datetime64")

    # [END bigquery_pandas_date_as_datetime]
    # [START bigquery_pandas_date_sub]

    dates2 = pd.Series(["2021-1-1", "2021-1-2"], dtype="dbdate")
    diffs = dates - dates2

    # [END bigquery_pandas_date_sub]
    # [START bigquery_pandas_date_add_offset]

    do = pd.DateOffset(days=1)
    after = dates + do
    before = dates - do

    # [END bigquery_pandas_date_add_offset]
    # [START bigquery_pandas_time_create]

    times = pd.Series([datetime.time(1, 2, 3, 456789), "12:00:00.6"], dtype="dbtime")

    # [END bigquery_pandas_time_create]
    # [START bigquery_pandas_time_as_timedelta]

    timedeltas = times.astype("timedelta64")

    # [END bigquery_pandas_time_as_timedelta]

    # Combine datetime64 and timedelta64 to confirm adding dates and times are
    # equivalent.
    combined0 = datetimes + timedeltas

    # [START bigquery_pandas_combine_date_time]

    combined = dates + times

    # [END bigquery_pandas_combine_date_time]

    return (
        dates,
        datetimes,
        dates2,
        diffs,
        do,
        after,
        before,
        times,
        timedeltas,
        combined,
        combined0,
    )
