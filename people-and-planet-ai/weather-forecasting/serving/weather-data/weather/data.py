# Copyright 2023 Google LLC
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

"""Data utilities to grab data from Earth Engine.
Meant to be used for both training and prediction so the model is
trained on exactly the same data that will be used for predictions.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import io

import ee
from google.api_core import exceptions, retry
import google.auth
import numpy as np
from numpy.lib.recfunctions import structured_to_unstructured
import requests

# Constants.
SCALE = 10000  # meters per pixel
INPUT_HOUR_DELTAS = [-4, -2, 0]
OUTPUT_HOUR_DELTAS = [2, 6]
WINDOW = timedelta(days=1)

# Authenticate and initialize Earth Engine with the default credentials.
credentials, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/earthengine",
    ]
)

# Use the Earth Engine High Volume endpoint.
#   https://developers.google.com/earth-engine/cloud/highvolume
ee.Initialize(
    credentials.with_quota_project(None),
    project=project,
    opt_url="https://earthengine-highvolume.googleapis.com",
)


def get_gpm(date: datetime) -> ee.Image:
    """Gets a Global Precipitation Measurement image for the selected date.

    For more information:
        https://developers.google.com/earth-engine/datasets/catalog/NASA_GPM_L3_IMERG_V06

    Args:
        date: Date to take a snapshot from.

    Returns: An Earth Engine image.
    """
    window_start = (date - WINDOW).isoformat()
    window_end = date.isoformat()
    return (
        ee.ImageCollection("NASA/GPM_L3/IMERG_V06")
        .filterDate(window_start, window_end)
        .select("precipitationCal")
        .sort("system:time_start", False)
        .mosaic()
        .unmask(0)
        .float()
    )


def get_gpm_sequence(dates: list[datetime]) -> ee.Image:
    """Gets a Global Precipitation Measurement sequence for the selected dates.

    Args:
        dates: List of dates to get images from.

    Returns: An Earth Engine image.
    """
    images = [get_gpm(date) for date in dates]
    return ee.ImageCollection(images).toBands()


def get_goes16(date: datetime) -> ee.Image:
    """Gets a GOES 16 image for the selected date.

    For more information:
        https://developers.google.com/earth-engine/datasets/catalog/NOAA_GOES_16_MCMIPF

    Args:
        date: Date to take a snapshot from.

    Returns: An Earth Engine image.
    """
    window_start = (date - WINDOW).isoformat()
    window_end = date.isoformat()
    return (
        ee.ImageCollection("NOAA/GOES/16/MCMIPF")
        .filterDate(window_start, window_end)
        .select("CMI_C.*")
        .sort("system:time_start", False)
        .mosaic()
        .unmask(0)
        .float()
    )


def get_goes16_sequence(dates: list[datetime]) -> ee.Image:
    """Gets a GOES 16 sequence for the selected dates.

    Args:
        dates: List of dates to get images from.

    Returns: An Earth Engine image.
    """
    images = [get_goes16(date) for date in dates]
    return ee.ImageCollection(images).toBands()


def get_elevation() -> ee.Image:
    """Gets a digital elevation map.

    For more information:
        https://developers.google.com/earth-engine/datasets/catalog/MERIT_DEM_v1_0_3

    Returns: An Earth Engine image.
    """
    return ee.Image("MERIT/DEM/v1_0_3").rename("elevation").unmask(0).float()


def get_inputs_image(date: datetime) -> ee.Image:
    """Gets an Earth Engine image with all the inputs for the model.

    Args:
        date: Date to take a snapshot from.

    Returns: An Earth Engine image.
    """
    dates = [date + timedelta(hours=h) for h in INPUT_HOUR_DELTAS]
    precipitation = get_gpm_sequence(dates)
    cloud_and_moisture = get_goes16_sequence(dates)
    elevation = get_elevation()
    return ee.Image([precipitation, cloud_and_moisture, elevation])


def get_labels_image(date: datetime) -> ee.Image:
    """Gets an Earth Engine image with the labels to train the model.

    Args:
        date: Date to take a snapshot from.

    Returns: An Earth Engine image.
    """
    dates = [date + timedelta(hours=h) for h in OUTPUT_HOUR_DELTAS]
    return get_gpm_sequence(dates)


def get_inputs_patch(date: datetime, point: tuple, patch_size: int) -> np.ndarray:
    """Gets the patch of pixels for the inputs.

    Args:
        date: The date of interest.
        point: A (longitude, latitude) coordinate.
        patch_size: Size in pixels of the surrounding square patch.

    Returns: The pixel values of a patch as a NumPy array.
    """
    image = get_inputs_image(date)
    patch = get_patch(image, point, patch_size, SCALE)
    return structured_to_unstructured(patch)


def get_labels_patch(date: datetime, point: tuple, patch_size: int) -> np.ndarray:
    """Gets the patch of pixels for the labels.

    Args:
        date: The date of interest.
        point: A (longitude, latitude) coordinate.
        patch_size: Size in pixels of the surrounding square patch.

    Returns: The pixel values of a patch as a NumPy array.
    """
    image = get_labels_image(date)
    patch = get_patch(image, point, patch_size, SCALE)
    return structured_to_unstructured(patch)


@retry.Retry()
def get_patch(image: ee.Image, point: tuple, patch_size: int, scale: int) -> np.ndarray:
    """Fetches a patch of pixels from Earth Engine.

    It retries if we get error "429: Too Many Requests".

    Args:
        image: Image to get the patch from.
        point: A (longitude, latitude) pair for the point of interest.
        patch_size: Size in pixels of the surrounding square patch.
        scale: Number of meters per pixel.

    Raises:
        requests.exceptions.RequestException

    Returns:
        The requested patch of pixels as a structured
        NumPy array with shape (width, height).
    """
    geometry = ee.Geometry.Point(point)
    url = image.getDownloadURL(
        {
            "region": geometry.buffer(scale * patch_size / 2, 1).bounds(1),
            "dimensions": [patch_size, patch_size],
            "format": "NPY",
        }
    )

    # If we get "429: Too Many Requests" errors, it's safe to retry the request.
    # The Retry library only works with `google.api_core` exceptions.
    response = requests.get(url)
    if response.status_code == 429:
        raise exceptions.TooManyRequests(response.text)

    # Still raise any other exceptions to make sure we got valid data.
    response.raise_for_status()
    return np.load(io.BytesIO(response.content), allow_pickle=True)
