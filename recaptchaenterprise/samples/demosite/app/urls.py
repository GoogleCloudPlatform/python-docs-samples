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

from flask import render_template, request, Response

from backend.recaptcha import execute_create_assessment

context = {
    "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
    "site_key": os.environ["SITE_KEY"]
}


def home() -> str:
    return render_template(template_name_or_list="home.html", context=context)


def signup() -> str:
    return render_template(template_name_or_list="signup.html", context=context)


def login() -> str:
    return render_template(template_name_or_list="login.html", context=context)


def store() -> str:
    return render_template(template_name_or_list="store.html", context=context)


def comment() -> str:
    return render_template(template_name_or_list="comment.html", context=context)


def game() -> str:
    return render_template(template_name_or_list="game.html", context=context)


def create_assessment() -> Response:
    json_data = json.loads(request.data)
    return execute_create_assessment(os.environ["GOOGLE_CLOUD_PROJECT"], json_data)
