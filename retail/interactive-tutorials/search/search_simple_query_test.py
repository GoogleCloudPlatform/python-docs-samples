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

# Call Retail API to search for a products in a catalog using only search query.
#
import re
import subprocess

from google.api_core.retry import Retry

from search_simple_query import search


@Retry()
def test_search_simple_query_pass():
    output = str(subprocess.check_output("python search_simple_query.py", shell=True))

    assert re.match(".*search request.*", output)
    assert re.match(".*search response.*", output)
    # check the response contains some products
    assert re.match(".*results.*id.*", output)


def test_search_simple_query_response():
    query_phrase = "Hoodie"
    response = search(query_phrase)

    assert len(response.results) <= 10
    assert len(response.results) >= 1

    for result in response.results:
        product_title = result.product.title
        if re.search(query_phrase, product_title, flags=re.IGNORECASE) is not None:
            assert f"{query_phrase} was found in {product_title}"
            return

    assert f"{query_phrase} was not Found" is None
