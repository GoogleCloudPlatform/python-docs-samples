# Copyright 2022 Google LLC
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


import datetime
import re

"""
Run the file to update the user_events.json and user_events_some_invalid.json files with more recent timestamp
"""


def update_events_timestamp(json_file):
    # Get the yesterday's date
    request_time = datetime.datetime.now() - datetime.timedelta(days=1)
    day = request_time.date().strftime("%Y-%m-%d")
    print(day)

    # Read in the file
    with open(json_file, 'r') as file:
        filedata = file.read()

    # Replace the target string  '"eventTime":"YYYY-mm-dd' with yesterday date
    filedata = re.sub('\"eventTime\":\"([0-9]{4})-([0-9]{2})-([0-9]{2})',
                      '\"eventTime\":\"' + day, filedata, flags=re.M)

    # Write the file out again
    with open(json_file, 'w') as file:
        file.write(filedata)
    print(f"The {json_file} is updated")


if __name__ == "__main__":
    update_events_timestamp("../resources/user_events.json")
    update_events_timestamp("../resources/user_events_some_invalid.json")
