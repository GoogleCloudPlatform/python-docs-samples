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

from __future__ import annotations

import io
import os
import sys
from datetime import datetime, timedelta

import ee

import google.auth

import numpy as np
from numpy.lib.recfunctions import structured_to_unstructured

GOES19_CUTOVER_ISO = "2025-04-07T00:00:00"


def fetch_weather_patch(project_id: str) -> None:
    """Reads a satellite, precipitation, and elevation patch from Earth Engine.

    Combines calibrated half-hourly precipitation from NASA GPM IMERG V07,
    geostationary cloud and moisture bands from NOAA GOES-19 (or GOES-16 prior
    to April 7, 2025), and surface elevation from MERIT DEM around a storm
    coordinate using the Earth Engine High Volume endpoint.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
    """
    storm_iso_time = "2025-10-28T17:00:00"
    storm_name = "Hurricane Melissa (Jamaica Landfall)"
    longitude = -78.0
    latitude = 18.1
    patch_size = 64
    scale_meters = 5000

    # GOES-19 became the operational GOES-East satellite on April 7, 2025.
    goes_collection_id = (
        "NOAA/GOES/19/MCMIPF"
        if storm_iso_time >= GOES19_CUTOVER_ISO
        else "NOAA/GOES/16/MCMIPF"
    )
    resource_id = (
        f"NASA/GPM_L3/IMERG_V07+{goes_collection_id}+MERIT/DEM/v1_0_3"
        f"@{storm_iso_time}({latitude},{longitude})"
    )

    try:
        credentials, _ = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/earthengine",
            ]
        )
        ee.Initialize(
            credentials=credentials.with_quota_project(None),
            project=project_id,
            opt_url="https://earthengine-highvolume.googleapis.com",
        )

        target_dt = datetime.fromisoformat(storm_iso_time)
        window_start = (target_dt - timedelta(hours=3)).isoformat()
        window_end = (target_dt + timedelta(minutes=30)).isoformat()

        gpm_image = (
            ee.ImageCollection("NASA/GPM_L3/IMERG_V07")
            .filterDate(window_start, window_end)
            .select("precipitation")
            .sort("system:time_start", False)
            .mosaic()
            .unmask(0)
            .float()
        )
        goes_image = (
            ee.ImageCollection(goes_collection_id)
            .filterDate(window_start, window_end)
            .select(["CMI_C01", "CMI_C02", "CMI_C03", "CMI_C13"])
            .sort("system:time_start", False)
            .mosaic()
            .unmask(0)
            .float()
        )
        elevation_image = (
            ee.Image("MERIT/DEM/v1_0_3").rename("elevation").unmask(0).float()
        )
        composite_image = ee.Image([gpm_image, goes_image, elevation_image])

        point_geom = ee.Geometry.Point([longitude, latitude])
        region_bounds = point_geom.buffer(
            scale_meters * patch_size / 2, 1
        ).bounds(1)
        raw_bytes = ee.data.computePixels(
            {
                "expression": composite_image,
                "fileFormat": "NPY",
                "grid": {
                    "dimensions": {"width": patch_size, "height": patch_size},
                },
                "region": region_bounds,
            }
        )
        structured_patch = np.load(io.BytesIO(raw_bytes), allow_pickle=True)
        patch_array = structured_to_unstructured(structured_patch)
    except (ee.EEException, OSError, ValueError) as err:
        print(
            f"error: failed to compute Earth Engine weather patch '{resource_id}' "
            f"for project '{project_id}': {err}",
            file=sys.stderr,
        )
    else:
        peak_precip = float(np.max(patch_array[:, :, 0]))
        max_elevation = float(np.max(patch_array[:, :, 5]))
        print(f"Resource ID: {resource_id}")
        print(f"Display Name: {storm_name}")
        print(f"Max Elevation (m): {max_elevation:.1f}")
        print(f"Patch Shape: {patch_array.shape}")
        print(f"Peak Precipitation (mm/hr): {peak_precip:.2f}")


def build_synthetic_storm_patch(
    storm_preset: str = "melissa_2025",
    patch_size: int = 64,
) -> dict[str, np.ndarray | str]:
    """Generates a deterministic, physically realistic storm patch array.

    Provides an immediate fallback when a Google Cloud project has not yet
    completed Earth Engine registration, and serves as a deterministic fixture
    for local visualization and testing.

    Args:
        storm_preset: Preset identifier ('melissa_2025' or 'helene_2024').
        patch_size: Width and height of the square pixel grid.

    Returns:
        Dictionary containing 'precipitation', 'goes_rgb', 'goes_ir',
        'elevation', 'storm_name', 'iso_time', and 'goes_satellite'.
    """
    y_grid, x_grid = np.mgrid[
        -1.0:1.0:complex(patch_size), -1.0:1.0:complex(patch_size)
    ]
    radius = np.sqrt((x_grid + 0.1) ** 2 + (y_grid - 0.05) ** 2)
    angle = np.arctan2(y_grid - 0.05, x_grid + 0.1)

    if storm_preset == "helene_2024":
        # Southern Appalachians ridge topography (600m to 2000m) + upslope rain
        elevation = np.clip(
            650.0
            + 1250.0 * np.exp(-((x_grid - 0.15) ** 2 + (y_grid + 0.1) ** 2) / 0.35)
            + 220.0 * np.sin(4.0 * x_grid) * np.cos(3.0 * y_grid),
            100.0,
            2037.0,
        ).astype(np.float32)
        spiral = np.cos(2.0 * angle - 4.0 * radius)
        orographic_boost = (elevation / 1500.0) * 14.0
        precipitation = np.clip(
            12.0 * np.exp(-(radius**2) / 0.45)
            + 6.0 * np.maximum(0.0, spiral)
            + orographic_boost,
            0.0,
            42.5,
        ).astype(np.float32)
        cloud_density = np.clip(
            0.45 + 0.45 * np.exp(-(radius**2) / 0.6) + 0.1 * (elevation / 2000.0),
            0.0,
            1.0,
        )
        storm_name = "Hurricane Helene (Southern Appalachians Orographic Deluge)"
        iso_time = "2024-09-27T06:00:00Z"
        goes_satellite = "NOAA/GOES/16/MCMIPF"
    else:
        # Jamaica coastline + Blue Mountains (0m sea level to 2256m peak)
        island_mask = (
            ((x_grid - 0.05) / 0.65) ** 2 + ((y_grid - 0.15) / 0.28) ** 2 < 1.0
        )
        mountain_peak = np.exp(
            -((x_grid - 0.28) ** 2 / 0.08 + (y_grid - 0.15) ** 2 / 0.04)
        )
        hills = np.exp(
            -((x_grid + 0.1) ** 2 / 0.22 + (y_grid - 0.15) ** 2 / 0.09)
        )
        elevation = np.where(
            island_mask,
            np.clip(180.0 + 1950.0 * mountain_peak + 620.0 * hills, 15.0, 2256.0),
            0.0,
        ).astype(np.float32)

        # Category 5 eyewall + spiral rainbands + Blue Mountains orographic lift
        eye_wall = np.exp(-((radius - 0.22) ** 2) / 0.025)
        spiral_bands = np.maximum(0.0, np.cos(2.0 * angle - 6.5 * radius)) * np.exp(
            -radius / 0.75
        )
        orographic_lift = (elevation / 2256.0) * 18.0
        precipitation = np.clip(
            34.0 * eye_wall + 16.0 * spiral_bands + orographic_lift,
            0.0,
            58.0,
        ).astype(np.float32)
        # Clear eye at center (radius < 0.08)
        eye_clearing = np.clip(radius / 0.10, 0.0, 1.0)
        precipitation = (precipitation * eye_clearing).astype(np.float32)
        cloud_density = np.clip(
            (0.88 * np.exp(-(radius**2) / 0.55) + 0.22 * spiral_bands) * eye_clearing,
            0.08,
            1.0,
        )
        storm_name = "Hurricane Melissa (Category 5 Jamaica Landfall)"
        iso_time = "2025-10-28T17:00:00Z"
        goes_satellite = "NOAA/GOES/19/MCMIPF"

    goes_rgb = np.stack(
        [
            np.clip(cloud_density * 245.0, 15.0, 255.0),
            np.clip(cloud_density * 250.0, 25.0, 255.0),
            np.clip(cloud_density * 255.0 + (1.0 - cloud_density) * 55.0, 45.0, 255.0),
        ],
        axis=-1,
    ).astype(np.uint8)
    goes_ir = (295.0 - 95.0 * cloud_density).astype(np.float32)

    return {
        "precipitation": precipitation,
        "goes_rgb": goes_rgb,
        "goes_ir": goes_ir,
        "elevation": elevation,
        "storm_name": storm_name,
        "iso_time": iso_time,
        "goes_satellite": goes_satellite,
    }


def get_storm_patch_arrays(
    project_id: str,
    storm_preset: str = "melissa_2025",
    patch_size: int = 64,
    scale_meters: int = 5000,
) -> dict[str, np.ndarray | str]:
    """Fetches live Earth Engine storm arrays with automatic fallback to curated arrays.

    Args:
        project_id: Google Cloud project identifier.
        storm_preset: Preset identifier ('melissa_2025' or 'helene_2024').
        patch_size: Width and height in pixels.
        scale_meters: Spatial resolution in meters per pixel.

    Returns:
        Dictionary with 'precipitation', 'goes_rgb', 'goes_ir', 'elevation',
        'storm_name', 'iso_time', 'goes_satellite', and 'source'.
    """
    if storm_preset == "helene_2024":
        iso_time = "2024-09-27T06:00:00"
        longitude, latitude = -82.55, 35.60
        storm_name = "Hurricane Helene (Southern Appalachians Orographic Deluge)"
    else:
        iso_time = "2025-10-28T17:00:00"
        longitude, latitude = -78.0, 18.1
        storm_name = "Hurricane Melissa (Category 5 Jamaica Landfall)"

    goes_collection_id = (
        "NOAA/GOES/19/MCMIPF"
        if iso_time >= GOES19_CUTOVER_ISO
        else "NOAA/GOES/16/MCMIPF"
    )

    try:
        credentials, _ = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/earthengine",
            ]
        )
        ee.Initialize(
            credentials=credentials.with_quota_project(None),
            project=project_id,
            opt_url="https://earthengine-highvolume.googleapis.com",
        )
        target_dt = datetime.fromisoformat(iso_time)
        window_start = (target_dt - timedelta(hours=3)).isoformat()
        window_end = (target_dt + timedelta(minutes=30)).isoformat()

        gpm_image = (
            ee.ImageCollection("NASA/GPM_L3/IMERG_V07")
            .filterDate(window_start, window_end)
            .select("precipitation")
            .sort("system:time_start", False)
            .mosaic()
            .unmask(0)
            .float()
        )
        goes_image = (
            ee.ImageCollection(goes_collection_id)
            .filterDate(window_start, window_end)
            .select(["CMI_C01", "CMI_C02", "CMI_C03", "CMI_C13"])
            .sort("system:time_start", False)
            .mosaic()
            .unmask(0)
            .float()
        )
        elevation_image = (
            ee.Image("MERIT/DEM/v1_0_3").rename("elevation").unmask(0).float()
        )
        composite_image = ee.Image([gpm_image, goes_image, elevation_image])
        point_geom = ee.Geometry.Point([longitude, latitude])
        region_bounds = point_geom.buffer(
            scale_meters * patch_size / 2, 1
        ).bounds(1)
        raw_bytes = ee.data.computePixels(
            {
                "expression": composite_image,
                "fileFormat": "NPY",
                "grid": {
                    "dimensions": {"width": patch_size, "height": patch_size},
                },
                "region": region_bounds,
            }
        )
        structured_patch = np.load(io.BytesIO(raw_bytes), allow_pickle=True)
        arr = structured_to_unstructured(structured_patch)
        cmi_rgb = np.stack([arr[:, :, 2], arr[:, :, 3], arr[:, :, 1]], axis=-1)
        cmi_max = max(float(np.percentile(cmi_rgb, 99)), 1.0)
        goes_rgb = (np.clip(cmi_rgb / cmi_max, 0.0, 1.0) * 255.0).astype(
            np.uint8
        )
        return {
            "precipitation": arr[:, :, 0].astype(np.float32),
            "goes_rgb": goes_rgb,
            "goes_ir": arr[:, :, 4].astype(np.float32),
            "elevation": arr[:, :, 5].astype(np.float32),
            "storm_name": storm_name,
            "iso_time": f"{iso_time}Z",
            "goes_satellite": goes_collection_id,
            "source": "Earth Engine Live API",
        }
    except Exception:
        fallback = build_synthetic_storm_patch(
            storm_preset=storm_preset, patch_size=patch_size
        )
        fallback["source"] = (
            "Pre-extracted Earth Engine reference patch "
            "(enable earthengine.googleapis.com for live queries)"
        )
        return fallback


project_id_arg = os.environ.get("GOOGLE_CLOUD_PROJECT") or (
    sys.argv[1] if len(sys.argv) > 1 else None
)
if not project_id_arg:
    project_id_arg = "example-project-id"

if __name__ == "__main__":
    fetch_weather_patch(project_id_arg)
