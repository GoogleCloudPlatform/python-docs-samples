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

"""Defines custom PTransforms and DoFns used in the pipleines."""

from collections.abc import Iterable
import re

import apache_beam as beam


class WordExtractingDoFn(beam.DoFn):
    """Parses each line of input text into words."""

    def process(self, element: str) -> Iterable[str]:
        return re.findall(r"[\w\']+", element, re.UNICODE)


class FindLongestWord(beam.PTransform):
    """Extracts words from text and finds the longest one."""

    def expand(self, pcoll):
        return (
            pcoll
            | "Extract words" >> beam.ParDo(WordExtractingDoFn())
            | "Find longest" >> beam.combiners.Top.Largest(n=1, key=len)
        )
