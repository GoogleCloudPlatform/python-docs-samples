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

import backoff
import pytest

from google.api_core.exceptions import ResourceExhausted
from vertexai.generative_models import GenerativeModel, Tool

import advanced_example
import basic_example
import chat_example
import chat_function_calling_basic
import chat_function_calling_config
import parallel_function_calling_example
import declare_function_from_function


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling() -> None:
    response = basic_example.generate_function_call()

    expected_summary = [
        "Boston",
    ]
    expected_responses = [
        "candidates",
        "content",
        "role",
        "model",
        "parts",
        "Boston",
    ]
    assert all(x in str(response.text) for x in expected_summary)
    assert all(x in str(response) for x in expected_responses)


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_advanced_function_selection() -> None:
    response = advanced_example.generate_function_call_advanced()
    assert (
        "Pixel 8 Pro 128GB"
        in response.candidates[0].function_calls[0].args["product_name"]
    )


@pytest.mark.skip(reason="Blocked on b/... ")
@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_basic() -> None:
    response = chat_function_calling_basic.generate_text()
    assert "get_current_weather" in response.choices[0].message.tool_calls[0].id


@pytest.mark.skip(reason="Blocked on b/... ")
@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_config() -> None:
    response = chat_function_calling_config.generate_text()
    assert "Boston" in response.choices[0].message.tool_calls[0].function.arguments


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_function_calling_chat() -> None:
    chat = chat_example.generate_function_call_chat()

    assert chat
    assert chat.history

    expected_summaries = [
        "Pixel 8 Pro",
        "stock",
        "store",
        "2000 N Shoreline Blvd",
        "Mountain View",
    ]
    assert any(x in str(chat.history) for x in expected_summaries)


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_parallel_function_calling() -> None:
    response = parallel_function_calling_example.parallel_function_calling_example()
    assert response is not None


def test_function_declaration_from_func() -> None:
    func_declaration = declare_function_from_function.function_declaration_from_func()
    tools = Tool(function_declarations=[func_declaration])
    model = GenerativeModel(model_name="gemini-1.5-pro-002", tools=[tools])
    chat_session = model.start_chat()
    response = chat_session.send_message("What will be 1 multiplied by 2?")

    assert response is not None
