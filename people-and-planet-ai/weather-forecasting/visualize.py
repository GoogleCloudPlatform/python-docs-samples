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

import io
from typing import Any

from PIL import Image

import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def render_palette(
    values: np.ndarray,
    palette: list[str],
    min_val: float = 0.0,
    max_val: float = 1.0,
) -> np.ndarray:
    """Renders a 2D numeric NumPy array as an RGB uint8 image using a hex palette.

    Args:
        values: 2D float array with shape (height, width).
        palette: List of 6-character hex color strings (without leading '#').
        min_val: Value mapped to the start of the palette.
        max_val: Value mapped to the end of the palette.

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
    """Renders GPM IMERG V07 precipitation (mm/hr) using the NASA rainfall palette."""
    palette = [
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
    return render_palette(precipitation_mm_hr, palette, min_val=0.0, max_val=45.0)


def render_elevation_dem(elevation_m: np.ndarray) -> np.ndarray:
    """Renders MERIT DEM surface elevation (meters) using a terrain relief palette."""
    palette = [
        "0b2545",  # Ocean / sea level (0m)
        "2d6a4f",  # Coastal lowland green
        "74c69d",  # Foothills green
        "d9ed92",  # Upland yellow-green
        "ddb892",  # Highland tan
        "9c6644",  # Mountain brown
        "7f4f24",  # High ridge sienna
        "f8f9fa",  # Alpine peak (>2000m)
    ]
    return render_palette(elevation_m, palette, min_val=0.0, max_val=2200.0)


def create_storm_overview_figure(patch_data: dict[str, Any]) -> go.Figure:
    """Creates a 3-panel Plotly figure for GOES, GPM IMERG V07, and MERIT DEM."""
    goes_rgb = patch_data["goes_rgb"]
    precip_rgb = render_gpm_precipitation(patch_data["precipitation"])
    elev_rgb = render_elevation_dem(patch_data["elevation"])

    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            f"1. {patch_data.get('goes_satellite', 'GOES')} Cloud & Moisture",
            "2. NASA GPM IMERG V07 Rainfall (mm/hr)",
            "3. MERIT DEM Terrain Elevation (m)",
        ),
        horizontal_spacing=0.04,
    )
    fig.add_trace(go.Image(z=goes_rgb), row=1, col=1)
    fig.add_trace(go.Image(z=precip_rgb), row=1, col=2)
    fig.add_trace(go.Image(z=elev_rgb), row=1, col=3)

    peak_rain = float(np.max(patch_data["precipitation"]))
    max_elev = float(np.max(patch_data["elevation"]))
    title_text = (
        f"<b>{patch_data.get('storm_name', 'Storm Observation')}</b> — "
        f"{patch_data.get('iso_time', '')} "
        f"(Peak Rain: {peak_rain:.1f} mm/hr | Max Terrain: {max_elev:.0f} m)"
    )
    fig.update_layout(
        title=dict(text=title_text, x=0.5),
        height=390,
        margin=dict(l=15, r=15, t=65, b=15),
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig


def export_composite_png_bytes(patch_data: dict[str, Any]) -> bytes:
    """Stitches GOES RGB, GPM IMERG rainfall, and MERIT DEM into a single PNG.

    Used to pass a multi-band visual composite directly to Gemini 3.8 Flash
    via `types.Part.from_bytes(data=..., mime_type='image/png')`.
    """
    goes_rgb = patch_data["goes_rgb"]
    precip_rgb = render_gpm_precipitation(patch_data["precipitation"])
    elev_rgb = render_elevation_dem(patch_data["elevation"])

    height = goes_rgb.shape[0]
    separator = np.full((height, 4, 3), 255, dtype=np.uint8)
    combined = np.concatenate(
        [goes_rgb, separator, precip_rgb, separator, elev_rgb], axis=1
    )
    pil_image = Image.fromarray(combined, mode="RGB")
    pil_image = pil_image.resize(
        (combined.shape[1] * 3, combined.shape[0] * 3),
        resample=Image.Resampling.NEAREST,
    )
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return buffer.getvalue()


def create_forecast_comparison_figure(
    historical_rows: list[dict[str, Any]],
    forecast_rows: list[dict[str, Any]],
    storm_name: str,
) -> go.Figure:
    """Creates a Plotly chart comparing observed GPM rainfall and AI.FORECAST."""
    hist_times = [r["observation_time"] for r in historical_rows]
    hist_precip = [float(r["precipitation_mm_hr"]) for r in historical_rows]

    fc_times = [r["forecast_timestamp"] for r in forecast_rows]
    fc_vals = [float(r["forecasted_precipitation_mm_hr"]) for r in forecast_rows]
    fc_lower = [
        max(0.0, float(r["lower_bound_mm_hr"])) for r in forecast_rows
    ]
    fc_upper = [float(r["upper_bound_mm_hr"]) for r in forecast_rows]

    fig = go.Figure()

    # 90% confidence interval band
    fig.add_trace(
        go.Scatter(
            x=fc_times + fc_times[::-1],
            y=fc_upper + fc_lower[::-1],
            fill="toself",
            fillcolor="rgba(255, 99, 71, 0.22)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="BigQuery AI.FORECAST 90% Confidence Interval",
        )
    )
    # Observed historical series
    fig.add_trace(
        go.Scatter(
            x=hist_times,
            y=hist_precip,
            mode="lines+markers",
            name="Observed GPM IMERG V07 Rainfall (mm/hr)",
            line=dict(color="#0064ff", width=2.5),
        )
    )
    # AI.FORECAST TimesFM prediction
    fig.add_trace(
        go.Scatter(
            x=fc_times,
            y=fc_vals,
            mode="lines+markers",
            name="BigQuery AI.FORECAST (TimesFM) Nowcast (mm/hr)",
            line=dict(color="#eb1e00", width=3, dash="dash"),
        )
    )
    fig.update_layout(
        title=(
            f"<b>Precipitation Nowcast ({storm_name})</b> — "
            "Observed GPM IMERG V07 vs. BigQuery ML AI.FORECAST (TimesFM)"
        ),
        xaxis_title="Timestamp (UTC)",
        yaxis_title="Precipitation Rate (mm/hr)",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_weathernext_ensemble_figure(
    ensemble_data: dict[str, Any],
) -> go.Figure:
    """Creates a Plotly ensemble plume chart for WeatherNext 3 percentiles."""
    rows = ensemble_data["ensemble_rows"]
    times = [r["valid_time_utc"] for r in rows]
    p10 = [float(r["p10_mm_hr"]) for r in rows]
    p25 = [float(r["p25_mm_hr"]) for r in rows]
    p50 = [float(r["p50_mm_hr"]) for r in rows]
    p75 = [float(r["p75_mm_hr"]) for r in rows]
    p90 = [float(r["p90_mm_hr"]) for r in rows]
    mean_vals = [float(r["mean_mm_hr"]) for r in rows]

    fig = go.Figure()

    # Outer 10th-90th percentile band (80% of 64 ensemble members)
    fig.add_trace(
        go.Scatter(
            x=times + times[::-1],
            y=p90 + p10[::-1],
            fill="toself",
            fillcolor="rgba(30, 136, 229, 0.16)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="p10–p90 Spread (80% of 64 Members)",
        )
    )
    # Inner 25th-75th interquartile band (middle 50% of 64 ensemble members)
    fig.add_trace(
        go.Scatter(
            x=times + times[::-1],
            y=p75 + p25[::-1],
            fill="toself",
            fillcolor="rgba(30, 136, 229, 0.34)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="p25–p75 Interquartile Range (50% of Members)",
        )
    )
    # Ensemble Median (p50)
    fig.add_trace(
        go.Scatter(
            x=times,
            y=p50,
            mode="lines+markers",
            name="Ensemble Median (p50)",
            line=dict(color="#0d47a1", width=3),
        )
    )
    # Ensemble Mean
    fig.add_trace(
        go.Scatter(
            x=times,
            y=mean_vals,
            mode="lines+markers",
            name="Ensemble Mean (mean)",
            line=dict(color="#d81b60", width=2.5, dash="dash"),
        )
    )
    # 90th percentile tail-risk line
    fig.add_trace(
        go.Scatter(
            x=times,
            y=p90,
            mode="lines",
            name="p90 Worst-Case Tail Risk (90th Percentile)",
            line=dict(color="#ff6f00", width=1.8, dash="dot"),
        )
    )
    fig.update_layout(
        title=(
            f"<b>WeatherNext 3 (64-Member Ensemble)</b> — "
            f"{ensemble_data.get('region_name', 'Probabilistic Rainfall Forecast')}"
        ),
        xaxis_title="Valid Forecast Time (UTC)",
        yaxis_title="1-Hour Precipitation Rate (mm/hr)",
        height=430,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_bay_area_microclimate_figure(
    microclimate_rows: list[dict[str, Any]],
) -> go.Figure:
    """Creates a Plotly chart comparing 5 Bay Area & Monterey Bay microclimates."""
    labels = [
        f"{r['city']}<br><sup>{r['microclimate_zone']}</sup>"
        for r in microclimate_rows
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
    fig.update_layout(
        title=(
            "<b>San Francisco & Monterey Bay Microclimate Comparison</b> — "
            "Coastal Marine Gaps vs. Rain-Shadowed Valleys"
        ),
        barmode="group",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(
        title_text="Relative Humidity (%)", range=[0, 100], secondary_y=True
    )
    return fig
