# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from functions_framework import create_app


def test_googlechatbot():
    expected = {
        "cardsV2": {
            "cardId": "avatarCard",
            "card": {
                "name": "Avatar Card",
                "header": {"title": "Hello janedoe!"},
                "sections": [
                    {
                        "widgets": [
                            {"textParagraph": {"text": "Your avatar picture: "}},
                            {"image": {"imageUrl": "example.com/avatar.png"}},
                        ]
                    }
                ],
            },
        }
    }

    request = {
        "message": {
            "sender": {
                "displayName": "janedoe",
                "avatarUrl": "example.com/avatar.png",
            },
        },
    }

    tc = create_app("googlechatbot", "main.py").test_client()
    res = tc.post(
        "/",
        data=json.dumps(request),
        headers={
            "Content-Type": "application/json",
        },
    )

    print(res.data.decode("utf-8"))

    assert res.status == "200 OK"
    assert expected == json.loads(res.data.decode("utf-8"))
