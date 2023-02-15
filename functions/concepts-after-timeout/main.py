# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_concepts_after_timeout]
import time

import functions_framework


@functions_framework.http
def timeout(request):
    print('Function running...')
    time.sleep(120)

    # May not execute if function's timeout is <2 minutes
    print('Function completed!')
    return 'Function completed!'
# [END functions_concepts_after_timeout]
