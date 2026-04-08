# Copyright 2026 Google LLC
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

from unittest import mock

from google.cloud import retail_v2
import pytest

from search_offset import search_offset


@pytest.fixture
def test_config(project_id):
    return {
        "project_id": project_id,
        "placement_id": "default_placement",
        "visitor_id": "test_visitor",
    }


@mock.patch.object(retail_v2.SearchServiceClient, "search")
def test_search_offset(mock_search, test_config, capsys):
    # Mock result
    mock_product = mock.Mock()
    mock_product.id = "product_at_offset"
    mock_product.title = "Offset Title"

    mock_result = mock.Mock()
    mock_result.product = mock_product

    mock_page = mock.MagicMock()
    mock_page.results = [mock_result]
    mock_pager = mock.MagicMock()
    mock_pager.pages = iter([mock_page])
    mock_pager.__iter__.return_value = [mock_result]
    mock_search.return_value = mock_pager

    search_offset(
        project_id=test_config["project_id"],
        placement_id=test_config["placement_id"],
        visitor_id=test_config["visitor_id"],
        query="test query",
        offset=10,
    )

    out, _ = capsys.readouterr()
    assert "--- Results for offset: 10 ---" in out
    assert "Product ID: product_at_offset" in out

    # Verify call request
    args, kwargs = mock_search.call_args
    request = kwargs.get("request") or args[0]
    assert request.offset == 10
    assert request.page_size == 10
    assert request.query == "test query"
