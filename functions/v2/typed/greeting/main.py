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


# [START functions_typed_greeting]
from dataclasses import dataclass

import functions_framework


@dataclass
class GreetingRequest:
    first_name: str
    last_name: str

    # Required to deserialize the request
    @staticmethod
    def from_dict(req: dict) -> "GreetingRequest":
        return GreetingRequest(
            first_name=req["first_name"],
            last_name=req["last_name"],
        )


@dataclass
class GreetingResponse:
    message: str

    # Required to serialize the response
    def to_dict(self) -> dict:
        return {
            "message": self.message,
        }


@functions_framework.typed
def greeting(req: GreetingRequest):
    return GreetingResponse(message=f"Hello {req.first_name} {req.last_name}!")


# [END functions_typed_greeting]
