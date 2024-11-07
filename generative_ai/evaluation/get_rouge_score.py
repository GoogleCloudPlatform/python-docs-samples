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


def get_rouge_score() -> EvalResult:
    # [START generativeaionvertexai_evaluation_get_rouge_score]
    import pandas as pd

    import vertexai
    from vertexai.preview.evaluation import EvalTask

    # TODO(developer): Update & uncomment line below
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    reference_summarization = """
    The Great Barrier Reef, the world's largest coral reef system, is
    located off the coast of Queensland, Australia. It's a vast
    ecosystem spanning over 2,300 kilometers with thousands of reefs
    and islands. While it harbors an incredible diversity of marine
    life, including endangered species, it faces serious threats from
    climate change, ocean acidification, and coral bleaching."""

    # Compare pre-generated model responses against the reference (ground truth).
    eval_dataset = pd.DataFrame(
        {
            "response": [
                """The Great Barrier Reef, the world's largest coral reef system located
            in Australia, is a vast and diverse ecosystem. However, it faces serious
            threats from climate change, ocean acidification, and coral bleaching,
            endangering its rich marine life.""",
                """The Great Barrier Reef, a vast coral reef system off the coast of
            Queensland, Australia, is the world's largest. It's a complex ecosystem
            supporting diverse marine life, including endangered species. However,
            climate change, ocean acidification, and coral bleaching are serious
            threats to its survival.""",
                """The Great Barrier Reef, the world's largest coral reef system off the
            coast of Australia, is a vast and diverse ecosystem with thousands of
            reefs and islands. It is home to a multitude of marine life, including
            endangered species, but faces serious threats from climate change, ocean
            acidification, and coral bleaching.""",
            ],
            "reference": [reference_summarization] * 3,
        }
    )
    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            "rouge_1",
            "rouge_2",
            "rouge_l",
            "rouge_l_sum",
        ],
    )
    result = eval_task.evaluate()

    print("Summary Metrics:\n")
    for key, value in result.summary_metrics.items():
        print(f"{key}: \t{value}")

    print("\n\nMetrics Table:\n")
    print(result.metrics_table)
    # Example response:
    #
    # Summary Metrics:
    #
    # row_count:      3
    # rouge_1/mean:   0.7191161666666667
    # rouge_1/std:    0.06765143922270488
    # rouge_2/mean:   0.5441118566666666
    # ...
    # Metrics Table:
    #
    #                                        response                         reference  ...  rouge_l/score  rouge_l_sum/score
    # 0  The Great Barrier Reef, the world's ...  \n    The Great Barrier Reef, the ...  ...       0.577320           0.639175
    # 1  The Great Barrier Reef, a vast coral...  \n    The Great Barrier Reef, the ...  ...       0.552381           0.666667
    # 2  The Great Barrier Reef, the world's ...  \n    The Great Barrier Reef, the ...  ...       0.774775           0.774775
    # [END generativeaionvertexai_evaluation_get_rouge_score]
    return result


if __name__ == "__main__":
    get_rouge_score()
