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

from collections.abc import Iterator
from datetime import datetime, timezone
import io
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import ee
from google.api_core import exceptions
from google.genai import errors
import numpy as np
import pytest

import analyze_storm_risk  # noqa: I100
import fetch_weather_patch
import forecast_precipitation
import load_weather_time_series
import visualize


@pytest.fixture(autouse=True)
def _clear_ee_cache() -> Iterator[None]:
    fetch_weather_patch._EE_CACHE.clear()
    try:
        yield
    finally:
        fetch_weather_patch._EE_CACHE.clear()


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
        patch.object(
            fetch_weather_patch.google.auth,
            "default",
            return_value=(fake_creds, "test-proj"),
        ),
        patch.object(fetch_weather_patch.ee, "Initialize"),
        patch.object(fetch_weather_patch.ee, "ImageCollection"),
        patch.object(fetch_weather_patch.ee, "Image"),
        patch.object(fetch_weather_patch.ee.Geometry, "Point"),
        patch.object(
            fetch_weather_patch.ee.data, "computePixels", return_value=npy_bytes
        ),
    ):
        fetch_weather_patch.fetch_weather_patch("test-project-id")

    captured = capsys.readouterr()
    assert "Display Name: Hurricane Melissa (Jamaica Landfall)" in captured.out
    assert "GOES Collection: NOAA/GOES/19/MCMIPF" in captured.out
    assert "Max Elevation (m): 1850.0" in captured.out
    assert "Peak Precipitation (mm/hr): 42.50" in captured.out
    assert "test-project-id" not in captured.out
    assert "Resource ID:" not in captured.out
    assert captured.err == ""


def test_fetch_weather_patch_rejects_pickled_object_npy(
    capsys: pytest.CaptureFixture[str],
) -> None:
    buf = io.BytesIO()
    np.save(buf, np.array([{"unsafe": True}], dtype=object), allow_pickle=True)
    fake_creds = MagicMock()
    fake_creds.with_quota_project.return_value = fake_creds

    with (
        patch.object(
            fetch_weather_patch.google.auth,
            "default",
            return_value=(fake_creds, "test-proj"),
        ),
        patch.object(fetch_weather_patch.ee, "Initialize"),
        patch.object(fetch_weather_patch.ee, "ImageCollection"),
        patch.object(fetch_weather_patch.ee, "Image"),
        patch.object(fetch_weather_patch.ee.Geometry, "Point"),
        patch.object(
            fetch_weather_patch.ee.data,
            "computePixels",
            return_value=buf.getvalue(),
        ),
    ):
        fetch_weather_patch.fetch_weather_patch("test-project-id")

    captured = capsys.readouterr()
    assert "error: failed to compute Earth Engine weather patch" in captured.err
    assert "pickled" in captured.err.lower() or "object" in captured.err.lower()


def test_fetch_weather_patch_error(capsys: pytest.CaptureFixture[str]) -> None:
    fake_creds = MagicMock()
    fake_creds.with_quota_project.return_value = fake_creds

    with (
        patch.object(
            fetch_weather_patch.google.auth,
            "default",
            return_value=(fake_creds, "test-proj"),
        ),
        patch.object(
            fetch_weather_patch.ee,
            "Initialize",
            side_effect=ee.EEException("Earth Engine API not enabled"),
        ),
    ):
        fetch_weather_patch.fetch_weather_patch("test-project-id")

    captured = capsys.readouterr()
    assert "error: failed to compute Earth Engine weather patch" in captured.err
    assert "Hurricane Melissa (Jamaica Landfall)" in captured.err
    assert "test-project-id" not in captured.err
    assert "Resource ID:" not in captured.err


def test_build_synthetic_storm_patch_and_visualize() -> None:
    melissa = fetch_weather_patch.build_synthetic_storm_patch(
        "melissa_2025", patch_size=32
    )
    sf_bay = fetch_weather_patch.build_synthetic_storm_patch(
        "sf_bay_area", patch_size=32
    )

    assert melissa["goes_satellite"] == "NOAA/GOES/19/MCMIPF"
    assert sf_bay["goes_satellite"] == "NOAA/GOES/18/MCMIPF"
    assert melissa["precipitation"].shape == (32, 32)
    assert melissa["goes_rgb"].shape == (32, 32, 3)

    with (
        patch.object(
            fetch_weather_patch.google.auth,
            "default",
            return_value=(MagicMock(), "offline-test-project"),
        ),
        patch.object(
            fetch_weather_patch.ee,
            "Initialize",
            side_effect=ee.EEException("Offline test"),
        ),
    ):
        pre_2025_storm = fetch_weather_patch.get_storm_patch_arrays(
            project_id="offline-test-project",
            iso_time="2024-09-27T06:00:00",
            latitude=35.60,
            longitude=-82.55,
            storm_name="Custom Historical Storm",
            patch_size=16,
        )
        local_fc = fetch_weather_patch.get_local_weather_forecast(
            project_id="offline-test-project",
            region_name="San Francisco Bay Area, CA",
            latitude=37.7749,
            longitude=-122.4194,
            patch_size=16,
        )
        custom_fc = fetch_weather_patch.get_local_weather_forecast(
            project_id="offline-test-project",
            region_name="Miami, FL",
            latitude=25.7617,
            longitude=-80.1918,
            patch_size=16,
        )
        wn_fc = fetch_weather_patch.get_weathernext_ensemble_forecast(
            project_id="offline-test-project",
        )
    assert pre_2025_storm["goes_satellite"] == "NOAA/GOES/16/MCMIPF"
    assert pre_2025_storm["storm_name"] == "Custom Historical Storm"
    assert local_fc["patch_data"]["goes_satellite"] == "NOAA/GOES/18/MCMIPF"
    assert len(local_fc["forecast_rows"]) == 7
    assert len(local_fc["microclimate_rows"]) == 5
    cities = [m["city"] for m in local_fc["microclimate_rows"]]
    assert cities == [
        "San Francisco",
        "Palo Alto",
        "San Jose",
        "Santa Cruz",
        "Monterey",
    ]
    assert "37.7749°N, 122.4194°W" in local_fc["forecast_context"]

    # Custom non-Bay-Area coordinates omit California 5-city microclimate data.
    assert custom_fc["microclimate_rows"] == []
    assert "25.7617°N, 80.1918°W" in custom_fc["forecast_context"]
    assert "Bay Area" not in custom_fc["forecast_context"]

    micro_fig = visualize.create_bay_area_microclimate_figure(
        local_fc["microclimate_rows"]
    )
    assert len(micro_fig.data) == 3
    assert len(wn_fc["ensemble_rows"]) == 8
    wn_fig = visualize.create_weathernext_ensemble_figure(wn_fc)
    assert len(wn_fig.data) == 5

    # Verify in-memory Earth Engine cache avoids duplicate API calls on repeat runs
    npy_bytes = _make_structured_npy_bytes(patch_size=16)
    fake_creds = MagicMock()
    fake_creds.with_quota_project.return_value = fake_creds
    with (
        patch.object(
            fetch_weather_patch.google.auth,
            "default",
            return_value=(fake_creds, "test-proj"),
        ),
        patch.object(fetch_weather_patch.ee, "Initialize"),
        patch.object(fetch_weather_patch.ee, "ImageCollection"),
        patch.object(fetch_weather_patch.ee, "Image"),
        patch.object(fetch_weather_patch.ee.Geometry, "Point"),
        patch.object(
            fetch_weather_patch.ee.data, "computePixels", return_value=npy_bytes
        ) as mock_compute,
    ):
        first = fetch_weather_patch.get_storm_patch_arrays("cached-proj", patch_size=16)
        second = fetch_weather_patch.get_storm_patch_arrays(
            "cached-proj", patch_size=16
        )
    assert mock_compute.call_count == 1
    assert first["source"] == "Earth Engine Live API"
    assert second["source"] == "Earth Engine Live API (in-memory cache)"

    overview_fig = visualize.create_storm_overview_figure(melissa)
    assert len(overview_fig.data) == 4

    png_bytes = visualize.export_multiband_strip_png_bytes(melissa)
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
            "forecast_timestamp": datetime(2025, 10, 28, 18, tzinfo=timezone.utc),
            "forecasted_precipitation_mm_hr": 45.5,
            "lower_bound_mm_hr": -2.5,
            "upper_bound_mm_hr": 55.0,
        }
    ]
    eval_metrics = visualize.evaluate_forecast_against_ground_truth(fc_rows)
    assert eval_metrics["clamped_negative_bounds"] == 1
    assert eval_metrics["interval_coverage_pct"] == 100.0
    fc_fig = visualize.create_forecast_comparison_figure(
        historical_rows=hist_rows,
        forecast_rows=fc_rows,
        storm_name="Hurricane Melissa",
        holdout_rows=eval_metrics["holdout_rows"],
    )
    assert len(fc_fig.data) == 4


def test_float_or_default_preserves_zero_values() -> None:
    props = {
        "temperature_2m_above_ground": 0.0,
        "elevation": 0.0,
        "rtma_wind_ms": 0.0,
        "missing": None,
    }
    assert (
        fetch_weather_patch._float_or_default(
            props, "temperature_2m_above_ground", 15.0
        )
        == 0.0
    )
    assert fetch_weather_patch._float_or_default(props, "elevation", 15.0) == 0.0
    assert fetch_weather_patch._float_or_default(props, "rtma_wind_ms", 1.5) == 0.0
    assert fetch_weather_patch._float_or_default(props, "missing", 15.0) == 15.0


def test_load_weather_time_series_success(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch.object(
            load_weather_time_series.bigquery, "Client", autospec=True
        ) as mock_bq_cls,
        patch.object(
            load_weather_time_series.beam.io,
            "WriteToBigQuery",
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
    assert "Display Name: storm_hourly_observations" in captured.out
    assert "Dataset ID: weather_forecasting" in captured.out
    assert "Loaded Hours: 36" in captured.out
    assert "Storm Name: Hurricane Melissa" in captured.out
    assert "test-project-id" not in captured.out
    assert "Resource ID:" not in captured.out
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

    with patch.object(
        forecast_precipitation.bigquery, "Client", autospec=True
    ) as mock_bq_cls:
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
    assert "Display Name: storm_hourly_observations" in captured.out
    assert "Forecast Horizon Hours: 2" in captured.out
    assert "Peak Forecasted Precipitation (mm/hr): 36.40" in captured.out
    assert "test-project-id" not in captured.out
    assert "Resource ID:" not in captured.out
    assert captured.err == ""


def test_forecast_precipitation_error(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(
        forecast_precipitation.bigquery, "Client", autospec=True
    ) as mock_bq_cls:
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
    assert "missing_table" in captured.err
    assert "test-project-id" not in captured.err
    assert "Resource ID:" not in captured.err


def test_analyze_storm_risk_success(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    patch_data = fetch_weather_patch.build_synthetic_storm_patch(
        "melissa_2025", patch_size=16
    )
    img_path = tmp_path / "composite.png"
    img_path.write_bytes(visualize.export_multiband_strip_png_bytes(patch_data))

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

    with patch.object(
        analyze_storm_risk.genai, "Client", autospec=True
    ) as mock_genai_cls:
        mock_client = mock_genai_cls.return_value
        mock_client.models.generate_content.return_value = mock_response
        analyze_storm_risk.analyze_storm_risk("test-project-id", str(img_path))

    mock_genai_cls.assert_called_once_with(
        vertexai=True, project="test-project-id", location="global"
    )
    call_kwargs = mock_client.models.generate_content.call_args.kwargs
    assert call_kwargs["model"] == "gemini-3.8-flash"
    assert call_kwargs["config"].system_instruction is not None

    captured = capsys.readouterr()
    assert "Display Name: EXTREME" in captured.out
    assert "Peak Expected Rainfall (mm/hr): 38.4" in captured.out
    assert "test-project-id" not in captured.out
    assert "Resource ID:" not in captured.out
    assert captured.err == ""


def test_analyze_storm_risk_api_and_file_errors(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    img_path = tmp_path / "composite.png"
    img_path.write_bytes(b"\x89PNG\r\n\x1a\n")

    with patch.object(
        analyze_storm_risk.genai, "Client", autospec=True
    ) as mock_genai_cls:
        mock_client = mock_genai_cls.return_value
        mock_client.models.generate_content.side_effect = errors.APIError(
            code=429, response_json={"error": {"message": "Quota exceeded"}}
        )
        analyze_storm_risk.analyze_storm_risk("test-project-id", str(img_path))

    captured = capsys.readouterr()
    assert "error: failed to analyze storm composite" in captured.err
    assert "location 'global'" in captured.err
    assert "test-project-id" not in captured.err

    # Missing file and empty response text are also caught cleanly without tracebacks
    with patch.object(
        analyze_storm_risk.genai, "Client", autospec=True
    ) as mock_genai_cls:
        analyze_storm_risk.analyze_storm_risk(
            "test-project-id", str(tmp_path / "missing.png")
        )
    missing_captured = capsys.readouterr()
    assert "error: failed to analyze storm composite" in missing_captured.err

    empty_response = MagicMock()
    empty_response.text = None
    with patch.object(
        analyze_storm_risk.genai, "Client", autospec=True
    ) as mock_genai_cls:
        mock_genai_cls.return_value.models.generate_content.return_value = (
            empty_response
        )
        analyze_storm_risk.analyze_storm_risk("test-project-id", str(img_path))
    empty_captured = capsys.readouterr()
    assert "error: failed to analyze storm composite" in empty_captured.err
