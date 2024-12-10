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

from google.api_core.exceptions import ResourceExhausted

import pytest

from vertexai.generative_models import GenerativeModel

import advanced_example
import basic_example
import chat_example
import chat_function_calling_basic
import chat_function_calling_config
import example_syntax
import function_calling_application
import parallel_function_calling_example


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


def test_function_calling_app() -> None:
    result = function_calling_application.create_app()
    assert result["weather_response"] is not None

    tool = result["tool"]
    model = GenerativeModel(model_name="gemini-1.5-pro-002", tools=[tool])
    chat_session = model.start_chat()

    response = chat_session.send_message("What will be 1 multiplied by 2?")
    assert response is not None

    extract_sales_prompt = """
    I need to parse a series of sale transactions written down in a text editor and extract
     full sales records for each transaction.
    1 / 031023 / $123,02
    2 / 031123 / $12,99
    3 / 031123 / $12,99
    4 / 031223 / $15,99
    5 / 031223 / $2,20
    """
    response = chat_session.send_message(extract_sales_prompt)
    assert response


def test_example_syntax() -> None:
    model = example_syntax.create_model_with_toolbox()
    assert model is not None
