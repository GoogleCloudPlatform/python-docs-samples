from trainer.sklearn_model import task as sklearn_task
from trainer.tfkeras_model import task as tfkeras_task
from collections import namedtuple
import pytest
import shutil
import os
import uuid

SKLEARN_JOB_DIR = f'local-sklearn-{uuid.uuid4()}'
TFKERAS_JOB_DIR = f'local-keras-{uuid.uuid4()}'

def test_sklearn():
    SklearnArgs = namedtuple('SklearnArgs',
            ['job_dir', 'degree', 'alpha'])
    sklearn_args = SklearnArgs(job_dir=SKLEARN_JOB_DIR, degree=sklearn_task.DEFAULT_DEGREE, alpha=sklearn_task.DEFAULT_ALPHA)
    sklearn_task.fit_model(sklearn_args)

    assert os.path.isdir(SKLEARN_JOB_DIR), "Sklearn job directory not found"
    assert os.path.isfile(os.path.join(SKLEARN_JOB_DIR, 'model.joblib')), "Sklearn model file not found"
    shutil.rmtree(SKLEARN_JOB_DIR)

def test_tfkeras():
    TfkerasArgs = namedtuple('TfkerasArgs', 
            ['job_dir', 'num_epochs', 'batch_size', 'learning_rate', 'verbosity'])
    tfkeras_args = TfkerasArgs(job_dir=TFKERAS_JOB_DIR, num_epochs=tfkeras_task.DEFAULT_NUM_EPOCHS, batch_size=tfkeras_task.DEFAULT_BATCH_SIZE, learning_rate=tfkeras_task.DEFAULT_LEARNING_RATE, verbosity=tfkeras_task.DEFAULT_VERBOSITY)

    tfkeras_task.train_and_evaluate(tfkeras_args)

    assert os.path.isdir(TFKERAS_JOB_DIR)
    assert os.path.isfile(os.path.join(TFKERAS_JOB_DIR, 'keras_export', 'saved_model.pb')), "Keras model file not found"
    shutil.rmtree(TFKERAS_JOB_DIR)
