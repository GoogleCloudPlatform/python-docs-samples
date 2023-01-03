# -*- encoding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import translate_v3_translate_text_with_model


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
MODEL_ID = "TRL251293382528204800"


def test_translate_text_with_model(capsys):
    translate_v3_translate_text_with_model.translate_text_with_model(
        "That' il do it.", PROJECT_ID, MODEL_ID
    )
    out, _ = capsys.readouterr()
    assert "それはそうだ" or "それじゃあ" in out
