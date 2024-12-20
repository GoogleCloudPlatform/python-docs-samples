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


import prompt_create_save_generate
import prompt_delete
import prompt_list_prompts
import prompt_list_version
import prompt_load_or_retrieve
import prompt_restore_version
import prompt_template


def test_prompt_template() -> None:
    text = prompt_template.prompt_template_example()
    assert len(text) > 2


def test_prompt_create_save_generate() -> None:
    response = prompt_create_save_generate.prompt_local_prompt_create()
    assert response


def test_prompt_list_prompts() -> None:
    list_prompts = prompt_list_prompts.list_prompt()
    assert list_prompts


def test_prompt_load_or_retrieve() -> str:
    get_prompt = prompt_load_or_retrieve.get_prompt()
    assert get_prompt


def test_prompt_list_version() -> None:
    list_versions = prompt_list_version.list_prompt_version()
    assert list_versions


def test_prompt_delete() -> None:
    prompt = prompts.Prompt(
        prompt_name="Test-prompt",
        prompt_data="This is a test prompt.",
    )

    prompt1 = prompts.create_version(prompt=prompt)
    prompt_id = prompt1.prompt_id
    prompt_delete.delete_prompt()

    try:
        prompts.get(prompt_id=prompt_id)
        assert False, "Prompt was not deleted!"
    except Exception:
        assert True


def test_prompt_restore_version() -> None:
    prompt1 = prompt_restore_version.restore_prompt_version()
    assert prompt1
