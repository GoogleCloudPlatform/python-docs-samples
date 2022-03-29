# Copyright 2021 Google Inc. All Rights Reserved.
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

import datetime

import numpy as np
from pandas import Timestamp


def test_pandas_date_and_time():
    from .pandas_date_and_time import pandas_date_and_time

    (
        dates,
        _,
        dates2,
        diffs,
        do,
        after,
        before,
        times,
        _,
        combined,
        combined0,
    ) = pandas_date_and_time()

    assert str(dates.dtype) == "dbdate"
    assert list(dates) == [datetime.date(2021, 9, 17), datetime.date(2021, 9, 18)]

    assert np.array_equal(
        diffs,
        dates.astype("datetime64") - dates2.astype("datetime64"),
    )

    assert np.array_equal(after, dates.astype("object") + do)
    assert np.array_equal(before, dates.astype("object") - do)

    assert str(times.dtype) == "dbtime"
    assert list(times) == [
        datetime.time(1, 2, 3, 456789),
        datetime.time(12, 0, 0, 600000),
    ]

    for c in combined0, combined:
        assert str(c.dtype) == "datetime64[ns]"
        assert list(c) == [
            Timestamp("2021-09-17 01:02:03.456789"),
            Timestamp("2021-09-18 12:00:00.600000"),
        ]
