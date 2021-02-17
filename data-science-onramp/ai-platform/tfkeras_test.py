import os
import tarfile
import time
import uuid

from google.cloud import storage
from google.cloud.aiplatform import gapic as aip
import pytest

STAGING_BUCKET = f"tfkeras-job-dir-{uuid.uuid4()}"
INPUT_DIR = "inputs"
TRAINER_DIR = "modules"
MODEL_DIR = "model"
TRAIN_DATA = "train.csv"
TRAINER_TAR = "trainer.tar.gz"
TRAIN_DATA_PATH = f"gs://{STAGING_BUCKET}/{INPUT_DIR}/{TRAIN_DATA}"

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
MODEL_NAME = f"tfkeras-test-{uuid.uuid4()}"
JOB_ID = f"tfkeras_{str(uuid.uuid4())[:7]}"
DEPLOY_IMAGE = "gcr.io/cloud-aiplatform/training/tf-cpu.2-3:latest"

TERMINAL_STATES = [
    aip.JobState.JOB_STATE_SUCCEEDED,
    aip.JobState.JOB_STATE_FAILED,
    aip.JobState.JOB_STATE_CANCELLING,
    aip.JobState.JOB_STATE_CANCELLED
]


@pytest.fixture
def shared_state():
    state = {}
    yield state

@pytest.fixture(autouse=True)
def setup_teardown(shared_state):
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(STAGING_BUCKET, location=REGION)
    bucket.blob(f"{INPUT_DIR}/{TRAIN_DATA}").upload_from_filename(TRAIN_DATA, timeout=600)

    with tarfile.open(TRAINER_TAR, mode="x:gz") as tar:
        tar.add(f"{TRAINER_DIR}/")

    bucket.blob(TRAINER_TAR).upload_from_filename(TRAINER_TAR)

    aip_job_client = aip.JobServiceClient(
        client_options={
            "api_endpoint": f"{REGION}-aiplatform.googleapis.com"
        }
    )

    yield bucket, aip_job_client

    [blob.delete() for blob in bucket.list_blobs()]
    bucket.delete()

    os.remove(TRAINER_TAR)

    aip_job_client.delete_custom_job(name=shared_state["model_name"]).result()

@pytest.mark.timeout(1200)
def test_tfkeras(setup_teardown, shared_state):
    bucket, aip_job_client = setup_teardown

    custom_job = {
        "display_name": JOB_ID,
        "job_spec": {
            "base_output_directory": {"output_uri_prefix": f"gs://{STAGING_BUCKET}"},
            "worker_pool_specs": [{
                "replica_count": 1,
                "machine_spec": {
                    "machine_type": "n1-standard-4",
                },
                "python_package_spec": {
                    "executor_image_uri": DEPLOY_IMAGE,
                    "package_uris": [f"gs://{STAGING_BUCKET}/{TRAINER_TAR}"],
                    "python_module": "trainer.tfkeras_model.task",
                    "args": [
                        "--input-path",
                        TRAIN_DATA_PATH
                    ]
                }
            }]
        }
    }

    parent = f"projects/{PROJECT_ID}/locations/{REGION}"
    response = aip_job_client.create_custom_job(
        parent=parent, custom_job=custom_job
    )
    resource_name = response.name
    shared_state["model_name"] = resource_name

    while (response.state not in TERMINAL_STATES):
        time.sleep(10)
        response = aip_job_client.get_custom_job(name=resource_name)

    assert bucket.blob(f"{MODEL_DIR}/tfkeras_model/saved_model.pb").exists()
