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

import io
from typing import Callable, Iterable, List, Optional, Tuple

import apache_beam as beam
import ee
import google.auth
import numpy as np
import requests
from urllib3 import HTTPAdapter, Retry


class GetPatch(beam.DoFn):
    def __init__(
        self,
        get_image: Callable[[], ee.Image],
        bands: List[str],
        patch_size: int,
        scale: int,
        project: str = "",
        max_retries: int = 20,
        retry_exp_backoff: float = 0.5,
    ) -> None:
        self.get_image = get_image
        self.bands = bands
        self.patch_size = patch_size
        self.scale = scale
        self.project = project
        self.max_retries = max_retries
        self.retry_exp_backoff = retry_exp_backoff

    def setup(self) -> None:
        credentials, default_project = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/earthengine",
            ]
        )
        ee.Initialize(
            credentials,
            project=self.project or default_project,
            opt_url="https://earthengine-highvolume.googleapis.com",
        )
        self.image = self.get_image()

        # Create a retry strategy for the HTTP requests.
        self.http = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            status_forcelist=[429],
            backoff_factor=self.retry_exp_backoff,
        )
        self.http.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    def process(self, lat_lon: Tuple[float, float]) -> Iterable[np.ndarray]:
        # Prepare to download the patch of pixels as a numpy array.
        lat, lon = lat_lon
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(self.scale * self.patch_size / 2, 1).bounds(1)
        url = self.image.getDownloadURL(
            {
                "region": region,
                "dimensions": [self.patch_size, self.patch_size],
                "format": "NPY",
                "bands": self.bands or self.image.bandNames().getInfo(),
            }
        )

        # Fetch the data from Earth Engine and return it as a numpy array.
        np_bytes = self.http.get(url).content
        return np.load(io.BytesIO(np_bytes), allow_pickle=True)
