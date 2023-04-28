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

import pytest

from google.cloud.aiplatform.private_preview.language_models import TextGenerationModel

import ideation


interview_expected_response = '''1. Tell me about a time when you successfully managed a complex project. What were the challenges you faced, and how did you overcome them?
2. What is your approach to planning and prioritizing tasks?
3. How do you communicate with and collaborate with stakeholders?
4. What is your experience with project management software?
5. What are your strengths and weaknesses as a program manager?
6. What are your career goals?
7. Why are you interested in this role?
8. What do you know about our company?
9. What can you contribute to our company?
10. Do you have any questions for me?

These questions are designed to assess your skills and experience in project management, as well as your fit for the role and company. Be prepared to answer them thoughtfully and honestly, and to provide specific examples from your past experience.'''

def test_interview():
    content = ideation.interview(temperature=0).text
    assert content == interview_expected_response
    print(f'Response from Model: {content}')