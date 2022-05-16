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

import uuid

import storage_fileio_pandas
import storage_fileio_write_read


def test_fileio_write_read(bucket, capsys):
    blob_name = f"test-fileio-{uuid.uuid4()}"
    storage_fileio_write_read.write_read(bucket.name, blob_name)
    out, _ = capsys.readouterr()
    assert "Hello world" in out


def test_fileio_pandas(bucket, capsys):
    blob_name = f"test-fileio-{uuid.uuid4()}"
    storage_fileio_pandas.pandas_write(bucket.name, blob_name)
    out, _ = capsys.readouterr()
    assert f"Wrote csv with pandas with name {blob_name} from bucket {bucket.name}." in out
    storage_fileio_pandas.pandas_read(bucket.name, blob_name)
    out, _ = capsys.readouterr()
    assert f"Read csv with pandas with name {blob_name} from bucket {bucket.name}." in out
