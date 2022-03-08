# Copyright 2021 Google LLC
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

from ..images.get import get_image
from ..images.list import list_images


def test_list_images():
    images = list_images("debian-cloud")
    for img in images:
        assert img.kind == "compute#image"
        assert img.self_link.startswith(
            "https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/"
        )


def test_get_image():
    images = list_images("debian-cloud")
    image = next(iter(images))

    image2 = get_image("debian-cloud", image.name)

    assert image == image2
