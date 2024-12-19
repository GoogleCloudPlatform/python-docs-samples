# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from vertexai.preview import prompts


import prompt_template
import prompt_template_create_save_generate
import prompt_template_delete
import prompt_template_list_prompts
import prompt_template_list_version
import prompt_template_load_or_retrieve


def test_prompt_template() -> None:
    text = prompt_template.prompt_template_example()
    assert len(text) > 2


def test_prompt_template_create_save_generate() -> None:
    response = prompt_template_create_save_generate.prompt_template_local_prompt_generate()
    assert response


def test_prompt_template_list_prompts() -> None:
    list_prompts = prompt_template_list_prompts.list_prompt_generate()
    assert list_prompts


def test_prompt_template_load_or_retrieve() -> str:
    get_prompt = prompt_template_load_or_retrieve.load_prompt_generate()
    assert get_prompt


def test_prompt_template_list_version() -> None:
    list_versions = prompt_template_list_version.list_prompt_version_generate()
    assert list_versions


def test_prompt_template_delete() -> None:
    prompts.delete = prompt_template_delete.delete_prompt_version_generate()
    assert True
