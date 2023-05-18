# Copyright 2022 Google LLC
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
#

# flake8: noqa

import os

from documentai.snippets import list_evaluations_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "feacd98c28866ede"
processor_version_id = "stable"


def test_list_evaluations(capsys):

    list_evaluations_sample.list_evaluations_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_id=processor_version_id,
    )

    out, _ = capsys.readouterr()
    assert "Evaluation" in out
