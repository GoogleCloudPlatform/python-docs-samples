# Copyright 2024 Google LLC
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

"""
Top-level entry point that launches the pipeline.

In this example, the Python pipeline is defined in a package, consisting of
several modules. This file provides the entrypoint that launches the
workflow defined in the package.

This entrypoint will be called when the Flex Template starts.

The my_package package should be installed in the Flex Template image, and
in the runtime environment. The latter could be accomplished with the
--setup_file pipeline option or by supplying a custom container image.
"""

import logging

from my_package import launcher

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    launcher.run()
