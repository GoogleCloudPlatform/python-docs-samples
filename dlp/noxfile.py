from __future__ import absolute_import
import os
import shutil

import nox


BLACK_VERSION = "black==19.3b0"
BLACK_PATHS = ["tests", "noxfile.py"]

if os.path.exists("samples"):
    BLACK_PATHS.append("samples")


@nox.session
def setup(session):
    # Same as pip install -r -r requirements.txt.
    session.install("-r", "requirements.txt")
    session.install("mock", "pytest")

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable")

@nox.session
@nox.parametrize("bucket_name", ["GOOGLE_CLOUD_TESTS_VPCSC_INSIDE_PERIMETER_BUCKET", "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_BUCKET"])
def vpc_enabled(session, bucket_name):

    # Additional setup for VPCSC system tests
    env = {
        "VPC_ENABLED": True,
        "GCLOUD_PROJECT": os.environ.get("GCLOUD_PROJECT"),
        "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT": os.environ.get(
            "GCLOUD_PROJECT"
        ),
        "TEST_BUCKET_NAME": os.environ.get(bucket_name),
    }
    tests_path = "tests"
    if not os.path.exists(tests_path):
      session.skip("tests were not found")
    session.run("pytest", "--quiet", tests_path, env=env)
