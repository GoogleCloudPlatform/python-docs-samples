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

from vertexai.preview.evaluation import EvalResult


def eval_pairwise_summarization_quality(project_id: str):
    # [START generativeaionvertexai_eval_pairwise_summarization_quality]
    import json

    from google import auth
    from google.auth.transport import requests as google_auth_requests

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    creds, _ = auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    data = {
        "pairwise_summarization_quality_input": {
            "metric_spec": {},
            "instance": {
                "prediction": "France is a country located in Western Europe.",
                "baseline_prediction": "France is a country.",
                "instruction": "Summarize the context.",
                "context": (
                    "France is a country located in Western Europe. It's bordered by "
                    "Belgium, Luxembourg, Germany, Switzerland, Italy, Monaco, Spain, "
                    "and Andorra.  France's coastline stretches along the English "
                    "Channel, the North Sea, the Atlantic Ocean, and the Mediterranean "
                    "Sea.  Known for its rich history, iconic landmarks like the Eiffel "
                    "Tower, and delicious cuisine, France is a major cultural and "
                    "economic power in Europe and throughout the world."
                ),
            },
        }
    }

    uri = f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/us-central1:evaluateInstances"
    result = google_auth_requests.AuthorizedSession(creds).post(uri, json=data)

    print(json.dumps(result.json(), indent=2))
    # [END generativeaionvertexai_eval_pairwise_summarization_quality]

    return result


def eval_pairwise_summarization_quality(project_id: str) -> EvalResult:

    # [START generativeaionvertexai_eval_pairwise_summarization_quality]
    import pandas as pd

    import vertexai
    from vertexai.preview.evaluation import EvalTask
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    eval_dataset = pd.DataFrame(
        {
            "instruction": ["Summarize the context."],
            "content": ["Summarize the context."],
            "context": [
                "France is a country located in Western Europe. It's bordered by "
                "Belgium, Luxembourg, Germany, Switzerland, Italy, Monaco, Spain, "
                "and Andorra.  France's coastline stretches along the English "
                "Channel, the North Sea, the Atlantic Ocean, and the Mediterranean "
                "Sea.  Known for its rich history, iconic landmarks like the Eiffel "
                "Tower, and delicious cuisine, France is a major cultural and "
                "economic power in Europe and throughout the world."
            ],
            "baseline_prediction": "France is a country.",
            "response": ["France is a country located in Western Europe."],
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=["pairwise_summarization_quality"],
    )

    model = GenerativeModel("gemini-1.0-pro")

    result = eval_task.evaluate(model=model)

    print(result)
    # [END generativeaionvertexai_eval_pairwise_summarization_quality]
    return result


def eval_rouge(project_id: str) -> EvalResult:

    # [START generativeaionvertexai_eval_rouge]
    import pandas as pd

    import vertexai
    from vertexai.preview.evaluation import EvalTask
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    # eval_dataset = pd.DataFrame(
    #     {
    #         "prediction": "A fast brown fox leaps over a lazy dog.",
    #         "reference": "The quick brown fox jumps over the lazy dog.",
    #     },
    #     {
    #         "prediction": "A quick brown fox jumps over the lazy canine.",
    #         "reference": "The quick brown fox jumps over the lazy dog.",
    #     },
    #     {
    #         "prediction": "The speedy brown fox jumps over the lazy dog.",
    #         "reference": "The quick brown fox jumps over the lazy dog.",
    #     },
    # )

    # eval_task = EvalTask(
    #     dataset=eval_dataset,
    #     metrics=["rouge"],
    # )

    eval_dataset = pd.DataFrame(
        {
            "content": [
                "The Roman Senate was filled with exuberance due to Pompey's defeat in Asia."
            ],
            "reference": [
                "The Roman Senate was filled with exuberance due to successes against Catiline."
            ],
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=["exact_match", "bleu", "rouge"],
    )
    model = GenerativeModel("gemini-1.0-pro")

    result = eval_task.evaluate(model=model)

    print(result)
    # [END generativeaionvertexai_eval_rouge]
    return result


if __name__ == "__main__":
    generate_content("document-ai-test-337818", "us-central1")
