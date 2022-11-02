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

import os

from samples.snippets import set_default_processor_version_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "aeb8cea219b7c272"
current_default_processor_version = "pretrained-ocr-v1.0-2020-09-23"
new_default_processor_version = "pretrained-ocr-v1.1-2022-09-12"


def test_set_default_processor_version(capsys):
    set_default_processor_version_sample.set_default_processor_version_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_id=new_default_processor_version,
    )
    out, _ = capsys.readouterr()

    assert "operation" in out

    # Set back to previous default
    set_default_processor_version_sample.set_default_processor_version_sample(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version_id=current_default_processor_version,
    )
