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

# [START aiplatform_sdk_embedding]
import re

from google.cloud import aiplatform
from google.cloud.aiplatform import initializer as aiplatform_init
from google.cloud.aiplatform import pipeline_jobs


def tune_embedding_model(
    api_endpoint: str,
    project: str,
    output_dir: str,
    pipeline_job_display_name: str = "embedding-customization-pipeline-sample",
    base_model_version_id: str = "textembedding-gecko@003",
    task_type: str = "DEFAULT",
    queries_path: str = "gs://embedding-customization-pipeline/dataset/queries.jsonl",
    corpus_path: str = "gs://embedding-customization-pipeline/dataset/corpus.jsonl",
    train_label_path: str = "gs://embedding-customization-pipeline/dataset/train.tsv",
    test_label_path: str = "gs://embedding-customization-pipeline/dataset/test.tsv",
    batch_size: int = 128,
    iterations: int = 1000,
) -> pipeline_jobs.PipelineJob:
    match = re.search(r"^(\w+-\w+)", api_endpoint)
    location = match.group(1) if match else "us-central1"
    job = aiplatform.PipelineJob(
        display_name=pipeline_job_display_name,
        template_path="https://us-kfp.pkg.dev/ml-pipeline/llm-text-embedding/tune-text-embedding-model/v1.1.2",
        pipeline_root=output_dir,
        parameter_values=dict(
            project=project,
            location=location,
            base_model_version_id=base_model_version_id,
            task_type=task_type,
            queries_path=queries_path,
            corpus_path=corpus_path,
            train_label_path=train_label_path,
            test_label_path=test_label_path,
            batch_size=batch_size,
            iterations=iterations,
        ),
    )
    job.submit()
    return job


# [END aiplatform_sdk_embedding]
if __name__ == "__main__":
    tune_embedding_model(
        aiplatform_init.global_config.api_endpoint,
        aiplatform_init.global_config.project,
        aiplatform_init.global_config.staging_bucket,
    )
