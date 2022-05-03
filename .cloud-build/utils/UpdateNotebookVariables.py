#!/usr/bin/env python
# Copyright 2022 Google LLC
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

import re

"""
 This script is used to update variables in the notebook via regex
 It requires variables to be defined in particular format
For example, if your variable was PROJECT_ID, use:
    PROJECT_ID = "[your_project_here]"
Single-quotes also work:
    PROJECT_ID = '[your_project_here]'
Variables in conditionals can also be replaced:
    PROJECT_ID == "[your_project_here]"
"""


def get_updated_value(content: str, variable_name: str, variable_value: str) -> str:
    return re.sub(
        rf"({variable_name}.*?=.*?[\",\'])\[.+?\]([\",\'].*?)",
        rf"\1{variable_value}\2",
        content,
        flags=re.M,
    )


def test_update_value():
    new_content = get_updated_value(
        content='asdf\nPROJECT_ID = "[your-project-id]" #@param {type:"string"} \nasdf',
        variable_name="PROJECT_ID",
        variable_value="sample-project",
    )
    assert (
        new_content
        == 'asdf\nPROJECT_ID = "sample-project" #@param {type:"string"} \nasdf'
    )


def test_update_value_single_quotes():
    new_content = get_updated_value(
        content="PROJECT_ID = '[your-project-id]'",
        variable_name="PROJECT_ID",
        variable_value="sample-project",
    )
    assert new_content == "PROJECT_ID = 'sample-project'"


def test_update_value_avoidance():
    new_content = get_updated_value(
        content="PROJECT_ID = shell_output[0] ",
        variable_name="PROJECT_ID",
        variable_value="sample-project",
    )
    assert new_content == "PROJECT_ID = shell_output[0] "


def test_region():
    new_content = get_updated_value(
        content='REGION = "[your-region]"  # @param {type:"string"}',
        variable_name="REGION",
        variable_value="us-central1",
    )
    assert new_content == 'REGION = "us-central1"  # @param {type:"string"}'
