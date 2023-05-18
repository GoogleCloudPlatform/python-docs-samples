# Copyright 2023 Google LLC
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

import ideation


interview_expected_response = '''1. What is your experience with project management?
2. What is your process for managing a project?
3. How do you handle unexpected challenges or roadblocks?
4. How do you communicate with stakeholders?
5. How do you measure the success of a project?
6. What are your strengths and weaknesses as a project manager?
7. What are your salary expectations?
8. What are your career goals?
9. Why are you interested in this position?
10. What questions do you have for me?'''


def test_interview() -> None:
    content = ideation.interview(temperature=0).text
    assert content == interview_expected_response
