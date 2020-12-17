import os
import glob
import uuid

from google.cloud import storage
from googleapiclient import discovery
import pytest

STAGING_BUCKET = f"sklearn-job-dir-{uuid.uuid4()}"
INPUT_DIR = "inputs"
TRAINER_DIR = "trainer"
MODELS_DIR = "models"
JOB_DIR = f"{STAGING_BUCKET}/{MODELS_DIR}"
TRAIN_DATA = "train.csv"
TRAIN_DATA_PATH = f"gs://{STAGING_BUCKET}/{INPUT_DIR}/{TRAIN_DATA}"

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-east1"
MODEL_NAME = f"sklearn-test-{uuid.uuid4()}"
JOB_ID = f"sklearn_{str(uuid.uuid4())[:7]}"


def copy_dir_to_gcs(local_path, gcs_path, bucket):
    for path in glob.glob(f"{local_path}/**"):
        new_gcs_path = f"{gcs_path}/{os.path.basename(path)}"
        if not os.path.isfile(path):
            copy_dir_to_gcs(path, new_gcs_path, bucket)
        else:
            bucket.blob(new_gcs_path).upload_from_filename(path)
        

@pytest.fixture(autouse=True)
def setup_teardown():
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(STAGING_BUCKET)
    bucket.blob(INPUT_DIR).upload_from_filename(TRAIN_DATA)
    copy_dir_to_gcs(f"{TRAINER_DIR}/", TRAINER_DIR, bucket)

    yield bucket

    [blob.delete() for blob in bucket.list_blobs()]
    bucket.delete()


def test_sklearn(setup_teardown):
    ml = discovery.build('ml', 'v1')

    proj_id = f"projects/{PROJECT_ID}"
    request_dict = {
        "jobId": JOB_ID,
        "trainingInput": {
            "scaleTier": "STANDARD_1",
            "region": REGION,
            "packageUris": [f"gs://{STAGING_BUCKET}/{TRAINER_DIR}/"],
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
