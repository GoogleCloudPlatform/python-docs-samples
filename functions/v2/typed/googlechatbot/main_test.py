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

import main


def test_googlechatbot():
    expected = main.ChatResponse(
        "avatarCard",
        {
            "name": "Avatar Card",
            "header": {
                "title": "Hello janedoe!",
            },
            "sections": [
                {
                    "widgets": [
                        {
                            "textParagraph": {
                                "text": "Your avatar picture: ",
                            },
                        },
                        {
                            "image": {
                                "imageUrl": "example.com/avatar.png",
                            },
                        },
                    ],
                },
            ],
        },
    )

    request = {
        "message": {
            "sender": {
                "displayName": "janedoe",
                "avatarUrl": "example.com/avatar.png",
            },
        },
    }

    req = main.ChatRequest.from_dict(request)
    res = main.googlechatbot(req)
    assert expected == res
