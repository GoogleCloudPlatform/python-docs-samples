import json
import pytest

from predictor import Predictor
import task
from util import CitibikeDataset


def test_dataset():
    dataset = CitibikeDataset()
    x, y = dataset[0]

    assert len(x) == 11
    assert len(y) == 1807


def test_predictor():
    # Get model predictor
    model = Predictor.from_path('testing_data')

    # Get input instances
    with open('testing_data/inputs.json') as f:
        inputs = json.load(f)

    # Run prediction routine
    outputs = model.predict(inputs)

    # Verify output shape
    assert len(outputs[0]) == 1807
    