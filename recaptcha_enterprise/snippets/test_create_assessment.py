#!/usr/bin/env python
# Copyright 2021 Google, Inc
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
#
# All Rights Reserved.
import hashlib
import hmac
import multiprocessing
import os
import re
import secrets
import time
import typing

from _pytest.capture import CaptureFixture
from flask import Flask, render_template, url_for
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from annotate_assessment import annotate_assessment
from create_assessment import create_assessment
from create_mfa_assessment import create_mfa_assessment
from create_site_key import create_site_key
from delete_site_key import delete_site_key

GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
DOMAIN_NAME = "localhost"
# Switch the multi-processing style for Python > 3.7: https://github.com/pytest-dev/pytest-flask/issues/104
multiprocessing.set_start_method("fork")


@pytest.fixture(scope="session")
def app() -> Flask:
    app = Flask(__name__)

    @app.route("/assess/<site_key>", methods=["GET"])
    def assess(site_key: str) -> str:
        return render_template("index.html", site_key=site_key)

    @app.route("/", methods=["GET"])
    def index() -> str:
        return "Helloworld!"

    return app


@pytest.fixture(scope="module")
def browser() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1420,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                               options=chrome_options)
    yield browser
    browser.close()


@pytest.fixture(scope="module")
def recaptcha_site_key() -> str:
    recaptcha_site_key = create_site_key(
        project_id=GOOGLE_CLOUD_PROJECT, domain_name=DOMAIN_NAME
    )
    yield recaptcha_site_key
    delete_site_key(
        project_id=GOOGLE_CLOUD_PROJECT, recaptcha_site_key=recaptcha_site_key
    )


@pytest.mark.usefixtures("live_server")
def test_assessment(
    capsys: CaptureFixture, recaptcha_site_key: str, browser: WebDriver
) -> None:
    # Get token.
    token, action = get_token(recaptcha_site_key, browser)
    # Create assessment.
    assessment_response = assess_token(recaptcha_site_key, token=token, action=action)
    score = str(assessment_response.risk_analysis.score)
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()
    # Parse the assessment_response.name which is of the format:
    # {'project': 'my-project-id', 'assessment': 'assessment-id'}
    assessment_name = client.parse_assessment_path(assessment_response.name).get(
        "assessment"
    )
    assert assessment_name != ""
    set_score(browser, score)

    # Annotate assessment.
    annotate_assessment(project_id=GOOGLE_CLOUD_PROJECT, assessment_id=assessment_name)
    out, _ = capsys.readouterr()
    assert re.search("Annotated response sent successfully !", out)


@pytest.mark.usefixtures("live_server")
def test_mfa_assessment(
        capsys: CaptureFixture, recaptcha_site_key: str, browser: WebDriver
) -> None:
    # Get token.
    token, action = get_token(recaptcha_site_key, browser)
    # Create assessment.
    create_mfa_assessment(
        project_id=GOOGLE_CLOUD_PROJECT,
        recaptcha_site_key=recaptcha_site_key,
        token=token,
        recaptcha_action=action,
        hashed_account_id=get_hashed_account_id(),
        email="abc@example.com",
        phone_number="+12345678901")
    out, _ = capsys.readouterr()
    assert re.search("Result unspecified. Trigger MFA challenge in the client by passing the request token.", out)


def get_token(recaptcha_site_key: str, browser: WebDriver) -> typing.Tuple:
    browser.get(url_for("assess", site_key=recaptcha_site_key, _external=True))
    time.sleep(5)

    browser.find_element(By.ID, "username").send_keys("username")
    browser.find_element(By.ID, "password").send_keys("password")
    browser.find_element(By.ID, "recaptchabutton").click()

    # Timeout of 5 seconds
    time.sleep(5)

    element = browser.find_element(By.CSS_SELECTOR, "#assessment")
    token = element.get_attribute("data-token")
    action = element.get_attribute("data-action")
    return token, action


def assess_token(recaptcha_site_key: str, token: str, action: str) -> Assessment:
    return create_assessment(
        project_id=GOOGLE_CLOUD_PROJECT,
        recaptcha_site_key=recaptcha_site_key,
        token=token,
        recaptcha_action=action,
    )


def set_score(browser: WebDriver, score: str) -> None:
    browser.find_element(By.CSS_SELECTOR, "#assessment").send_keys(score)


def get_hashed_account_id() -> str:
    account_id = "alicebob"
    key = "your_secret_key"

    salt = secrets.token_hex(16)
    salted_account_id = salt + account_id

    # Encode the key and salted message as bytes
    key_bytes = bytes(key, 'utf-8')
    salted_message_bytes = bytes(salted_account_id, 'utf-8')

    # Create an HMAC SHA-256 hash of the salted message using the key
    hashed = hmac.new(key_bytes, salted_message_bytes, hashlib.sha256)

    # Get the hex-encoded digest of the hash
    return hashed.hexdigest()
