#!/usr/bin/env python

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

"""Visualization utilities for Earth Engine satellite patches and BigQuery forecasts."""

from __future__ import annotations

from datetime import datetime, timedelta
import io
import math
from typing import Any

import numpy as np
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import load_weather_time_series  # noqa: I100

# NASA GPM IMERG rainfall radar color scale (0.0 to 45.0+ mm/hr).
_GPM_PRECIPITATION_PALETTE: list[str] = [
    "0a1832",  # Very dark navy (0 mm/hr)
    "0050d5",  # Deep blue
    "00b4ff",  # Cyan blue
    "33db80",  # Emerald green
    "9beb4a",  # Lime green
    "ffeb00",  # Yellow
    "ffb300",  # Amber
    "ff5000",  # Orange red
    "d60000",  # Crimson
    "7a0068",  # Extreme magenta (>45 mm/hr)
]

# Hypsometric terrain relief color scale (0 m sea level to 2,200+ m alpine peaks).
_MERIT_DEM_PALETTE: list[str] = [
    "0b2545",  # Ocean / sea level (0m)
    "2d6a4f",  # Coastal lowland green
    "74c69d",  # Foothills green
    "d9ed92",  # Upland yellow-green
    "ddb892",  # Highland tan
    "9c6644",  # Mountain brown
    "7f4f24",  # High ridge sienna
    "f8f9fa",  # Alpine peak (>2000m)
]


def render_palette(
    values: np.ndarray,
    palette: list[str],
    min_val: float = 0.0,
    max_val: float = 1.0,
) -> np.ndarray:
    """Renders a 2D numeric NumPy array as an RGB uint8 image using a hex palette.

    Normalizes raw physical sensor values (such as rainfall rate in mm/hr or
    terrain elevation in meters) into a 256-step linearly interpolated RGB
    lookup table so disparate satellite and terrain bands can be inspected
    visually or passed as RGB imagery to multimodal models.

    Args:
        values: 2D float array with shape (height, width).
        palette: List of 6-character hex color strings (without leading '#').
        min_val: Physical value mapped to the first color in the palette.
        max_val: Physical value mapped to the final color in the palette.

    Returns:
        An RGB uint8 array with shape (height, width, 3).
    """
    xs = np.linspace(0, len(palette) - 1, 256)
    indices = np.arange(len(palette))

    red = np.interp(xs, indices, [int(c[0:2], 16) for c in palette])
    green = np.interp(xs, indices, [int(c[2:4], 16) for c in palette])
    blue = np.interp(xs, indices, [int(c[4:6], 16) for c in palette])
    color_map = np.stack([red, green, blue], axis=-1).astype(np.uint8)

    denom = max(max_val - min_val, 1e-6)
    scaled = np.clip((values - min_val) / denom, 0.0, 1.0)
    color_indices = (scaled * 255).astype(np.uint8)
    return color_map[color_indices]


def render_gpm_precipitation(precipitation_mm_hr: np.ndarray) -> np.ndarray:
    """Renders GPM IMERG V07 precipitation (mm/hr) using the NASA rainfall palette.

    Maps half-hourly surface rain rates across `0.0` to `45.0 mm/hr` onto a
    high-contrast meteorological radar color scale (dark navy for dry sky,
    cyan/green for light-to-moderate rain, yellow/amber for heavy rain, and
    crimson/magenta for extreme hurricane eyewall convection).

    Args:
        precipitation_mm_hr: 2D float array of surface rain rates in mm/hr.

    Returns:
        An RGB uint8 array with shape (height, width, 3) representing rainfall
        intensity.
    """
    return render_palette(
        precipitation_mm_hr, _GPM_PRECIPITATION_PALETTE, min_val=0.0, max_val=45.0
    )


def render_elevation_dem(elevation_m: np.ndarray) -> np.ndarray:
    """Renders MERIT DEM surface elevation (meters) using a terrain relief palette.

    Maps elevation values from `0 m` (sea level) to `2,200 m` (high mountain
    ridges such as Jamaica's Blue Mountains or the Southern Appalachians) onto
    a hypsometric tint scale so coastal plains, foothills, and steep windward
    escarpments are visually distinct.

    Args:
        elevation_m: 2D float array of terrain elevation in meters above sea level.

    Returns:
        An RGB uint8 array with shape (height, width, 3) representing terrain
        topography.
    """
    return render_palette(elevation_m, _MERIT_DEM_PALETTE, min_val=0.0, max_val=2200.0)


def render_storm_terrain_overlay(
    goes_rgb: np.ndarray,
    precipitation_mm_hr: np.ndarray,
    elevation_m: np.ndarray,
) -> np.ndarray:
    """Alpha-blends GOES clouds and GPM rainbands onto MERIT DEM topography.

    Combines all three aligned Earth Engine rasters into a single co-registered
    composite image to reveal orographic amplification—showing where moist
    spiraling rainbands (`>= 1.2 mm/hr`) directly collide with steep mountain
    ridges.

    Args:
        goes_rgb: 3D uint8 array `(height, width, 3)` of GOES cloud and moisture
            imagery.
        precipitation_mm_hr: 2D float array `(height, width)` of GPM IMERG
            precipitation rates in mm/hr.
        elevation_m: 2D float array `(height, width)` of MERIT DEM terrain
            elevation in meters.

    Returns:
        An RGB uint8 array with shape `(height, width, 3)` blending terrain,
        translucent cloud cover, and high-opacity radar rainbands.
    """
    elev_rgb = render_elevation_dem(elevation_m).astype(np.float32)
    precip_rgb = render_gpm_precipitation(precipitation_mm_hr).astype(np.float32)
    goes_float = goes_rgb.astype(np.float32)

    # 1. Translucent cloud layer over terrain/ocean (up to 35% opacity)
    cloud_brightness = np.mean(goes_float, axis=-1, keepdims=True)
    cloud_alpha = np.clip((cloud_brightness - 55.0) / 195.0, 0.0, 1.0) * 0.35
    blended = elev_rgb * (1.0 - cloud_alpha) + goes_float * cloud_alpha

    # 2. High-opacity radar rainbands where precipitation >= 1.2 mm/hr
    rain_alpha = np.clip((precipitation_mm_hr[..., np.newaxis] - 1.2) / 22.0, 0.0, 0.82)
    blended = blended * (1.0 - rain_alpha) + precip_rgb * rain_alpha
    return np.clip(blended, 0.0, 255.0).astype(np.uint8)


def _render_four_panel_arrays(
    patch_data: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Renders the 4 aligned RGB panels (GOES, GPM, DEM, and Terrain Overlay).

    Centralizes the conversion of raw physical storm arrays into uint8 RGB
    images so both the interactive Plotly figure (`create_storm_overview_figure`)
    and the multimodal PNG strip exporter (`export_multiband_strip_png_bytes`)
    use identical visual encodings.

    Args:
        patch_data: Dictionary containing `'goes_rgb'`, `'precipitation'`, and
            `'elevation'` NumPy arrays.

    Returns:
        A 4-tuple `(goes_rgb, precip_rgb, elev_rgb, overlay_rgb)` of uint8 RGB
        arrays.
    """
    goes_rgb = patch_data["goes_rgb"]
    precip_rgb = render_gpm_precipitation(patch_data["precipitation"])
    elev_rgb = render_elevation_dem(patch_data["elevation"])
    overlay_rgb = render_storm_terrain_overlay(
        goes_rgb, patch_data["precipitation"], patch_data["elevation"]
    )
    return goes_rgb, precip_rgb, elev_rgb, overlay_rgb


def create_storm_overview_figure(patch_data: dict[str, Any]) -> go.Figure:
    """Creates a 4-panel Plotly figure for GOES, GPM, DEM, and Terrain Overlay.

    Displays the three individual sensor channels (`GOES` cloud/moisture at
    2 km native resolution, `GPM IMERG` rainfall at 10 km resolution, and
    `MERIT DEM` elevation) side-by-side with the 4th alpha-blended spatial
    overlay so analysts can compare raw sensor values against topographic
    rainband alignment.

    Args:
        patch_data: Dictionary returned by `fetch_weather_patch.get_storm_patch_arrays`
            containing `'goes_rgb'`, `'precipitation'`, `'elevation'`,
            `'storm_name'`, `'iso_time'`, and `'goes_satellite'`.

    Returns:
        A 4-column `plotly.graph_objects.Figure` ready for interactive display.
    """
    goes_rgb, precip_rgb, elev_rgb, overlay_rgb = _render_four_panel_arrays(patch_data)

    fig = make_subplots(
        rows=1,
        cols=4,
        subplot_titles=(
            f"1. {patch_data.get('goes_satellite', 'GOES')} (2 km)",
            "2. GPM IMERG Rainfall (10 km, mm/hr)",
            "3. MERIT DEM Terrain (m)",
            "4. Rainbands Overlaid on Terrain",
        ),
        horizontal_spacing=0.03,
    )
    for col_idx, panel_rgb in enumerate(
        (goes_rgb, precip_rgb, elev_rgb, overlay_rgb), start=1
    ):
        fig.add_trace(go.Image(z=panel_rgb), row=1, col=col_idx)

    peak_rain = float(np.max(patch_data["precipitation"]))
    max_elev = float(np.max(patch_data["elevation"]))
    title_text = (
        f"<b>{patch_data.get('storm_name', 'Storm Observation')}</b> — "
        f"{patch_data.get('iso_time', '')} "
        f"(Peak Rain: {peak_rain:.1f} mm/hr | Max Terrain: {max_elev:.0f} m)"
    )
    fig.update_layout(
        title=dict(text=title_text, x=0.5),
        height=380,
        margin=dict(l=12, r=12, t=65, b=12),
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig


def export_multiband_strip_png_bytes(patch_data: dict[str, Any]) -> bytes:
    """Stitches GOES, GPM rainfall, MERIT DEM, and Terrain Overlay into a PNG.

    Packages the three unoccluded sensor panels alongside the 4th spatial
    overlay into a single horizontally concatenated PNG byte stream (upscaled
    3x with nearest-neighbor resampling to preserve crisp pixel boundaries) for
    multimodal reasoning with Gemini 3.8 Flash (`types.Part.from_bytes`).

    Args:
        patch_data: Dictionary containing `'goes_rgb'`, `'precipitation'`, and
            `'elevation'` NumPy arrays for the region of interest.

    Returns:
        PNG-encoded image bytes containing the 4-panel horizontal strip.
    """
    goes_rgb, precip_rgb, elev_rgb, overlay_rgb = _render_four_panel_arrays(patch_data)

    height = goes_rgb.shape[0]
    separator = np.full((height, 4, 3), 255, dtype=np.uint8)
    combined = np.concatenate(
        [
            goes_rgb,
            separator,
            precip_rgb,
            separator,
            elev_rgb,
            separator,
            overlay_rgb,
        ],
        axis=1,
    )
    pil_image = Image.fromarray(combined, mode="RGB")
    pil_image = pil_image.resize(
        (combined.shape[1] * 3, combined.shape[0] * 3),
        resample=Image.Resampling.NEAREST,
    )
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return buffer.getvalue()


def build_storm_holdout_labels(horizon: int = 6) -> list[dict[str, Any]]:
    """Returns the 6-hour post-landfall ground-truth GPM IMERG labels.

    Continues the Hurricane Melissa hourly precipitation series for hours
    `+36..+41` (`2025-10-28 18:00 UTC` to `23:00 UTC`) held out from the
    36-hour input table so users can score the zero-shot TimesFM 2.5 hindcast
    against unseen post-landfall observations.

    Args:
        horizon: Number of future holdout hours to generate (default: 6).

    Returns:
        List of dictionaries with `'forecast_timestamp'` and
        `'actual_precipitation_mm_hr'`.
    """
    base_time = datetime(2025, 10, 27, 6, 0, 0)
    return [
        {
            "forecast_timestamp": (base_time + timedelta(hours=36 + step)).strftime(
                "%Y-%m-%d %H:%M:%S+00:00"
            ),
            "actual_precipitation_mm_hr": (
                load_weather_time_series.compute_melissa_hourly_rainfall(36 + step)
            ),
        }
        for step in range(horizon)
    ]


def evaluate_forecast_against_ground_truth(
    forecast_rows: list[dict[str, Any]],
    holdout_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evaluates AI.FORECAST predictions against 6-hour holdout ground truth.

    Applies physical non-negativity clamping (`max(0.0, x)`, analogous to a
    neural network ReLU output layer) to the predicted precipitation values and
    lower confidence bounds, then computes Mean Absolute Error (MAE), Root Mean
    Squared Error (RMSE), and 90% prediction interval coverage against the
    held-out GPM IMERG observations.

    Args:
        forecast_rows: List of dictionaries returned by BigQuery `AI.FORECAST`
            containing `'forecast_timestamp'`,
            `'forecasted_precipitation_mm_hr'`, `'lower_bound_mm_hr'`, and
            `'upper_bound_mm_hr'`.
        holdout_rows: Optional list of ground-truth dictionaries containing
            `'actual_precipitation_mm_hr'`. Defaults to
            `build_storm_holdout_labels`.

    Returns:
        Dictionary containing `'mae_mm_hr'`, `'rmse_mm_hr'`,
        `'interval_coverage_pct'`, `'clamped_negative_bounds'`, and
        `'holdout_rows'`.
    """
    if holdout_rows is None:
        holdout_rows = build_storm_holdout_labels(horizon=len(forecast_rows))

    abs_errors: list[float] = []
    sq_errors: list[float] = []
    inside_interval = 0
    clamped_negative_bounds = 0

    for fc, gt in zip(forecast_rows, holdout_rows):
        pred = max(0.0, float(fc["forecasted_precipitation_mm_hr"]))
        raw_lower = float(fc["lower_bound_mm_hr"])
        if raw_lower < 0.0:
            clamped_negative_bounds += 1
        lower = max(0.0, raw_lower)
        upper = float(fc["upper_bound_mm_hr"])
        actual = float(gt["actual_precipitation_mm_hr"])

        err = abs(pred - actual)
        abs_errors.append(err)
        sq_errors.append(err**2)
        if lower <= actual <= upper:
            inside_interval += 1

    n = max(1, len(abs_errors))
    return {
        "mae_mm_hr": round(sum(abs_errors) / n, 2),
        "rmse_mm_hr": round(math.sqrt(sum(sq_errors) / n), 2),
        "interval_coverage_pct": round(100.0 * inside_interval / n, 1),
        "clamped_negative_bounds": clamped_negative_bounds,
        "holdout_rows": holdout_rows,
    }


def _add_confidence_band_trace(
    fig: go.Figure,
    timestamps: list[Any],
    lower_bounds: list[float],
    upper_bounds: list[float],
    fillcolor: str,
    name: str,
) -> None:
    """Adds a shaded closed-polygon confidence or percentile band to a figure.

    Constructs a forward-and-reverse (`timestamps + timestamps[::-1]`) polygon
    trace with `fill='toself'` so uncertainty intervals (`90% CI`, `p10–p90`,
    or `p25–p75`) render as a single legend item without border lines.

    Args:
        fig: Target `plotly.graph_objects.Figure`.
        timestamps: Sequence of x-axis timestamps.
        lower_bounds: Sequence of lower interval values matching `timestamps`.
        upper_bounds: Sequence of upper interval values matching `timestamps`.
        fillcolor: RGBA fill color string (for example, `'rgba(255,99,71,0.2)'`).
        name: Legend label for the uncertainty band.
    """
    fig.add_trace(
        go.Scatter(
            x=timestamps + timestamps[::-1],
            y=upper_bounds + lower_bounds[::-1],
            fill="toself",
            fillcolor=fillcolor,
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name=name,
        )
    )


def _apply_standard_chart_layout(
    fig: go.Figure,
    title: str,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
    height: int = 430,
) -> go.Figure:
    """Applies consistent styling, white template, and top legend to a figure.

    Args:
        fig: Target `plotly.graph_objects.Figure`.
        title: HTML-formatted chart title.
        xaxis_title: Optional x-axis label.
        yaxis_title: Optional y-axis label.
        height: Figure height in pixels (default: 430).

    Returns:
        The styled `plotly.graph_objects.Figure`.
    """
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        height=height,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_forecast_comparison_figure(
    historical_rows: list[dict[str, Any]],
    forecast_rows: list[dict[str, Any]],
    storm_name: str,
    holdout_rows: list[dict[str, Any]] | None = None,
) -> go.Figure:
    """Creates a Plotly chart comparing inputs, AI.FORECAST, and ground truth.

    Visualizes the end-to-end hindcast evaluation by plotting the 36-hour
    historical GPM IMERG input context alongside BigQuery ML's 6-hour
    `AI.FORECAST` (`TimesFM 2.5`) trajectory, its ReLU-clamped 90% confidence
    band, and the actual observed 6-hour ground-truth labels.

    Args:
        historical_rows: List of dictionaries with `'observation_time'` and
            `'precipitation_mm_hr'` representing the 36-hour input context.
        forecast_rows: List of dictionaries with `'forecast_timestamp'`,
            `'forecasted_precipitation_mm_hr'`, `'lower_bound_mm_hr'`, and
            `'upper_bound_mm_hr'`.
        storm_name: Display title of the storm event.
        holdout_rows: Optional list of held-out ground-truth dictionaries with
            `'actual_precipitation_mm_hr'`.

    Returns:
        A `plotly.graph_objects.Figure` comparing historical inputs, forecast
        intervals, and ground-truth observations.
    """
    if holdout_rows is None:
        holdout_rows = build_storm_holdout_labels(horizon=len(forecast_rows))

    hist_times = [r["observation_time"] for r in historical_rows]
    hist_precip = [float(r["precipitation_mm_hr"]) for r in historical_rows]

    fc_times = [r["forecast_timestamp"] for r in forecast_rows]
    fc_vals = [
        max(0.0, float(r["forecasted_precipitation_mm_hr"])) for r in forecast_rows
    ]
    fc_lower = [max(0.0, float(r["lower_bound_mm_hr"])) for r in forecast_rows]
    fc_upper = [float(r["upper_bound_mm_hr"]) for r in forecast_rows]

    fig = go.Figure()

    _add_confidence_band_trace(
        fig,
        timestamps=fc_times,
        lower_bounds=fc_lower,
        upper_bounds=fc_upper,
        fillcolor="rgba(255, 99, 71, 0.20)",
        name="TimesFM 2.5 90% Interval (ReLU Clamped >= 0)",
    )
    fig.add_trace(
        go.Scatter(
            x=hist_times,
            y=hist_precip,
            mode="lines+markers",
            name="Observed GPM Inputs (36h Past Context)",
            line=dict(color="#0064ff", width=2.5),
        )
    )
    if holdout_rows:
        gt_vals = [float(r["actual_precipitation_mm_hr"]) for r in holdout_rows]
        fig.add_trace(
            go.Scatter(
                x=fc_times[: len(gt_vals)],
                y=gt_vals,
                mode="lines+markers",
                name="Observed GPM Ground-Truth Labels (6h Holdout)",
                line=dict(color="#00a65a", width=2.8),
                marker=dict(symbol="diamond", size=8),
            )
        )
    fig.add_trace(
        go.Scatter(
            x=fc_times,
            y=fc_vals,
            mode="lines+markers",
            name="BigQuery AI.FORECAST (TimesFM 2.5) Hindcast",
            line=dict(color="#eb1e00", width=3, dash="dash"),
        )
    )
    return _apply_standard_chart_layout(
        fig,
        title=(
            f"<b>Storm Hindcast Evaluation ({storm_name})</b> — "
            "36h GPM Inputs vs. 6h TimesFM 2.5 Hindcast & Ground-Truth Labels"
        ),
        xaxis_title="Timestamp (UTC)",
        yaxis_title="Precipitation Rate (mm/hr)",
    )


def create_weathernext_ensemble_figure(
    ensemble_data: dict[str, Any],
) -> go.Figure:
    """Creates a Plotly ensemble plume chart for WeatherNext 3 percentiles.

    Visualizes the probabilistic spread across Google DeepMind's 64-member
    WeatherNext 3 ensemble (`weathernext_3_0_0_0p1deg`), rendering the outer
    `p10–p90` band (80% of ensemble members), the inner `p25–p75` interquartile
    band, the `p50` median, the ensemble `mean`, and the `p90` worst-case
    tail-risk trajectory used for flood preparedness.

    Args:
        ensemble_data: Dictionary returned by
            `fetch_weather_patch.get_weathernext_ensemble_forecast` containing
            `'region_name'` and `'ensemble_rows'` (`p10_mm_hr`, `p25_mm_hr`,
            `p50_mm_hr`, `p75_mm_hr`, `p90_mm_hr`, `mean_mm_hr`).

    Returns:
        A `plotly.graph_objects.Figure` showing the 48-hour probabilistic
        ensemble plume.
    """
    rows = ensemble_data["ensemble_rows"]
    times = [r["valid_time_utc"] for r in rows]
    p10 = [float(r["p10_mm_hr"]) for r in rows]
    p25 = [float(r["p25_mm_hr"]) for r in rows]
    p50 = [float(r["p50_mm_hr"]) for r in rows]
    p75 = [float(r["p75_mm_hr"]) for r in rows]
    p90 = [float(r["p90_mm_hr"]) for r in rows]
    mean_vals = [float(r["mean_mm_hr"]) for r in rows]

    fig = go.Figure()

    _add_confidence_band_trace(
        fig,
        timestamps=times,
        lower_bounds=p10,
        upper_bounds=p90,
        fillcolor="rgba(30, 136, 229, 0.16)",
        name="p10–p90 Spread (80% of 64 Members)",
    )
    _add_confidence_band_trace(
        fig,
        timestamps=times,
        lower_bounds=p25,
        upper_bounds=p75,
        fillcolor="rgba(30, 136, 229, 0.34)",
        name="p25–p75 Interquartile Range (50% of Members)",
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=p50,
            mode="lines+markers",
            name="Ensemble Median (p50)",
            line=dict(color="#0d47a1", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=mean_vals,
            mode="lines+markers",
            name="Ensemble Mean (mean)",
            line=dict(color="#d81b60", width=2.5, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=p90,
            mode="lines",
            name="p90 Worst-Case Tail Risk (90th Percentile)",
            line=dict(color="#ff6f00", width=1.8, dash="dot"),
        )
    )
    return _apply_standard_chart_layout(
        fig,
        title=(
            f"<b>WeatherNext 3 (64-Member Ensemble)</b> — "
            f"{ensemble_data.get('region_name', 'Probabilistic Rainfall Forecast')}"
        ),
        xaxis_title="Valid Forecast Time (UTC)",
        yaxis_title="1-Hour Precipitation Rate (mm/hr)",
    )


def create_bay_area_microclimate_figure(
    microclimate_rows: list[dict[str, Any]],
) -> go.Figure:
    """Creates a Plotly chart comparing 5 Bay Area & Monterey Bay microclimates.

    Contrasts current 2.5 km NOAA RTMA surface temperatures against +24h NOAA
    GFS temperature and relative humidity forecasts across five coastal,
    rain-shadowed, and inland valley microclimate zones (`San Francisco`,
    `Palo Alto`, `San Jose`, `Santa Cruz`, and `Monterey`).

    Args:
        microclimate_rows: List of dictionaries returned in the
            `'microclimate_rows'` key of
            `fetch_weather_patch.get_local_weather_forecast`, containing
            `'city'`, `'microclimate_zone'`, `'current_temp_c'`,
            `'forecast_24h_temp_c'`, and `'forecast_24h_rh_pct'`.

    Returns:
        A dual-axis `plotly.graph_objects.Figure` comparing temperature bars
        (left axis) and relative humidity (right axis) across microclimates.
    """
    labels = [
        f"{r['city']}<br><sup>{r['microclimate_zone']}</sup>" for r in microclimate_rows
    ]
    current_c = [float(r["current_temp_c"]) for r in microclimate_rows]
    fc24_c = [float(r["forecast_24h_temp_c"]) for r in microclimate_rows]
    rh_pct = [float(r["forecast_24h_rh_pct"]) for r in microclimate_rows]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=labels,
            y=current_c,
            name="Current 2.5km RTMA Temp (°C)",
            marker_color="#1e88e5",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(
            x=labels,
            y=fc24_c,
            name="+24h NOAA GFS Forecast Temp (°C)",
            marker_color="#fb8c00",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=rh_pct,
            mode="lines+markers",
            name="+24h Relative Humidity (%)",
            line=dict(color="#00897b", width=3),
            marker=dict(size=9),
        ),
        secondary_y=True,
    )
    _apply_standard_chart_layout(
        fig,
        title=(
            "<b>San Francisco & Monterey Bay Microclimate Comparison</b> — "
            "Coastal Marine Gaps vs. Rain-Shadowed Valleys"
        ),
        height=420,
    )
    fig.update_layout(barmode="group")
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(
        title_text="Relative Humidity (%)", range=[0, 100], secondary_y=True
    )
    return fig
