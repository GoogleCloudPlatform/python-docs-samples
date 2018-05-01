# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from .get_dag_prefix import get_dag_prefix


PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
COMPOSER_LOCATION = os.environ['COMPOSER_LOCATION']
COMPOSER_ENVIRONMENT = os.environ['COMPOSER_ENVIRONMENT']


def test_get_dag_prefix(capsys):
    get_dag_prefix(PROJECT, COMPOSER_LOCATION, COMPOSER_ENVIRONMENT)
    out, _ = capsys.readouterr()
    assert 'gs://' in out
