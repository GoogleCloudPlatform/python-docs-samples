#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

import sys

# [START storage_define_bucket_website_configuration]
from google.cloud import storage


def define_bucket_website_configuration(bucket_name, main_page_suffix, not_found_page):
    """Configure website-related properties of bucket"""
    # bucket_name = "your-bucket-name"
    # main_page_suffix = "index.html"
    # not_found_page = "404.html"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.configure_website(main_page_suffix, not_found_page)
    bucket.patch()

    print(
        "Static website bucket {} is set up to use {} as the index page and {} as the 404 page".format(
            bucket.name, main_page_suffix, not_found_page
        )
    )
    return bucket


# [END storage_define_bucket_website_configuration]

if __name__ == "__main__":
    define_bucket_website_configuration(
        bucket_name=sys.argv[1],
        main_page_suffix=sys.argv[2],
        not_found_page=sys.argv[3],
    )
