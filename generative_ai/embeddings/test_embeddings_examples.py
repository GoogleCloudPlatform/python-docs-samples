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

import backoff

from google.api_core.exceptions import FailedPrecondition, ResourceExhausted

import google.auth

from google.cloud import aiplatform
from google.cloud.aiplatform import initializer as aiplatform_init


import batch_example
import code_retrieval_example
import document_retrieval_example
import generate_embeddings_with_lower_dimension
import model_tuning_example
import multimodal_example
import multimodal_image_example
import multimodal_video_example
import normalize_embeddings


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_embed_text_batch() -> None:
    batch_prediction_job = batch_example.embed_text_batch("gs://python-docs-samples-tests/")
    assert batch_prediction_job


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_multimodal_embedding_image_video_text() -> None:
    embeddings = multimodal_example.get_image_video_text_embeddings()
    assert embeddings is not None
    assert embeddings.image_embedding is not None
    assert embeddings.video_embeddings is not None
    assert embeddings.text_embedding is not None


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_multimodal_embedding_video() -> None:
    embeddings = multimodal_video_example.get_video_embeddings()
    assert embeddings is not None
    assert embeddings.video_embeddings is not None


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_multimodal_embedding_image() -> None:
    embeddings = multimodal_image_example.get_image_text_embeddings()
    assert embeddings is not None
    assert embeddings.image_embedding is not None
    assert embeddings.text_embedding is not None


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_generate_embeddings_with_lower_dimension() -> None:
    embeddings = (
        generate_embeddings_with_lower_dimension.generate_embeddings_with_lower_dimension()
    )
    assert embeddings is not None
    assert embeddings.image_embedding is not None
    assert len(embeddings.image_embedding) == 128
    assert embeddings.text_embedding is not None
    assert len(embeddings.text_embedding) == 128


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_text_embed_text() -> None:
    embeddings = document_retrieval_example.embed_text()
    assert [len(e) for e in embeddings] == [3072, 3072]


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_embed_text() -> None:
    texts = [
        "banana bread?",
        "banana muffin?",
        "banana?",
    ]
    dimensionality = 256
    embeddings = code_retrieval_example.embed_text(
        texts=texts,
        task="CODE_RETRIEVAL_QUERY",
        dimensionality=dimensionality,
    )
    assert [len(e) for e in embeddings] == [dimensionality or 768] * len(texts)


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_embedding_normalization() -> None:
    import numpy as np

    embedding_value = [0.01] * 256
    embedding_np = np.linalg.norm(np.array(embedding_value))
    assert np.isclose(np.linalg.norm(embedding_np), 0.16)

    normalized_embedding_np = normalize_embeddings.normalize_embedding(embedding_np)
    assert np.isclose(np.linalg.norm(normalized_embedding_np), 1)

    invalid_embedding_np = np.linalg.norm(np.array([0]))
    normalized_embedding_np = normalize_embeddings.normalize_embedding(invalid_embedding_np)
    assert np.isclose(np.linalg.norm(normalized_embedding_np), 0)


@backoff.on_exception(backoff.expo, FailedPrecondition, max_time=300)
def dispose(tuning_job) -> None:  # noqa: ANN001
    if tuning_job._status.name == "PIPELINE_STATE_RUNNING":
        tuning_job._cancel()


def test_tune_embedding_model() -> None:
    credentials, _ = google.auth.default(  # Set explicit credentials with Oauth scopes.
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    aiplatform.init(
        api_endpoint="us-central1-aiplatform.googleapis.com:443",
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        staging_bucket="gs://ucaip-samples-us-central1/training_pipeline_output",
        credentials=credentials,
    )
    tuning_job = model_tuning_example.tune_embedding_model(
        aiplatform_init.global_config.api_endpoint
    )
    try:
        assert tuning_job._status.name != "PIPELINE_STATE_FAILED"
    finally:
        dispose(tuning_job)
