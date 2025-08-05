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
import os

from vertexai.preview.evaluation import EvalResult

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def evaluate_output() -> EvalResult:
    # [START generativeaionvertexai_evaluation_pairwise_summarization_quality]
    import pandas as pd

    import vertexai
    from vertexai.generative_models import GenerativeModel
    from vertexai.evaluation import (
        EvalTask,
        PairwiseMetric,
        MetricPromptTemplateExamples,
    )

    # TODO(developer): Update & uncomment line below
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

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

    eval_dataset = pd.DataFrame({"prompt": [prompt]})

    # Baseline model for pairwise comparison
    baseline_model = GenerativeModel("gemini-2.0-flash-lite-001")

    # Candidate model for pairwise comparison
    candidate_model = GenerativeModel(
        "gemini-2.0-flash-001", generation_config={"temperature": 0.4}
    )

    prompt_template = MetricPromptTemplateExamples.get_prompt_template(
        "pairwise_summarization_quality"
    )

    summarization_quality_metric = PairwiseMetric(
        metric="pairwise_summarization_quality",
        metric_prompt_template=prompt_template,
        baseline_model=baseline_model,
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[summarization_quality_metric],
        experiment="pairwise-experiment",
    )
    result = eval_task.evaluate(model=candidate_model)

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
