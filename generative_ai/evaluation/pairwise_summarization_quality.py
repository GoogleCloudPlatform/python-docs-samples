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

# [START generativeaionvertexai_evaluation_pairwise_summarization_quality]

import os

import pandas as pd

from google import genai
from google.genai import types

import vertexai
from vertexai.preview.evaluation import EvalResult
from vertexai.evaluation import (
    EvalTask,
    PairwiseMetric,
    MetricPromptTemplateExamples,
)

# TODO (developer) set GOOGLE_CLOUD_PROJECT and REGION_ID
# environment variables before running.
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("REGION_ID")
BASELINE_MODEL = "gemini-2.5-flash"


def custom_model_fn(prompt: str) -> str:
    """Generates text from a prompt using the baseline Gemini model via Vertex AI."""

    genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    genai_config = types.GenerateContentConfig(temperature=0.4)

    response = genai_client.models.generate_content(
        model=BASELINE_MODEL, contents=prompt, config=genai_config
    )

    return response.text


def evaluate_output() -> EvalResult:
    """
    Evaluates a candidate model's summarization quality
    against a baseline model using Vertex AI.
    """

    prompt = """
    Summarize the text such that a five-year-old can understand.

    # Text

    As part of a comprehensive initiative to tackle urban congestion and foster
    sustainable urban living, a major city has revealed ambitious plans for an
    extensive overhaul of its public transportation system. The project aims not
    only to improve the efficiency and reliability of public transit but also to
    reduce the city\'s carbon footprint and promote eco-friendly commuting options.
    City officials anticipate that this strategic investment will enhance
    accessibility for residents and visitors alike, ushering in a new era of
    efficient, environmentally conscious urban transportation.
    """

    vertexai.init(project=PROJECT_ID, location=LOCATION)

    eval_dataset = pd.DataFrame({"prompt": [prompt]})

    prompt_template = MetricPromptTemplateExamples.get_prompt_template(
        "pairwise_summarization_quality"
    )

    summarization_quality_metric = PairwiseMetric(
        metric="pairwise_summarization_quality",
        metric_prompt_template=prompt_template,
        baseline_model=BASELINE_MODEL,
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[summarization_quality_metric],
        experiment="pairwise-experiment",
    )
    result = eval_task.evaluate(
        model=custom_model_fn, experiment_run_name="genai-client-vs-legacy-baseline-6"
    )

    baseline_model_response = result.metrics_table["baseline_model_response"].iloc[0]
    candidate_model_response = result.metrics_table["response"].iloc[0]

    winner_model = result.metrics_table[
        "pairwise_summarization_quality/pairwise_choice"
    ].iloc[0]

    explanation = result.metrics_table[
        "pairwise_summarization_quality/explanation"
    ].iloc[0]

    print(f"Baseline's story:\n{baseline_model_response}")
    print(f"Candidate's story:\n{candidate_model_response}")
    print(f"Winner: {winner_model}")
    print(f"Explanation: {explanation}")
    # Example response:
    # Baseline's story:
    # A big city wants to make it easier for people to get around without using cars! They're going to make buses and trains ...
    #
    # Candidate's story:
    # A big city wants to make it easier for people to get around without using cars! ... This will help keep the air clean ...
    #
    # Winner: CANDIDATE
    # Explanation: Both responses adhere to the prompt's constraints, are grounded in the provided text, and ... However, Response B ...
    # [END generativeaionvertexai_evaluation_pairwise_summarization_quality]
    return result


if __name__ == "__main__":
    evaluate_output()
