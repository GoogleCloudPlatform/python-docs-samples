# Copyright 2021 Google LLC
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

from google.appengine.ext import vendor
import pkg_resources

# Set path to your libraries folder.
path = "lib"
# Add libraries installed in the path folder.
vendor.add(path)
# Add libraries to pkg_resources working set to find the distribution.
pkg_resources.working_set.add_entry(path)
