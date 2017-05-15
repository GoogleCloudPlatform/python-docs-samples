# Copyright 2017 Google Inc.
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

"""This module contains various strategies for upscaling and downscaling
Bigtable."""


def _upscale_incremental_strategy(current_nodes):
    """Simple scaling strategy, increase nodes by 2."""
    return current_nodes + 2


UPSCALE_STRATEGIES = {
    'incremental': _upscale_incremental_strategy
}

"""UPSCALE_STRATEGIES contains a dict of functions for scaling Bigtable.

The function signature should accept the current number of nodes and return
the new number of nodes to scale to.
"""


def _downscale_incremental_strategy(current_nodes):
    """Simple downscale strategy: decrease nodes by 2."""
    new_nodes = current_nodes - 2
    if new_nodes < 3:  # 3 is minimum number of CBT nodes
        return 3
    return new_nodes


DOWNSCALE_STRATEGIES = {
    'incremental': _downscale_incremental_strategy
}

"""DOWNSCALE_STRATEGIES contains a dict of functions for scaling Bigtable.

The function signature should accept the current number of nodes and return
the new number of nodes to scale to.
"""
