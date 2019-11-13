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
        "SHOULD_PASS_VPCSC": "True",
        "GCLOUD_PROJECT": "dlp-prober-prod",
    }
    tests_path = "tests/inspect_content_test.py"
    if not os.path.exists(tests_path):
        session.skip("tests were not found")
    session.run("pytest", "--quiet", tests_path, env=env)


@nox.session
def vpc_disabled(session):
    # Additional setup for VPCSC system tests
    env = {
        "SHOULD_PASS_VPCSC": "False",
        "GCLOUD_PROJECT": "vpcsc-dlp-1569864437-dut-0",
    }
    tests_path = "tests/inspect_content_test.py"
    if not os.path.exists(tests_path):
        session.skip("tests were not found")
    session.run("pytest", "--quiet", tests_path, env=env)
