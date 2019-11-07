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
def vpc_enabled(session):

    # Additional setup for VPCSC system tests
    env = {
        "SHOULD_PASS": "True",
        "GCLOUD_PROJECT": os.environ.get("GCLOUD_PROJECT"),
    }
    tests_path = "tests/inspect_content_test.py"
    if not os.path.exists(tests_path):
      session.skip("tests were not found")
    session.run("pytest", "--quiet", tests_path, env=env)
