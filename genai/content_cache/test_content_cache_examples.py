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

import os

import contentcache_create_with_txt_gcs_pdf
import contentcache_delete
import contentcache_list
import contentcache_update
import contentcache_use_with_txt


os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


def test_content_cache() -> None:
    # Create a Cache
    cache_name = contentcache_create_with_txt_gcs_pdf.create_content_cache()
    assert cache_name

    # List cache
    assert contentcache_list.list_context_caches()

    # Update cache
    assert contentcache_update.update_content_cache(cache_name)

    # Use cache
    assert contentcache_use_with_txt.generate_content(cache_name)

    # Delete cache
    assert contentcache_delete.delete_context_caches(cache_name)


if __name__ == "__main__":
    test_content_cache()
