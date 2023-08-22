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


# [START functions_typed_googlechatbot]
from dataclasses import dataclass
from typing import Any, Dict, List, Union

import functions_framework


@dataclass
class ChatRequest:
    message: Dict[str, Union[str, Dict[str, str], List[Dict[str, str]]]]

    # Required to deserialize the request
    @staticmethod
    def from_dict(req: dict) -> "ChatRequest":
        return ChatRequest(message=req["message"])


@dataclass
class ChatResponse:
    cardId: str
    card: Dict[str, Any]

    # Required to serialize the response
    def to_dict(self) -> dict:
        return {
            "cardsV2": {
                "cardId": self.cardId,
                "card": self.card,
            }
        }


@functions_framework.typed
def googlechatbot(req: ChatRequest) -> ChatResponse:
    displayName = req.message["sender"]["displayName"]
    imageUrl = req.message["sender"]["avatarUrl"]

    cardHeader = {
        "title": f"Hello {displayName}!",
    }

    avatarWidget = {
        "textParagraph": {"text": "Your avatar picture: "},
    }

    avatarImageWidget = {
        "image": {"imageUrl": imageUrl},
    }

    avatarSection = {
        "widgets": [avatarWidget, avatarImageWidget],
    }

    return ChatResponse(
        cardId="avatarCard",
        card={
            "name": "Avatar Card",
            "header": cardHeader,
            "sections": [avatarSection],
        },
    )


# [END functions_typed_googlechatbot]
