# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tutorial


def test_neutral():
    result = tutorial.get_response('reviews/bladerunner-neutral.txt')
    assert result['language'] == 'en'
    assert (-1 < result['documentSentiment']['score'] < 1)
    assert (0 < result['documentSentiment']['magnitude'] < 2.0)


def test_pos():
    result = tutorial.get_response('reviews/bladerunner-pos.txt')
    assert result['language'] == 'en'
    assert result['documentSentiment']['score'] > 0.0
    assert result['documentSentiment']['magnitude'] > 2.0


def test_neg():
    result = tutorial.get_response('reviews/bladerunner-neg.txt')
    assert result['language'] == 'en'
    assert result['documentSentiment']['score'] < 0.0
    assert result['documentSentiment']['magnitude'] > 1.0


def test_mixed():
    result = tutorial.get_response('reviews/bladerunner-mixed.txt')
    assert result['language'] == 'en'
    assert (-1 < result['documentSentiment']['score'] < 1)
    assert result['documentSentiment']['magnitude'] > 4.0
