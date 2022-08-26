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

"""Trains a model to predict precipitation."""

from __future__ import annotations

from glob import glob
import os

from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict
import numpy as np
from transformers import Trainer, TrainingArguments

from weather.model import WeatherModel


# Default values.
EPOCHS = 100
BATCH_SIZE = 512
TRAIN_TEST_RATIO = 0.9

# Constants.
NUM_DATASET_READ_PROC = 16  # number of processes to read data files in parallel
NUM_DATASET_PROC = os.cpu_count() or 8  # number of processes for CPU transformations


def read_dataset(data_path: str, train_test_ratio: float) -> DatasetDict:
    """Reads data files into a Dataset with train/test splits."""

    def read_data_file(item: dict[str, str]) -> dict[str, np.ndarray]:
        with open(item["filename"], "rb") as f:
            npz = np.load(f)
            return {"inputs": npz["inputs"], "labels": npz["labels"]}

    def flatten(batch: dict) -> dict:
        return {key: np.concatenate(values) for key, values in batch.items()}

    files = glob(os.path.join(data_path, "*.npz"))
    dataset = (
        Dataset.from_dict({"filename": files})
        .map(
            read_data_file,
            num_proc=NUM_DATASET_READ_PROC,
            remove_columns=["filename"],
        )
        .map(flatten, batched=True, num_proc=NUM_DATASET_PROC)
    )
    return dataset.train_test_split(train_size=train_test_ratio, shuffle=True)


def augmented(dataset: Dataset) -> Dataset:
    """Augment dataset by rotating and flipping the examples."""

    def augment(values: list) -> np.ndarray:
        transformed = [
            np.rot90(values, 0, (1, 2)),
            np.rot90(values, 1, (1, 2)),
            np.rot90(values, 2, (1, 2)),
            np.rot90(values, 3, (1, 2)),
            np.flip(np.rot90(values, 0, (1, 2)), axis=1),
            np.flip(np.rot90(values, 1, (1, 2)), axis=1),
            np.flip(np.rot90(values, 2, (1, 2)), axis=1),
            np.flip(np.rot90(values, 3, (1, 2)), axis=1),
        ]
        return np.concatenate(transformed)

    return dataset.map(
        lambda batch: {key: augment(values) for key, values in batch.items()},
        batched=True,
        num_proc=NUM_DATASET_PROC,
    )


def run(
    data_path: str,
    model_path: str,
    epochs: int = EPOCHS,
    batch_size: int = BATCH_SIZE,
    train_test_ratio: float = TRAIN_TEST_RATIO,
    from_checkpoint: bool = False,
) -> None:
    """Trains a new WeatherModel.

    Args:
        data_path: Directory path to read data files from.
        model_path Directory path to write the trained model to.
        epochs: Number of times to go through the training dataset.
        batch_size: Number of training examples to learn from at once.
        train_test_ratio: Ratio of examples to use for training and for testing.
        from_checkpoint: Whether or not to resume from latest checkpoint.
    """

    print(f"data_path: {data_path}")
    print(f"model_path: {model_path}")
    print(f"epochs: {epochs}")
    print(f"batch_size: {batch_size}")
    print(f"train_test_ratio: {train_test_ratio}")
    print("-" * 40)

    dataset = read_dataset(data_path, train_test_ratio)
    print(dataset)

    model = WeatherModel.create(dataset["train"]["inputs"])
    print(model.config)
    print(model)

    training_args = TrainingArguments(
        output_dir=os.path.join(model_path, "checkpoints"),
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        logging_strategy="epoch",
        evaluation_strategy="epoch",
    )
    trainer = Trainer(
        model,
        training_args,
        train_dataset=augmented(dataset["train"]),
        eval_dataset=dataset["test"],
    )
    trainer.train(resume_from_checkpoint=from_checkpoint)
    trainer.save_model(model_path)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        required=True,
        help="Directory path to read data files from.",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Directory path to write the trained model to.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=EPOCHS,
        help="Number of times to go through the training dataset.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
        help="Number of training examples to learn from at once.",
    )
    parser.add_argument(
        "--train-test-ratio",
        type=float,
        default=TRAIN_TEST_RATIO,
        help="Ratio of examples to use for training and for testing.",
    )
    parser.add_argument(
        "--from-checkpoint",
        action="store_true",
        help="Whether or not to resume from latest checkpoint.",
    )
    args = parser.parse_args()

    run(**vars(args))


if __name__ == "__main__":
    main()
