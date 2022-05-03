#!/usr/bin/env python
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

import os

import subprocess
import tarfile
import uuid


def download_file(bucket_name: str, blob_name: str, destination_file: str) -> str:
    """Copies a remote GCS file to a local path"""
    remote_file_path = "".join(["gs://", "/".join([bucket_name, blob_name])])

    subprocess.check_output(
        ["gsutil", "cp", remote_file_path, destination_file], encoding="UTF-8"
    )

    return destination_file


def upload_file(
    local_file_path: str,
    remote_file_path: str,
) -> str:
    """Copies a local file to a GCS path"""
    subprocess.check_output(
        ["gsutil", "cp", local_file_path, remote_file_path], encoding="UTF-8"
    )

    return remote_file_path


def archive_code_and_upload(staging_bucket: str):
    # Archive all source in current directory
    unique_id = uuid.uuid4()
    source_archived_file = f"source_archived_{unique_id}.tar.gz"

    git_files = subprocess.check_output(
        ["git", "ls-tree", "-r", "HEAD", "--name-only"], encoding="UTF-8"
    ).split("\n")

    with tarfile.open(source_archived_file, "w:gz") as tar:
        for file in git_files:
            if len(file) > 0 and os.path.exists(file):
                tar.add(file)

    # Upload archive to GCS bucket
    source_archived_file_gcs = upload_file(
        local_file_path=f"{source_archived_file}",
        remote_file_path="/".join(
            [staging_bucket, "code_archives", source_archived_file]
        ),
    )

    print(f"Uploaded source code archive to {source_archived_file_gcs}")

    return source_archived_file_gcs
