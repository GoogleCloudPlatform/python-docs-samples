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

from __future__ import annotations

import numpy as np
from plotly.graph_objects import Image
from plotly.subplots import make_subplots

CLASSIFICATIONS = {
    "💧 Water": "419BDF",
    "🌳 Trees": "397D49",
    "🌾 Grass": "88B053",
    "🌿 Flooded vegetation": "7A87C6",
    "🚜 Crops": "E49635",
    "🪴 Shrub and scrub": "DFC35A",
    "🏗️ Built-up areas": "C4281B",
    "🪨 Bare ground": "A59B8F",
    "❄️ Snow and ice": "B39FE1",
}


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
    rgb_values = np.clip(scaled_values, 0, 1) * 255
    return rgb_values.astype(np.uint8)


def render_classifications(values: np.ndarray, palette: list[str]) -> np.ndarray:
    """Renders a classifications NumPy array with shape (width, height, 1) as an image.

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
    color_indices = (values / len(palette) * 255).astype(np.uint8)
    return np.take(color_map, color_indices, axis=0)


def render_sentinel2(patch: np.ndarray, max: float = 3000) -> np.ndarray:
    """Renders a Sentinel 2 image."""
    red = patch[:, :, 3]  # B4
    green = patch[:, :, 2]  # B3
    blue = patch[:, :, 1]  # B2
    rgb_patch = np.stack([red, green, blue], axis=-1)
    return render_rgb_images(rgb_patch, 0, max)


def render_landcover(patch: np.ndarray) -> np.ndarray:
    """Renders a land cover image."""
    palette = list(CLASSIFICATIONS.values())
    return render_classifications(patch[:, :, 0], palette)


def show_inputs(inputs: np.ndarray, max: float = 3000) -> None:
    """Shows the input data as an image."""
    fig = make_subplots(rows=1, cols=1, subplot_titles=("Sentinel 2"))
    fig.add_trace(Image(z=render_sentinel2(inputs, max)), row=1, col=1)
    fig.show()


def show_outputs(outputs: np.ndarray) -> None:
    """Shows the outputs/labels data as an image."""
    fig = make_subplots(rows=1, cols=1, subplot_titles=("Land cover",))
    fig.add_trace(Image(z=render_landcover(outputs)), row=1, col=1)
    fig.show()


def show_example(inputs: np.ndarray, labels: np.ndarray, max: float = 3000) -> None:
    """Shows an example of inputs and labels an image."""
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Sentinel 2", "Land cover"))
    fig.add_trace(Image(z=render_sentinel2(inputs, max)), row=1, col=1)
    fig.add_trace(Image(z=render_landcover(labels)), row=1, col=2)
    fig.show()


def show_legend() -> None:
    """Shows the legend of the land cover classifications."""

    def color_box(red: int, green: int, blue: int) -> str:
        return f"\033[48;2;{red};{green};{blue}m"

    reset_color = "\u001b[0m"
    for name, color in CLASSIFICATIONS.items():
        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)
        print(f"{color_box(red, green, blue)}   {reset_color} {name}")
