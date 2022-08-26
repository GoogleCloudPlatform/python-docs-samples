# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# this script is used to preprocess the ghcn-stations.txt public data file
# found on the info site about the structure of the ghcn data set:
# https://docs.opendata.aws/noaa-ghcn-pds/readme.html
# users can run it once if they wish to process the data on their own
# otherwise, we include a processed version of the data in this repo
import csv


def preprocess_station_data(input_filename: str, output_filename: str) -> None:
    out = open(output_filename, "w")
    with open(input_filename) as f:
        data = f.readlines()

        rows = []
        # Each line is a string and the character position determines the column as dictated in the README
        # https://docs.opendata.aws/noaa-ghcn-pds/readme.html
        # Map the positions appropriately, strip them of trailing and leading whitespace,
        # and skip the final three columns which aren't relevant for our use case
        """
        Variable	Columns	Type	Example
        ID	1-11	Character	EI000003980
        LATITUDE	13-20	Real	55.3717
        LONGITUDE	22-30	Real	-7.3400
        ELEVATION	32-37	Real	21.0
        STATE	39-40	Character
        NAME	42-71	Character	MALIN HEAD
        GSN FLAG	73-75	Character	GSN
        HCN/CRN FLAG	77-79	Character
        WMO ID	81-85	Character	03980
        """
        for row in data:
            row = [
                row[0:12].strip(),
                row[12:21].strip(),
                row[21:31].strip(),
                row[31:38].strip(),
                row[38:41].strip(),
                row[41:72].strip(),
            ]
            rows.append(row)

    with out:
        write = csv.writer(out)
        write.writerows(rows)


if __name__ == "__main__":
    preprocess_station_data("ghcnd-stations.txt", "ghcn-stations-processed.csv")
