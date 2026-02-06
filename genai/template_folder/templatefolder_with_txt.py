# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def greetings(user_name: str) -> str:
    # [START googlegenaisdk_TEMPLATEFOLDER_with_txt]
    # Example user_name = "Sampath"
    print(f"Hello World!\nHow are you doing today, {user_name}?")
    # Example response:
    #   Hello World!
    #   How are you doing today, Sampath?
    # [END googlegenaisdk_TEMPLATEFOLDER_with_txt]
    return user_name


if __name__ == "__main__":
    greetings(input("UserName:"))
