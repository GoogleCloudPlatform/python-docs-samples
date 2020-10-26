import os
import uuid

from google.cloud import storage
from googleapiclient import discovery
import pytest

STAGING_BUCKET = f"sklearn-job-dir-{uuid.uuid4()}"
INPUT_DIR = "inputs"
MODELS_DIR = "models"
JOB_DIR = STAGING_BUCKET + "/" + MODELS_DIR
TRAIN_DATA = "train.csv"
TRAIN_DATA_PATH = f"gs://{STAGING_BUCKET}/{INPUT_DIR}/{TRAIN_DATA}"

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-east1"
MODEL_NAME = f"sklearn-test-{uuid.uuid4()}"
JOB_ID = f"sklearn_{str(uuid.uuid4())[:7]}"


@pytest.fixture(autouse=True)
def setup_teardown():
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(STAGING_BUCKET)
    bucket.blob(INPUT_DIR).upload_from_filename(TRAIN_DATA)

    yield bucket

    [blob.delete() for blob in bucket.list_blobs()]
    bucket.delete()


def test_sklearn(setup_teardown):
    ml = discovery.build('ml', 'v1')

    proj_id = f"projects/{PROJECT_ID}"
    request_dict = {
        "jobId": JOB_ID,
        "trainingInput": {
            "region": REGION,
            "packageUris": ["trainer/"],
            "pythonModule": "trainer.sklearn_model.task",
            "jobDir": JOB_DIR,
            "runtimeVersion": "2.2",
            "pythonVersion": "3.7",
            "args": [
                "--input-path",
                TRAIN_DATA_PATH
            ]
        }
    }

    response = ml.projects().jobs().create(parent=proj_id,
                                           body=request_dict).execute()

    assert setup_teardown.blob(f"{MODELS_DIR}/model.joblib").exists()
