#!/usr/bin/env python

# Copyright 2019 Google, Inc
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

import create_annotation_spec_set
from google.cloud import datalabeling_v1beta1 as datalabeling
import pytest

PROJECT_ID = os.getenv('GCLOUD_PROJECT')


@pytest.mark.slow
def test_create_annotation_spec_set(capsys):
    response = create_annotation_spec_set.create_annotation_spec_set(
        PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'The annotation_spec_set resource name:' in out

    # Delete the created annotation spec set.
    annotation_spec_set_name = response.name
    client = datalabeling.DataLabelingServiceClient()
    client.delete_annotation_spec_set(annotation_spec_set_name)
