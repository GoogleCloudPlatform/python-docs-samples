import json
import os

from flask import render_template, request, Response

from backend.recaptcha import execute_create_assessment


def login() -> str:
    # TODO: These env variables should be made available through Cloud Run's env vars.
    context = {
        "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
        "site_key": os.environ["SITE_KEY"]
    }
    return render_template(template_name_or_list="login.html", context=context)


def signup() -> str:
    context = {
        "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
        "checkbox_site_key": os.environ["CHECKBOX_SITE_KEY"]
    }
    return render_template(template_name_or_list="signup.html", context=context)


def create_assessment() -> Response:
    json_data = json.loads(request.data)
    return execute_create_assessment(os.environ["GOOGLE_CLOUD_PROJECT"], json_data)
