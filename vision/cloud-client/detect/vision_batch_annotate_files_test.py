# -*- coding: utf-8 -*-
# Copyright 2020 Google
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
import uuid

import vision_batch_annotate_files

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
GCS_ROOT = "gs://cloud-samples-data/vision/"

BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
OUTPUT_PREFIX = "TEST_OUTPUT_{}".format(uuid.uuid4())
GCS_DESTINATION_URI = "gs://{}/{}/".format(BUCKET, OUTPUT_PREFIX)


def test_sample_batch_annotate_files(capsys):
    file_path = "resources/kafka.pdf"

    vision_batch_annotate_files.sample_batch_annotate_files(file_path=file_path)

    out, _ = capsys.readouterr()

    assert "Full text" in out
    assert "Block confidence" in out
