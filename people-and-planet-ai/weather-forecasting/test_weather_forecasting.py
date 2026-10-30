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

import io
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import analyze_storm_risk

import ee

import fetch_weather_patch

import forecast_precipitation

from google.api_core import exceptions
from google.genai import errors

import load_weather_time_series

import numpy as np

import pytest

import visualize


def _make_structured_npy_bytes(patch_size: int = 8) -> bytes:
    dtype = np.dtype(
        [
            ("precipitation", "<f4"),
            ("CMI_C01", "<f4"),
            ("CMI_C02", "<f4"),
            ("CMI_C03", "<f4"),
            ("CMI_C13", "<f4"),
            ("elevation", "<f4"),
        ]
    )
    arr = np.zeros((patch_size, patch_size), dtype=dtype)
    arr["precipitation"] = 42.5
    arr["CMI_C01"] = 120.0
    arr["CMI_C02"] = 180.0
    arr["CMI_C03"] = 200.0
    arr["CMI_C13"] = 215.0
    arr["elevation"] = 1850.0
    buf = io.BytesIO()
    np.save(buf, arr)
    return buf.getvalue()


def test_fetch_weather_patch_success(capsys: pytest.CaptureFixture[str]) -> None:
    npy_bytes = _make_structured_npy_bytes(patch_size=64)
    fake_creds = MagicMock()
    fake_creds.with_quota_project.return_value = fake_creds

    with (
        patch(
            "fetch_weather_patch.google.auth.default",
            return_value=(fake_creds, "test-proj"),
        ),
        patch("fetch_weather_patch.ee.Initialize"),
        patch("fetch_weather_patch.ee.ImageCollection"),
        patch("fetch_weather_patch.ee.Image"),
        patch("fetch_weather_patch.ee.Geometry.Point"),
        patch("fetch_weather_patch.ee.data.computePixels", return_value=npy_bytes),
    ):
        fetch_weather_patch.fetch_weather_patch("test-project-id")

    captured = capsys.readouterr()
    expected_prefix = (
        "Resource ID: NASA/GPM_L3/IMERG_V07+NOAA/GOES/19/MCMIPF+MERIT/DEM/v1_0_3"
    )
    assert expected_prefix in captured.out
    assert "Display Name: Hurricane Melissa (Jamaica Landfall)" in captured.out
    assert "Max Elevation (m): 1850.0" in captured.out
    assert "Peak Precipitation (mm/hr): 42.50" in captured.out
    assert captured.err == ""


def test_fetch_weather_patch_error(capsys: pytest.CaptureFixture[str]) -> None:
    fake_creds = MagicMock()
    fake_creds.with_quota_project.return_value = fake_creds

    with (
        patch(
            "fetch_weather_patch.google.auth.default",
            return_value=(fake_creds, "test-proj"),
        ),
        patch(
            "fetch_weather_patch.ee.Initialize",
            side_effect=ee.EEException("Earth Engine API not enabled"),
        ),
    ):
        fetch_weather_patch.fetch_weather_patch("test-project-id")

    captured = capsys.readouterr()
    assert "error: failed to compute Earth Engine weather patch" in captured.err
    assert "test-project-id" in captured.err


def test_build_synthetic_storm_patch_and_visualize(tmp_path: Path) -> None:
    melissa = fetch_weather_patch.build_synthetic_storm_patch(
        "melissa_2025", patch_size=32
    )
    helene = fetch_weather_patch.build_synthetic_storm_patch(
        "helene_2024", patch_size=32
    )
    sf_bay = fetch_weather_patch.build_synthetic_storm_patch(
        "sf_bay_area", patch_size=32
    )

    assert melissa["goes_satellite"] == "NOAA/GOES/19/MCMIPF"
    assert helene["goes_satellite"] == "NOAA/GOES/16/MCMIPF"
    assert sf_bay["goes_satellite"] == "NOAA/GOES/18/MCMIPF"
    assert melissa["precipitation"].shape == (32, 32)
    assert melissa["goes_rgb"].shape == (32, 32, 3)

    with patch(
        "fetch_weather_patch.ee.Initialize",
        side_effect=ee.EEException("Offline test"),
    ):
        local_fc = fetch_weather_patch.get_local_weather_forecast(
            project_id="offline-test-project",
            region_name="San Francisco Bay Area, CA",
            latitude=37.7749,
            longitude=-122.4194,
            patch_size=16,
        )
        wn_fc = fetch_weather_patch.get_weathernext_ensemble_forecast(
            project_id="offline-test-project",
        )
    assert (
        local_fc["patch_data"]["goes_satellite"] == "NOAA/GOES/18/MCMIPF"
    )
    assert len(local_fc["forecast_rows"]) == 7
    assert "San Francisco Bay Area, CA" in local_fc["forecast_context"]
    assert len(wn_fc["ensemble_rows"]) == 8
    wn_fig = visualize.create_weathernext_ensemble_figure(wn_fc)
    assert len(wn_fig.data) == 5

    # Verify in-memory Earth Engine cache avoids duplicate API calls on repeat runs
    fetch_weather_patch._EE_CACHE.clear()
    npy_bytes = _make_structured_npy_bytes(patch_size=16)
    fake_creds = MagicMock()
    fake_creds.with_quota_project.return_value = fake_creds
    with (
        patch(
            "fetch_weather_patch.google.auth.default",
            return_value=(fake_creds, "test-proj"),
        ),
        patch("fetch_weather_patch.ee.Initialize"),
        patch("fetch_weather_patch.ee.ImageCollection"),
        patch("fetch_weather_patch.ee.Image"),
        patch("fetch_weather_patch.ee.Geometry.Point"),
        patch(
            "fetch_weather_patch.ee.data.computePixels", return_value=npy_bytes
        ) as mock_compute,
    ):
        first = fetch_weather_patch.get_storm_patch_arrays(
            "cached-proj", "melissa_2025", patch_size=16
        )
        second = fetch_weather_patch.get_storm_patch_arrays(
            "cached-proj", "melissa_2025", patch_size=16
        )
    assert mock_compute.call_count == 1
    assert first["source"] == "Earth Engine Live API"
    assert second["source"] == "Earth Engine Live API (in-memory cache)"
    fetch_weather_patch._EE_CACHE.clear()

    overview_fig = visualize.create_storm_overview_figure(melissa)
    assert len(overview_fig.data) == 3

    png_bytes = visualize.export_composite_png_bytes(melissa)
    assert png_bytes.startswith(b"\x89PNG")

    hist_rows = [
        {
            "observation_time": datetime(2025, 10, 28, 15, tzinfo=timezone.utc),
            "precipitation_mm_hr": 28.0,
        },
        {
            "observation_time": datetime(2025, 10, 28, 16, tzinfo=timezone.utc),
            "precipitation_mm_hr": 45.0,
        },
    ]
    fc_rows = [
        {
            "forecast_timestamp": datetime(2025, 10, 28, 17, tzinfo=timezone.utc),
            "forecasted_precipitation_mm_hr": 38.5,
            "lower_bound_mm_hr": 30.0,
            "upper_bound_mm_hr": 47.0,
        }
    ]
    fc_fig = visualize.create_forecast_comparison_figure(
        historical_rows=hist_rows,
        forecast_rows=fc_rows,
        storm_name="Hurricane Melissa",
    )
    assert len(fc_fig.data) == 3


def test_load_weather_time_series_success(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch("load_weather_time_series.bigquery.Client") as mock_bq_cls,
        patch(
            "load_weather_time_series.beam.io.WriteToBigQuery",
            return_value=load_weather_time_series.beam.Map(lambda row: row),
        ),
    ):
        load_weather_time_series.load_weather_time_series(
            project_id="test-project-id",
            dataset_id="weather_forecasting",
            table_id="storm_hourly_observations",
            beam_args=["--runner=DirectRunner"],
        )

    mock_bq_cls.return_value.create_dataset.assert_called_once_with(
        "test-project-id.weather_forecasting", exists_ok=True
    )
    captured = capsys.readouterr()
    expected_id = (
        "Resource ID: projects/test-project-id/datasets/weather_forecasting/"
        "tables/storm_hourly_observations"
    )
    assert expected_id in captured.out
    assert "Loaded Hours: 36" in captured.out
    assert "Storm Name: Hurricane Melissa" in captured.out
    assert captured.err == ""


def test_forecast_precipitation_success(capsys: pytest.CaptureFixture[str]) -> None:
    fake_rows = [
        SimpleNamespace(
            forecast_timestamp=datetime(2025, 10, 28, 18, 0, tzinfo=timezone.utc),
            forecasted_precipitation_mm_hr=36.4,
            lower_bound_mm_hr=29.1,
            upper_bound_mm_hr=43.8,
        ),
        SimpleNamespace(
            forecast_timestamp=datetime(2025, 10, 28, 19, 0, tzinfo=timezone.utc),
            forecasted_precipitation_mm_hr=24.2,
            lower_bound_mm_hr=18.5,
            upper_bound_mm_hr=30.1,
        ),
    ]
    mock_job = MagicMock()
    mock_job.job_id = "test-job-123"
    mock_job.result.return_value = fake_rows

    with patch("forecast_precipitation.bigquery.Client") as mock_bq_cls:
        mock_bq_cls.return_value.query.return_value = mock_job
        forecast_precipitation.forecast_precipitation(
            project_id="test-project-id",
            dataset_id="weather_forecasting",
            table_id="storm_hourly_observations",
        )

    query_str = mock_bq_cls.return_value.query.call_args[0][0]
    assert "AI.FORECAST" in query_str
    assert "TimesFM 2.5" in query_str
    captured = capsys.readouterr()
    expected_ref = (
        "Resource ID: test-project-id.weather_forecasting.storm_hourly_observations"
    )
    assert expected_ref in captured.out
    assert "Forecast Horizon Hours: 2" in captured.out
    assert "Peak Forecasted Precipitation (mm/hr): 36.40" in captured.out
    assert captured.err == ""


def test_forecast_precipitation_error(capsys: pytest.CaptureFixture[str]) -> None:
    with patch("forecast_precipitation.bigquery.Client") as mock_bq_cls:
        mock_bq_cls.return_value.query.side_effect = exceptions.NotFound(
            "Table not found"
        )
        forecast_precipitation.forecast_precipitation(
            project_id="test-project-id",
            dataset_id="weather_forecasting",
            table_id="missing_table",
        )

    captured = capsys.readouterr()
    assert "error: failed to run AI.FORECAST" in captured.err
    assert "test-project-id.weather_forecasting.missing_table" in captured.err


def test_analyze_storm_risk_success(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    patch_data = fetch_weather_patch.build_synthetic_storm_patch(
        "melissa_2025", patch_size=16
    )
    img_path = tmp_path / "composite.png"
    img_path.write_bytes(visualize.export_composite_png_bytes(patch_data))

    fake_assessment = analyze_storm_risk.StormRiskAssessment(
        storm_summary="Category 5 eyewall rainbands impacting southwestern Jamaica.",
        flood_risk_level="EXTREME",
        orographic_amplification_risk="HIGH — Steep Blue Mountains terrain.",
        peak_expected_rainfall_mm_hr=38.4,
        recommended_actions=[
            "Evacuate low-lying coastal flood zones and mountain river valleys.",
            "Pre-position swift-water rescue teams along southern watersheds.",
        ],
    )
    mock_response = MagicMock()
    mock_response.text = fake_assessment.model_dump_json()

    with patch("analyze_storm_risk.genai.Client") as mock_genai_cls:
        mock_client = mock_genai_cls.return_value
        mock_client.models.generate_content.return_value = mock_response
        analyze_storm_risk.analyze_storm_risk("test-project-id", str(img_path))

    mock_genai_cls.assert_called_once_with(
        vertexai=True, project="test-project-id", location="global"
    )
    call_kwargs = mock_client.models.generate_content.call_args.kwargs
    assert call_kwargs["model"] == "gemini-3.8-flash"

    captured = capsys.readouterr()
    assert f"Resource ID: {img_path}" in captured.out
    assert "Display Name: EXTREME" in captured.out
    assert "Peak Expected Rainfall (mm/hr): 38.4" in captured.out
    assert captured.err == ""


def test_analyze_storm_risk_api_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    img_path = tmp_path / "composite.png"
    img_path.write_bytes(b"\x89PNG\r\n\x1a\n")

    with patch("analyze_storm_risk.genai.Client") as mock_genai_cls:
        mock_client = mock_genai_cls.return_value
        mock_client.models.generate_content.side_effect = errors.APIError(
            code=429, response_json={"error": {"message": "Quota exceeded"}}
        )
        analyze_storm_risk.analyze_storm_risk("test-project-id", str(img_path))

    captured = capsys.readouterr()
    assert "error: failed to analyze storm composite" in captured.err
    assert "location 'global'" in captured.err
    assert "test-project-id" in captured.err
