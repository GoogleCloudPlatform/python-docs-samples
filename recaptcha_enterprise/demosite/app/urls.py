# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from backend import create_recaptcha_assessment

from flask import jsonify, render_template, request, Response

SAMPLE_THRESHOLD_SCORE = 0.50

context = {
    "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
    "site_key": os.environ["SITE_KEY"],
}


def home() -> str:
    return render_template(template_name_or_list="home.html", context=context)


def signup() -> str:
    return render_template(template_name_or_list="signup.html", context=context)


def on_signup() -> Response:
    try:
        json_data = json.loads(request.data)
        project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
        credentials = json_data["recaptcha_cred"]

        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Starts -->
        assessment_response = create_recaptcha_assessment.create_assessment(
            project_id,
            context.get("site_key"),
            credentials["token"],
            credentials["action"],
        )

        # Check if the token is valid, score is above threshold score and the action equals expected.
        if assessment_response.token_properties.valid and \
                assessment_response.risk_analysis.score > SAMPLE_THRESHOLD_SCORE and \
                assessment_response.token_properties.action == credentials["action"]:
            # Write new username and password to users database.
            # username = json_data["username"]
            # password = json_data["password"]
            # Business logic.
            verdict = "Not Bad"
            pass
        else:
            # If any of the above condition fails, trigger email/ phone verification flow.
            verdict = "Bad"
            pass
        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Ends -->

        # Return the risk score.
        return jsonify(
            {
                "data": {
                    "score": "{:.1f}".format(assessment_response.risk_analysis.score),
                    "verdict": verdict,
                }
            }
        )
    except ValueError or Exception as e:
        return jsonify({"data": {"error_msg": str(e.__dict__)}})


def login() -> str:
    return render_template(template_name_or_list="login.html", context=context)


def on_login() -> Response:
    try:
        json_data = json.loads(request.data)
        project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
        credentials = json_data["recaptcha_cred"]

        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Starts -->
        assessment_response = create_recaptcha_assessment.create_assessment(
            project_id,
            context.get("site_key"),
            credentials["token"],
            credentials["action"],
        )

        # Check if the token is valid, score is above threshold score and the action equals expected.
        if assessment_response.token_properties.valid and \
                assessment_response.risk_analysis.score > SAMPLE_THRESHOLD_SCORE and \
                assessment_response.token_properties.action == credentials["action"]:
            # Check if the login credentials exist and match.
            # username = json_data["username"]
            # password = json_data["password"]
            # Business logic.
            verdict = "Not Bad"
            pass
        else:
            # If any of the above condition fails, trigger email/phone verification flow.
            verdict = "Bad"
            pass
        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Ends -->

        # Return the risk score.
        return jsonify(
            {
                "data": {
                    "score": "{:.1f}".format(assessment_response.risk_analysis.score),
                    "verdict": verdict,
                }
            }
        )
    except ValueError or Exception as e:
        return jsonify({"data": {"error_msg": str(e.__dict__)}})


def store() -> str:
    return render_template(template_name_or_list="store.html", context=context)


def on_store_checkout() -> Response:
    try:
        json_data = json.loads(request.data)
        project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
        credentials = json_data["recaptcha_cred"]

        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Starts -->
        assessment_response = create_recaptcha_assessment.create_assessment(
            project_id,
            context.get("site_key"),
            credentials["token"],
            credentials["action"],
        )

        # Check if the token is valid, score is above threshold score and the action equals expected.
        if assessment_response.token_properties.valid and \
                assessment_response.risk_analysis.score > SAMPLE_THRESHOLD_SCORE and \
                assessment_response.token_properties.action == credentials["action"]:
            # Check if the cart contains items and proceed to checkout and payment.
            # Business logic.
            verdict = "Not Bad"
            pass
        else:
            # If any of the above condition fails, trigger email/phone verification flow.
            verdict = "Bad"
            pass
        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Ends -->

        # Return the risk score.
        return jsonify(
            {
                "data": {
                    "score": "{:.1f}".format(assessment_response.risk_analysis.score),
                    "verdict": verdict,
                }
            }
        )
    except ValueError or Exception as e:
        return jsonify({"data": {"error_msg": str(e.__dict__)}})


def comment() -> str:
    return render_template(template_name_or_list="comment.html", context=context)


def on_comment_submit() -> Response:
    try:
        json_data = json.loads(request.data)
        project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
        credentials = json_data["recaptcha_cred"]

        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Starts -->
        assessment_response = create_recaptcha_assessment.create_assessment(
            project_id,
            context.get("site_key"),
            credentials["token"],
            credentials["action"],
        )

        # Check if the token is valid, score is above threshold score and the action equals expected.
        if assessment_response.token_properties.valid and \
                assessment_response.risk_analysis.score > SAMPLE_THRESHOLD_SCORE and \
                assessment_response.token_properties.action == credentials["action"]:
            # Check if comment has safe language and proceed to store in database.
            # Business logic.
            verdict = "Not Bad"
            pass
        else:
            # If any of the above condition fails, trigger email/phone verification flow.
            verdict = "Bad"
            pass
        # <!-- ATTENTION: reCAPTCHA Example (Server Part 1/2) Ends -->

        # Return the risk score.
        return jsonify(
            {
                "data": {
                    "score": "{:.1f}".format(assessment_response.risk_analysis.score),
                    "verdict": verdict,
                }
            }
        )
    except ValueError or Exception as e:
        return jsonify({"data": {"error_msg": str(e.__dict__)}})


def game() -> str:
    return render_template(template_name_or_list="game.html", context=context)
