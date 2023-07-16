# Copyright 2023 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-return-statements

from datetime import date
from typing import List
from unittest.mock import MagicMock

import pytest
from google.cloud import storage

import main

TEST_LOG_ID = 'test-log'
TEST_BUCKET = 'test-bucket'
TEST_BUCKET_NAME = f'gs://{TEST_BUCKET}'


def _setup_environment(task_index: int = 0, task_count: int = 1,
                       start_date: str = '01/01/0001', end_date: str = '01/01/0001',
                       log_id: str = TEST_LOG_ID, storage_bucket: str = TEST_BUCKET):
    main.LOG_ID = log_id
    main.BUCKET_NAME = storage_bucket
    main.TASK_INDEX = task_index
    main.TASK_COUNT = task_count
    main.START_DATE = start_date
    main.END_DATE = end_date


@pytest.mark.parametrize(
    'start_date, end_date, task_index, task_count, expected_first_day, expected_last_day',
    [(date(2001, 1, 1), date(2001, 1, 31), 0, 1,
      date(2001, 1,  1), date(2001, 1, 31)),
     (date(2001, 1, 1), date(2001, 1, 10), 0, 20,
      date(2001, 1,  1), date(2001, 1,  2)),
     (date(2001, 1, 1), date(2001, 1, 10), 12, 20,
      date(2001, 1, 10), date(2001, 1, 1)),
     (date(2001, 1, 10), date(2001, 2, 1), 0, 2,
      date(2001, 1, 10), date(2001, 1, 21)),
     (date(2001, 1, 10), date(2001, 2, 1), 1, 2,
      date(2001, 1, 22), date(2001, 2, 1)),
     (date(2001, 5, 5), date(2002, 2, 2), 1, 2,
      date(2001, 9, 19), date(2002, 2, 2)),
     ],
    ids=['simple single range',
         'more tasks than days',
         'extra task when more tasks then days',
         'two month range task 1',
         'two month range task 2',
         'multi year range'
         ])
def test_calc_import_range(start_date: str, end_date: str, task_index: int, task_count: int,
                           expected_first_day: date, expected_last_day: date):
    _setup_environment(task_index=task_index, task_count=task_count,
                       start_date=start_date, end_date=end_date)

    first_day, last_day = main.calc_import_range()

    assert first_day == expected_first_day, \
        f'first day is wrong: expected {expected_first_day} and got {first_day}'
    assert last_day == expected_last_day, \
        f'last day is wrong: expected {expected_last_day} and got {last_day}'


TEST_FILES_JUN_2001 = [
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/06/01/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/06/01/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/06/02/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/06/02/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/06/03/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/06/03/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/06/04/file2.json', bucket=TEST_BUCKET),
]
TEST_FILES_JUL_2001 = [
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/07/01/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/07/01/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/07/02/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/07/02/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/07/03/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/07/03/file2.json', bucket=TEST_BUCKET),
]
TEST_FILES_AUG_2001 = [
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/08/01/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/08/01/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/08/02/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/08/02/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/08/03/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2001/08/03/file2.json', bucket=TEST_BUCKET),
]
TEST_FILES_MAY_2002 = [
    storage.Blob(
        name=f'{TEST_LOG_ID}/2002/05/01/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2002/05/01/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2002/05/02/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2002/05/02/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2002/05/03/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2002/05/03/file2.json', bucket=TEST_BUCKET),
]
TEST_FILES_JAN_2003 = [
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/01/01/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/01/01/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/01/02/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/01/02/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/01/03/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/01/03/file2.json', bucket=TEST_BUCKET),
]
TEST_FILES_FEB_2003 = [
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/02/01/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/02/01/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/02/02/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/02/02/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/02/03/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/02/03/file2.json', bucket=TEST_BUCKET),
]
TEST_FILES_MAR_2003 = [
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/03/01/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/03/01/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/03/02/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/03/02/file2.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/03/03/file1.json', bucket=TEST_BUCKET),
    storage.Blob(
        name=f'{TEST_LOG_ID}/2003/03/03/file2.json', bucket=TEST_BUCKET),
]


def _args_based_list_blobs_return(*_args, **kwargs):
    if kwargs['prefix'] == f'{TEST_LOG_ID}/2001/06/':
        print('TEST_FILES_JUN_2001')
        return TEST_FILES_JUN_2001
    elif kwargs['prefix'] == f'{TEST_LOG_ID}/2001/07/':
        print('TEST_FILES_JUL_2001')
        return TEST_FILES_JUL_2001
    elif kwargs['prefix'] == f'{TEST_LOG_ID}/2001/08/':
        print('TEST_FILES_AUG_2001')
        return TEST_FILES_AUG_2001
    elif kwargs['prefix'] == f'{TEST_LOG_ID}/2002/05/':
        print('TEST_FILES_MAY_2002')
        return TEST_FILES_MAY_2002
    elif kwargs['prefix'] == f'{TEST_LOG_ID}/2003/01/':
        print('TEST_FILES_JAN_2003')
        return TEST_FILES_JAN_2003
    elif kwargs['prefix'] == f'{TEST_LOG_ID}/2003/02/':
        print('TEST_FILES_FEB_2003')
        return TEST_FILES_FEB_2003
    elif kwargs['prefix'] == f'{TEST_LOG_ID}/2003/03/':
        print('TEST_FILES_MAR_2003')
        return TEST_FILES_MAR_2003
    else:
        return []


@ pytest.mark.parametrize(
    'first_day, last_day, expected_paths',
    [(date(2001, 6,  1), date(2001, 6, 30),
      [f.name for f in TEST_FILES_JUN_2001]),
     (date(2001, 6,  2), date(2001, 6, 3),
      [f.name for f in TEST_FILES_JUN_2001[2:-1]]),
     (date(2001, 7,  3), date(2003, 2,  2),
      [f.name for f in [*TEST_FILES_JUL_2001[-2:],
                        *TEST_FILES_AUG_2001,
                        *TEST_FILES_MAY_2002,
                        *TEST_FILES_JAN_2003,
                        *TEST_FILES_FEB_2003[:-2]]]),
     ])
#    ids=['simple one month range', 'subrange of one month', 'cross year range'])
def test_list_log_files(first_day: str, last_day: str, expected_paths: List):
    _setup_environment()

    mocked_client = MagicMock(spec=storage.Client)
    mocked_client.list_blobs = MagicMock(
        side_effect=_args_based_list_blobs_return)

    paths = main.list_log_files(first_day, last_day, mocked_client)

    assert set(paths) == set(expected_paths)
