# Copyright 2017 Google Inc.
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

import redact

def test_redact_string(capsys):
    test_string = 'I am Gary and my email is gary@example.com'

    redact.redact_string(test_string, 'REDACTED')

    out, _ = capsys.readouterr()
    assert 'REDACTED' in out

def test_redact_string_with_info_types(capsys):
    test_string = 'My email is gary@example.com and my number is 206-555-5555'

    redact.redact_string(test_string, 'REDACTED',
        info_types=['PHONE_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'REDACTED' in out
    assert out.count('REDACTED') == 1

def test_redact_string_no_findings(capsys):
    test_string = 'Nothing to see here'

    redact.redact_string(test_string, 'REDACTED')

    out, _ = capsys.readouterr()
    assert 'REDACTED' not in out
