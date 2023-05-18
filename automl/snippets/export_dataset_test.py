# Copyright 2020 Google LLC
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
import os

import export_dataset

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
BUCKET_ID = f"{PROJECT_ID}-lcm"
PREFIX = "TEST_EXPORT_OUTPUT_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
DATASET_ID = "TEN0000000000000000000"


def test_export_dataset(capsys):
    # As exporting a dataset can take a long time and only one operation can be
    # run on a dataset at once. Try to export a nonexistent dataset and confirm
    # that the dataset was not found, but other elements of the request were\
    # valid.
    try:
        export_dataset.export_dataset(
            PROJECT_ID, DATASET_ID, f"gs://{BUCKET_ID}/{PREFIX}/"
        )
        out, _ = capsys.readouterr()
        assert (
            "The Dataset doesn't exist or is inaccessible for use with AutoMl." in out
        )
    except Exception as e:
        assert (
            "The Dataset doesn't exist or is inaccessible for use with AutoMl."
            in e.message
        )
