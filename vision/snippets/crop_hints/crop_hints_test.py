# Copyright 2017 Google LLC
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

import os

import crop_hints


def test_crop(capsys):
    """Checks the output image for cropping the image is created."""
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/cropme.jpg')
    crop_hints.crop_to_hint(file_name)
    out, _ = capsys.readouterr()
    assert os.path.isfile('output-crop.jpg')


def test_draw(capsys):
    """Checks the output image for drawing the crop hint is created."""
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/cropme.jpg')
    crop_hints.draw_hint(file_name)
    out, _ = capsys.readouterr()
    assert os.path.isfile('output-hint.jpg')
