# Copyright 2026 Google LLC
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

# [START aiplatform_genai_evaluation_pairwise_summarization_quality]

import os

from google import genai
from google.genai import types

import pandas as pd

from vertexai.evaluation import (
    EvalTask,
    MetricPromptTemplateExamples,
    PairwiseMetric,
)
from vertexai.preview.evaluation import EvalResult

# TODO (developer) set GOOGLE_CLOUD_PROJECT and REGION_ID
# environment variables before running.
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("REGION_ID")
BASELINE_MODEL = os.getenv("BASELINE_MODEL", "gemini-2.5-flash")
CANDIDATE_MODEL = os.getenv("CANDIDATE_MODEL", "gemini-2.5-pro")

PROMPT = """
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


def evaluate_output() -> EvalResult:
    """
    Evaluates a candidate model's summarization quality
    against a baseline model using Vertex AI.
    """

    baseline_responses = []
    candidate_responses = []

    genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    baseline_resp = genai_client.models.generate_content(
        model=BASELINE_MODEL,
        contents=PROMPT,
        config=types.GenerateContentConfig(temperature=0.4),
    )
    baseline_responses.append(baseline_resp.text)

    candidate_resp = genai_client.models.generate_content(
        model=CANDIDATE_MODEL,
        contents=PROMPT,
        config=types.GenerateContentConfig(temperature=0.4),
    )
    candidate_responses.append(candidate_resp.text)

    eval_df = pd.DataFrame(
        {
            "prompt": PROMPT,
            "response": candidate_responses,
            "baseline_model_response": baseline_responses,
        }
    )

    prompt_template = MetricPromptTemplateExamples.get_prompt_template(
        "pairwise_summarization_quality"
    )

    pairwise_text_quality = PairwiseMetric(
        metric="pairwise_summarization_quality",
        metric_prompt_template=prompt_template,
    )

    eval_task = EvalTask(
        dataset=eval_df,
        metrics=[pairwise_text_quality],
        experiment="pairwise-benchmark2",
    )

    comparison_result = eval_task.evaluate()

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", 250)

    columns_to_print = [
        "prompt",
        "baseline_model_response",
        "response",
        "pairwise_summarization_quality/pairwise_choice",
        "pairwise_summarization_quality/explanation",
    ]
    print(comparison_result.metrics_table[columns_to_print])

    return comparison_result


# [END aiplatform_genai_evaluation_pairwise_summarization_quality]
