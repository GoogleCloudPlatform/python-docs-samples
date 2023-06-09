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

"""Defines a Fully Convolutional Network to predict precipitation."""

from __future__ import annotations

from typing import Any as AnyType

from datasets.arrow_dataset import Dataset
import numpy as np
import torch
from transformers import PretrainedConfig, PreTrainedModel


class WeatherConfig(PretrainedConfig):
    """A custom Hugging Face config for a WeatherModel.

    This contains all the hyperparameters for the model, including the
    mean and standard deviation used for the Normalization layer in the model.

    For more information:
        https://huggingface.co/docs/transformers/main/en/custom_models#writing-a-custom-configuration
    """

    model_type = "weather"

    def __init__(
        self,
        mean: list = [],
        std: list = [],
        num_inputs: int = 52,
        num_hidden1: int = 64,
        num_hidden2: int = 128,
        num_outputs: int = 2,
        kernel_size: tuple[int, int] = (3, 3),
        **kwargs: AnyType,
    ) -> None:
        self.mean = mean
        self.std = std
        self.num_inputs = num_inputs
        self.num_hidden1 = num_hidden1
        self.num_hidden2 = num_hidden2
        self.num_outputs = num_outputs
        self.kernel_size = kernel_size
        super().__init__(**kwargs)


class WeatherModel(PreTrainedModel):
    """A custom Hugging Face model.

    For more information:
        https://huggingface.co/docs/transformers/main/en/custom_models#writing-a-custom-model
    """

    config_class = WeatherConfig

    def __init__(self, config: WeatherConfig) -> None:
        super().__init__(config)
        self.layers = torch.nn.Sequential(
            Normalization(config.mean, config.std),
            MoveDim(-1, 1),  # convert to channels-first
            torch.nn.Conv2d(config.num_inputs, config.num_hidden1, config.kernel_size),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(
                config.num_hidden1, config.num_hidden2, config.kernel_size
            ),
            torch.nn.ReLU(),
            MoveDim(1, -1),  # convert to channels-last
            torch.nn.Linear(config.num_hidden2, config.num_outputs),
            torch.nn.ReLU(),  # precipitation cannot be negative
        )

    def forward(
        self, inputs: torch.Tensor, labels: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        """Computes predictions as expected by ModelOutputs.

        If `labels` are passed, it computes the loss between the model's
        predictions and the actual labels.

        For more information:
            https://huggingface.co/docs/transformers/main/en/main_classes/output

        Args:
            inputs: Input data.
            labels: Ground truth data.

        Returns:
            {"loss": loss, "logits": predictions} if `labels` is provided.
            {"logits": predictions} otherwise.
        """
        predictions = self.layers(inputs)
        if labels is None:
            return {"logits": predictions}

        loss_fn = torch.nn.SmoothL1Loss()
        loss = loss_fn(predictions, labels)
        return {"loss": loss, "logits": predictions}

    @staticmethod
    def create(inputs: Dataset, **kwargs: AnyType) -> WeatherModel:
        """Creates a new WeatherModel calculating the
        mean and standard deviation from a dataset."""
        data = np.array(inputs, np.float32)
        mean = data.mean(axis=(0, 1, 2))[None, None, None, :]
        std = data.std(axis=(0, 1, 2))[None, None, None, :]
        config = WeatherConfig(mean.tolist(), std.tolist(), **kwargs)
        return WeatherModel(config)

    def predict(self, inputs: AnyType) -> np.ndarray:
        """Predicts a single request."""
        return self.predict_batch(torch.as_tensor([inputs]))[0]

    def predict_batch(self, inputs_batch: AnyType) -> np.ndarray:
        """Predicts a batch of requests."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = self.to(device)
        with torch.no_grad():
            outputs = model(torch.as_tensor(inputs_batch, device=device))
            predictions = outputs["logits"]
            return predictions.cpu().numpy()


class Normalization(torch.nn.Module):
    """Preprocessing normalization layer with z-score."""

    def __init__(self, mean: AnyType, std: AnyType) -> None:
        super().__init__()
        self.mean = torch.nn.Parameter(torch.as_tensor(mean))
        self.std = torch.nn.Parameter(torch.as_tensor(std))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return (x - self.mean) / self.std


class MoveDim(torch.nn.Module):
    """Moves a dimension axis to another position."""

    def __init__(self, src: int, dest: int) -> None:
        super().__init__()
        self.src = src
        self.dest = dest

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.moveaxis(self.src, self.dest)
