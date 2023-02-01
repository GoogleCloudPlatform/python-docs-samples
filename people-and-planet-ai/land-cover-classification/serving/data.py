# Copyright 2022 Google LLC
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

import io

import ee
from google.api_core import exceptions, retry
import google.auth
import numpy as np
from numpy.lib.recfunctions import structured_to_unstructured
import requests


SCALE = 10  # meters per pixel


def ee_init() -> None:
    """Authenticate and initialize Earth Engine with the default credentials."""
    # Use the Earth Engine High Volume endpoint.
    #   https://developers.google.com/earth-engine/cloud/highvolume
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )
    ee.Initialize(
        credentials.with_quota_project(None),
        project=project,
        opt_url="https://earthengine-highvolume.googleapis.com",
    )


def get_input_image(year: int) -> ee.Image:
    """Get a Sentinel-2 Earth Engine image.

    This filters clouds and returns the median for the selected time range.
    Then it removes the mask and fills all the missing values, otherwise
    the data normalization will give infinities and not-a-number.
    Missing values on Sentinel 2 are filled with 1000, which is near the mean.

    For more information, see:
        https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_HARMONIZED

    Args:
        year: Year to calculate the median composite.

    Returns: An Earth Engine image with the median Sentinel-2 values.
    """

    def mask_sentinel2_clouds(image: ee.Image) -> ee.Image:
        CLOUD_BIT = 10
        CIRRUS_CLOUD_BIT = 11
        bit_mask = (1 << CLOUD_BIT) | (1 << CIRRUS_CLOUD_BIT)
        mask = image.select("QA60").bitwiseAnd(bit_mask).eq(0)
        return image.updateMask(mask)

    return (
        ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
        .filterDate(f"{year}-1-1", f"{year}-12-31")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(mask_sentinel2_clouds)
        .select("B.*")
        .median()
        .unmask(1000)
        .float()
    )


def get_label_image() -> ee.Image:
    """Get the European Space Agency WorldCover image.

    This remaps the ESA classifications with the Dynamic World classifications.
    Any missing value is filled with 0 (water).

    For more information, see:
        https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100
        https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1

    Returns: An Earth Engine image with land cover classification as indices.
    """
    # Remap the ESA classifications into the Dynamic World classifications
    fromValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
    toValues = [1, 5, 2, 4, 6, 7, 8, 0, 3, 3, 7]
    return (
        ee.Image("ESA/WorldCover/v100/2020")
        .select("Map")
        .remap(fromValues, toValues)
        .rename("landcover")
        .unmask(0)
        .byte()  # as unsinged 8-bit integer
    )


def get_input_patch(
    year: int, lonlat: tuple[float, float], patch_size: int
) -> np.ndarray:
    """Gets the inputs patch of pixels for the given point and year.

    args:
        year: Year of interest, a median composite is used.
        lonlat: A (longitude, latitude) pair for the point of interest.
        patch_size: Size in pixels of the surrounding square patch.

    Returns: The pixel values of an inputs patch as a NumPy array.
    """
    image = get_input_image(year)
    patch = get_patch(image, lonlat, patch_size, SCALE)
    return structured_to_unstructured(patch)


def get_label_patch(lonlat: tuple[float, float], patch_size: int) -> np.ndarray:
    """Gets the labels patch of pixels for the given point.

    Labels land cover data is only available for 2020, so any training example
    must use inputs from the year 2020 as well.

    args:
        lonlat: A (longitude, latitude) pair for the point of interest.
        patch_size: Size in pixels of the surrounding square patch.

    Returns: The pixel values of a labels patch as a NumPy array.
    """
    image = get_label_image()
    patch = get_patch(image, lonlat, patch_size, SCALE)
    return structured_to_unstructured(patch)


@retry.Retry(deadline=10 * 60)  # seconds
def get_patch(
    image: ee.Image, lonlat: tuple[float, float], patch_size: int, scale: int
) -> np.ndarray:
    """Fetches a patch of pixels from Earth Engine.

    It retries if we get error "429: Too Many Requests".

    Args:
        image: Image to get the patch from.
        lonlat: A (longitude, latitude) pair for the point of interest.
        patch_size: Size in pixels of the surrounding square patch.
        scale: Number of meters per pixel.

    Raises:
        requests.exceptions.RequestException

    Returns: The requested patch of pixels as a NumPy array with shape (width, height, bands).
    """
    point = ee.Geometry.Point(lonlat)
    url = image.getDownloadURL(
        {
            "region": point.buffer(scale * patch_size / 2, 1).bounds(1),
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
