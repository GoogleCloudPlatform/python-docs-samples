# Copyright 2021 Google Inc. All Rights Reserved.
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

import re
import subprocess

from products_delete_gcs_bucket import delete_bucket_by_name


def test_create_gcs_bucket():
    output = str(
        subprocess.check_output(
            'python setup/products_create_gcs_bucket.py',
            shell=True))

    bucket_name = re.search('The gcs bucket (.+?) was created', output).group(1)
    delete_bucket_by_name(bucket_name)

    print("bucket_name = {}".format(bucket_name))

    assert re.match(
        '.*Creating new bucket.*', output)
    assert re.match(
        '(.*The gcs bucket.*?was created.*|.*Bucket.*?already exists.*)', output)
    assert re.match(
        '.*Uploading data from ../resources/products.json to the bucket.*', output)
    assert re.match(
        '.*Uploading data from ../resources/products_some_invalid.json to the bucket.*',
        output)
