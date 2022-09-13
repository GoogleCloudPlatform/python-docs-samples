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

from samples.snippets import disable_processor_sample, enable_processor_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "5e32eb3e1d0237c0"


def test_disable_processor(capsys):
    disable_processor_sample.disable_processor_sample(
        project_id=project_id, location=location, processor_id=processor_id
    )
    out, _ = capsys.readouterr()

    assert "projects" in out
    assert "locations" in out
    assert "operations" in out

    # Re-Enable Processor
    enable_processor_sample.enable_processor_sample(
        project_id=project_id, location=location, processor_id=processor_id
    )
