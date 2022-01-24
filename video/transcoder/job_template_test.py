# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from google.api_core.exceptions import NotFound

import create_job_template
import delete_job_template
import get_job_template
import list_job_templates

location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
project_number = os.environ["GOOGLE_CLOUD_PROJECT_NUMBER"]
template_id = f"my-python-test-template-{uuid.uuid4()}"


def test_template_operations(capsys):

    # Enable the following API on the test project:
    # *   Transcoder API

    job_template_name = (
        f"projects/{project_number}/locations/{location}/jobTemplates/{template_id}"
    )

    try:
        delete_job_template.delete_job_template(project_id, location, template_id)
    except NotFound as e:
        print(f"Ignoring NotFound, details: {e}")
    out, _ = capsys.readouterr()

    create_job_template.create_job_template(project_id, location, template_id)
    out, _ = capsys.readouterr()
    assert job_template_name in out

    get_job_template.get_job_template(project_id, location, template_id)
    out, _ = capsys.readouterr()
    assert job_template_name in out

    list_job_templates.list_job_templates(project_id, location)
    out, _ = capsys.readouterr()
    assert job_template_name in out

    delete_job_template.delete_job_template(project_id, location, template_id)
    out, _ = capsys.readouterr()
    assert "Deleted job template" in out
