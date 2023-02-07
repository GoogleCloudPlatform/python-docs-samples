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

"""Utility functions to visualize data.

Color names from https://chir.ag/projects/name-that-color
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as graph_objects
from plotly.subplots import make_subplots


def render_rgb_images(
    values: np.ndarray, min: float = 0.0, max: float = 1.0
) -> np.ndarray:
    """Renders a numeric NumPy array with shape (width, height, rgb) as an image.

    Args:
        values: A float array with shape (width, height, rgb).
        min: Minimum value in the values.
        max: Maximum value in the values.

    Returns: An uint8 array with shape (width, height, rgb).
    """
    scaled_values = (values - min) / (max - min)
    rgb_values = scaled_values.clip(0, 1) * 255
    return rgb_values.astype(np.uint8)


def render_palette(
    values: np.ndarray, palette: list[str], min: float = 0.0, max: float = 1.0
) -> np.ndarray:
    """Renders a NumPy array with shape (width, height, 1) as an image with a palette.

    Args:
        values: An uint8 array with shape (width, height, 1).
        palette: List of hex encoded colors.

    Returns: An uint8 array with shape (width, height, rgb) with colors from the palette.
    """
    # Create a color map from a hex color palette.
    xs = np.linspace(0, len(palette), 256)
    indices = np.arange(len(palette))

    red = np.interp(xs, indices, [int(c[0:2], 16) for c in palette])
    green = np.interp(xs, indices, [int(c[2:4], 16) for c in palette])
    blue = np.interp(xs, indices, [int(c[4:6], 16) for c in palette])
    color_map = np.array([red, green, blue]).astype(np.uint8).transpose()

    scaled_values = (values - min) / (max - min)
    color_indices = (scaled_values.clip(0, 1) * 255).astype(np.uint8)
    return np.take(color_map, color_indices, axis=0)


def render_goes16(patch: np.ndarray) -> np.ndarray:
    red = patch[:, :, 1]  # CMI_C02
    green = patch[:, :, 2]  # CMI_C03
    blue = patch[:, :, 0]  # CMI_C01
    rgb_patch = np.stack([red, green, blue], axis=-1)
    return render_rgb_images(rgb_patch, max=3000)


def render_gpm(patch: np.ndarray) -> np.ndarray:
    palette = [
        "000096",  # Navy blue
        "0064ff",  # Blue ribbon blue
        "00b4ff",  # Dodger blue
        "33db80",  # Shamrock green
        "9beb4a",  # Conifer green
        "ffeb00",  # Turbo yellow
        "ffb300",  # Selective yellow
        "ff6400",  # Blaze orange
        "eb1e00",  # Scarlet red
        "af0000",  # Bright red
    ]
    return render_palette(patch[:, :, 0], palette, max=20)


def render_elevation(patch: np.ndarray) -> np.ndarray:
    palette = [
        "000000",  # Black
        "478fcd",  # Shakespeare blue
        "86c58e",  # De York green
        "afc35e",  # Celery green
        "8f7131",  # Pesto brown
        "b78d4f",  # Muddy waters brown
        "e2b8a6",  # Rose fog pink
        "ffffff",  # White
    ]
    return render_palette(patch[:, :, 0], palette, max=3000)


def show_inputs(patch: np.ndarray) -> None:
    fig = make_subplots(rows=2, cols=4)
    fig.add_trace(graph_objects.Image(z=render_gpm(patch[:, :, 0:1])), row=1, col=1)
    fig.add_trace(graph_objects.Image(z=render_gpm(patch[:, :, 1:2])), row=1, col=2)
    fig.add_trace(graph_objects.Image(z=render_gpm(patch[:, :, 2:3])), row=1, col=3)
    fig.add_trace(graph_objects.Image(z=render_goes16(patch[:, :, 3:19])), row=2, col=1)
    fig.add_trace(
        graph_objects.Image(z=render_goes16(patch[:, :, 19:35])), row=2, col=2
    )
    fig.add_trace(
        graph_objects.Image(z=render_goes16(patch[:, :, 35:51])), row=2, col=3
    )
    fig.add_trace(
        graph_objects.Image(z=render_elevation(patch[:, :, 51:52])), row=1, col=4
    )
    fig.update_layout(height=500, margin=dict(l=0, r=0, b=0, t=0))
    fig.show()


def show_outputs(patch: np.ndarray) -> None:
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(graph_objects.Image(z=render_gpm(patch[:, :, 0:1])), row=1, col=1)
    fig.add_trace(graph_objects.Image(z=render_gpm(patch[:, :, 1:2])), row=1, col=2)
    fig.update_layout(height=300, margin=dict(l=0, r=0, b=0, t=0))
    fig.show()


def show_predictions(results: list[tuple]) -> None:
    fig = make_subplots(rows=5, cols=len(results), vertical_spacing=0.025)
    for i, (inputs, predictions, labels) in enumerate(results, start=1):
        fig.add_trace(
            graph_objects.Image(z=render_goes16(inputs[:, :, 35:51])), row=1, col=i
        )
        fig.add_trace(
            graph_objects.Image(z=render_gpm(inputs[:, :, 2:3])), row=2, col=i
        )
        fig.add_trace(
            graph_objects.Image(z=render_elevation(inputs[:, :, 51:52])), row=3, col=i
        )
        fig.add_trace(
            graph_objects.Image(z=render_gpm(predictions[:, :, 0:1])), row=4, col=i
        )
        fig.add_trace(
            graph_objects.Image(z=render_gpm(labels[:, :, 0:1])), row=5, col=i
        )
    fig.update_layout(
        height=5 * int(1000 / len(results)),
        margin=dict(l=0, r=0, b=0, t=0),
    )
    fig.show()
