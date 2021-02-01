import os
import tarfile
import time
import uuid

from google.cloud import storage
from googleapiclient import discovery
import pytest

STAGING_BUCKET = f"tfkeras-job-dir-{uuid.uuid4()}"
INPUT_DIR = "inputs"
TRAINER_DIR = "modules"
MODELS_DIR = "models"
JOB_DIR = f"gs://{STAGING_BUCKET}/{MODELS_DIR}"
TRAIN_DATA = "train.csv"
TRAINER_TAR = "trainer.tar.gz"
TRAIN_DATA_PATH = f"gs://{STAGING_BUCKET}/{INPUT_DIR}/{TRAIN_DATA}"

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
MODEL_NAME = f"tfkeras-test-{uuid.uuid4()}"
JOB_ID = f"tfkeras_{str(uuid.uuid4())[:7]}"

TERMINAL_STATES = ["SUCCEEDED", "FAILED", "CANCELLING", "CANCELLED"]


@pytest.fixture(autouse=True)
def setup_teardown():
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(STAGING_BUCKET)
    bucket.blob(f"{INPUT_DIR}/{TRAIN_DATA}").upload_from_filename(TRAIN_DATA, timeout=600)

    with tarfile.open(TRAINER_TAR, mode="x:gz") as tar:
        tar.add(f"{TRAINER_DIR}/")

    bucket.blob(TRAINER_TAR).upload_from_filename(TRAINER_TAR)

    yield bucket

    [blob.delete() for blob in bucket.list_blobs()]
    bucket.delete()

    os.remove(TRAINER_TAR)


@pytest.mark.timeout(1200)
def test_tfkeras(setup_teardown):
    ml = discovery.build('ml', 'v1')

    proj_id = f"projects/{PROJECT_ID}"
    request_dict = {
        "jobId": JOB_ID,
        "trainingInput": {
            "scaleTier": "STANDARD_1",
            "region": REGION,
            "packageUris": [f"gs://{STAGING_BUCKET}/{TRAINER_TAR}"],
            "pythonModule": "trainer.tfkeras_model.task",
            "jobDir": JOB_DIR,
            "runtimeVersion": "2.3",
            "pythonVersion": "3.7",
            "args": [
                "--input-path",
                TRAIN_DATA_PATH
            ]
        }
    }

    response = ml.projects().jobs().create(parent=proj_id,
                                           body=request_dict).execute()

    while (response.get('state') not in TERMINAL_STATES):
        time.sleep(10)
        response = ml.projects().jobs().get(
            name=f"projects/{PROJECT_ID}/jobs/{JOB_ID}").execute()

    assert setup_teardown.blob(f"{MODELS_DIR}/tfkeras_model/saved_model.pb").exists()
