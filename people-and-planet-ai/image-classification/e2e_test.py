# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from collections.abc import Iterable
import io
import json
import os
from typing import Any
from unittest import mock
import zipfile

import apache_beam as beam
from apache_beam.ml.inference.base import RunInference
from apache_beam.testing.util import assert_that
import pytest

import classify_wildlife_image
import create_images_metadata_table
import embed_wildlife_image
import run_wildlife_inference

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_classify_wildlife_image(capsys: pytest.CaptureFixture[str]) -> None:
    image_uri = "gs://public-datasets-lila/wcs-unzipped/animals/0036/0072.jpg"
    classify_wildlife_image.classify_wildlife_image(
        project_id=PROJECT,
        image_gcs_uri=image_uri,
        habitat_region="Southeast Asia tropical rainforest",
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert f"Resource ID: {image_uri}" in out
    assert "Taxon Family: Tapiridae" in out
    assert "Species: Tapirus indicus" in out


def test_classify_wildlife_image_geofenced_sf_bay(
    capsys: pytest.CaptureFixture[str],
) -> None:
    image_uri = (
        "gs://public-datasets-lila/felidae-conservation-fund/"
        "1/2025-03/53c186d3a51ede0a8a002d10dc9af6a985fbc70d04a17a335847e7179ce1a812.jpg"
    )
    classify_wildlife_image.classify_wildlife_image(
        project_id=PROJECT,
        image_gcs_uri=image_uri,
        habitat_region="San Francisco Bay Area, California, USA",
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert f"Resource ID: {image_uri}" in out
    assert "Taxon Family: Felidae" in out
    assert "Species: Puma concolor" in out
    assert "Habitat Region: San Francisco Bay Area, California, USA" in out


def test_embed_wildlife_image(capsys: pytest.CaptureFixture[str]) -> None:
    image_uri = "gs://public-datasets-lila/wcs-unzipped/animals/0036/0072.jpg"
    embed_wildlife_image.embed_wildlife_image(
        project_id=PROJECT,
        image_gcs_uri=image_uri,
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert f"Resource ID: {image_uri}" in out
    assert "Embedding Dimensions: 768" in out
    assert "Model: gemini-embedding-2" in out


def test_extract_metadata_fn_filters_invalid_categories() -> None:
    sample_metadata = {
        "categories": [
            {"id": 1, "name": "tapirus indicus"},
            {"id": 2, "name": "unknown"},
            {"id": 3, "name": "unknown rodent"},
            {"id": 4, "name": "especie desconocida"},
            {"id": 5, "name": "empty"},
        ],
        "images": [
            {"id": "img1", "file_name": "animals/0036/0072.jpg"},
            {"id": "img2", "file_name": "animals/0000/0001.jpg"},
            {"id": "img3", "file_name": "animals/0000/0002.jpg"},
            {"id": "img4", "file_name": "animals/0000/0003.jpg"},
            {"id": "img5", "file_name": "animals/0000/0004.jpg"},
        ],
        "annotations": [
            {"image_id": "img1", "category_id": 1},
            {"image_id": "img2", "category_id": 2},
            {"image_id": "img3", "category_id": 3},
            {"image_id": "img4", "category_id": 4},
            {"image_id": "img5", "category_id": 5},
        ],
    }
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("wcs_camera_traps.json", json.dumps(sample_metadata))

    mock_response = mock.MagicMock()
    mock_response.content = zip_buffer.getvalue()

    with mock.patch("requests.get", return_value=mock_response):
        fn = create_images_metadata_table._ExtractMetadataFn()
        results = list(fn.process(create_images_metadata_table.METADATA_URL))

    assert results == [
        {"category": "tapirus indicus", "file_name": "animals/0036/0072.jpg"}
    ]


def test_beam_run_inference_with_gemini_model_handler() -> None:
    rows = [
        {"category": "tapirus indicus", "file_name": "animals/0036/0072.jpg"},
        {"category": "tapirus indicus", "file_name": "animals/0036/0072.jpg"},
    ]
    handler = run_wildlife_inference.GeminiWildlifeModelHandler(
        project_id=PROJECT
    )

    def _verify_predictions(actual: Iterable[dict[str, Any]]) -> None:
        results = list(actual)
        assert len(results) == 1
        pred = results[0]
        assert pred["ground_truth_category"] == "tapirus indicus"
        assert pred["taxon_family"] == "Tapiridae"
        assert pred["animal_count"] >= 1
        assert pred["is_empty_or_misfire"] is False
        assert 0.0 <= pred["confidence"] <= 1.0

    with beam.Pipeline() as pipeline:
        predictions = (
            pipeline
            | "CreateRows" >> beam.Create(rows)
            | "KeyBySpecies" >> beam.WithKeys(lambda row: row["category"])
            | "SampleOnePerSpecies" >> beam.combiners.Sample.FixedSizePerKey(1)
            | "DropKey" >> beam.Values()
            | "Flatten" >> beam.FlatMap(lambda s: s)
            | "RunGeminiInference" >> RunInference(handler)
        )
        assert_that(predictions, _verify_predictions)
