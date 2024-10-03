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


def create_evaluation_task() -> EvalResult:
    # [START generativeaionvertexai_create_evaluation_task]
    import pandas as pd

    import vertexai
    from vertexai.preview.evaluation import EvalTask, MetricPromptTemplateExamples

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    eval_dataset = pd.DataFrame(
        {
            "instruction": [
                "Summarize the text in one sentence.",
                "Summarize the text such that a five-year-old can understand.",
            ],
            "context": [
                """As part of a comprehensive initiative to tackle urban congestion and foster
                sustainable urban living, a major city has revealed ambitious plans for an
                extensive overhaul of its public transportation system. The project aims not
                only to improve the efficiency and reliability of public transit but also to
                reduce the city\'s carbon footprint and promote eco-friendly commuting options.
                City officials anticipate that this strategic investment will enhance
                accessibility for residents and visitors alike, ushering in a new era of
                efficient, environmentally conscious urban transportation.""",
                """A team of archaeologists has unearthed ancient artifacts shedding light on a
                previously unknown civilization. The findings challenge existing historical
                narratives and provide valuable insights into human history.""",
            ],
            "response": [
                "A major city is revamping its public transportation system to fight congestion, reduce emissions, and make getting around greener and easier.",
                "Some people who dig for old things found some very special tools and objects that tell us about people who lived a long, long time ago! What they found is like a new puzzle piece that helps us understand how people used to live.",
            ],
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            MetricPromptTemplateExamples.Pointwise.SUMMARIZATION_QUALITY,
            MetricPromptTemplateExamples.Pointwise.GROUNDEDNESS,
            MetricPromptTemplateExamples.Pointwise.VERBOSITY,
            MetricPromptTemplateExamples.Pointwise.INSTRUCTION_FOLLOWING,
        ],
    )

    prompt_template = (
        "Instruction: {instruction}. Article: {context}. Summary: {response}"
    )
    result = eval_task.evaluate(prompt_template=prompt_template)

    print("Summary Metrics:\n")

    for key, value in result.summary_metrics.items():
        print(f"{key}: \t{value}")

    print("\n\nMetrics Table:\n")
    print(result.metrics_table)
    # Example response:
    # Summary Metrics:
    # row_count:      2
    # summarization_quality/mean:     3.5
    # summarization_quality/std:      2.1213203435596424
    # ...

    # [END generativeaionvertexai_create_evaluation_task]
    return result


if __name__ == "__main__":
    create_evaluation_task()
