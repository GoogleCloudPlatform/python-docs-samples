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

import os

import import_dataset

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
BUCKET_ID = "{}-lcm".format(PROJECT_ID)
DATASET_ID = "TEN0000000000000000000"


def test_import_dataset(capsys):
    # As importing a dataset can take a long time and only four operations can
    # be run on a dataset at once. Try to import into a nonexistent dataset and
    # confirm that the dataset was not found, but other elements of the request
    # were valid.
    try:
        data = "gs://{}/sentiment-analysis/dataset.csv".format(BUCKET_ID)
        import_dataset.import_dataset(PROJECT_ID, DATASET_ID, data)
        out, _ = capsys.readouterr()
        assert (
            "The Dataset doesn't exist or is inaccessible for use with AutoMl." in out
        )
    except Exception as e:
        assert (
            "The Dataset doesn't exist or is inaccessible for use with AutoMl."
            in e.message
        )
