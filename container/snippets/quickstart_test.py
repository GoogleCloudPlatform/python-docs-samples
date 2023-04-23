# Copyright 2022 Google LLC
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

import os

import quickstart as gke_list

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
ZONE = "us-central1-b"


def test_list_clusters(capsys: object) -> None:
    output_prefix = "There were "
    output_suffix = f" clusters in {ZONE} for project {PROJECT_ID}."

    gke_list.list_clusters(PROJECT_ID, ZONE)
    out, _ = capsys.readouterr()

    """
    Typical output looks as follows:

      There were 3 clusters in us-central1-b for project test-project.
       - cluster1
       - cluster2
       - cluster3

    Split array by '\n'
        [
            "There were 3 clusters in us-central1-b for project test-project.",
            "- cluster1",
            "- cluster2",
            "- cluster3",
            "",
        ]
    """
    out_lines = out.split("\n")
    first_line = out_lines[0]
    first_line = first_line.replace(output_prefix, "")
    first_line = first_line.replace(output_suffix, "")
    cluster_count = int(first_line)  # get the cluster count in the first line

    assert output_suffix in out
    assert cluster_count == len(out_lines) - 2
