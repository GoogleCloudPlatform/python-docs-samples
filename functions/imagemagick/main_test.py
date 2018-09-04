# Copyright 2018 Google LLC
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

import uuid

from mock import MagicMock, patch

import main


class DictObject(dict):
    pass


@patch('main.__blur_image')
def test_do_nothing_on_delete(__blur_image, capsys):
    __blur_image = MagicMock()
    data = {
      'resource_state': 'not_exists',
      'name': ''
    }

    main.blur_offensive_images(data, None)

    out, _ = capsys.readouterr()
    assert 'This is a deletion event.' in out
    assert __blur_image.called is False


@patch('main.__blur_image')
def test_do_nothing_on_deploy(__blur_image, capsys):
    __blur_image = MagicMock()

    main.blur_offensive_images({}, None)

    out, _ = capsys.readouterr()
    assert 'This is a deploy event.' in out
    assert __blur_image.called is False


@patch('main.__blur_image')
@patch('main.vision_client')
@patch('main.storage_client')
def test_process_offensive_image(
  __blur_image,
  vision_client,
  storage_client,
  capsys):
    result = DictObject()
    result.safe_search_annotation = DictObject()
    result.safe_search_annotation.adult = 'VERY_LIKELY'
    result.safe_search_annotation.violence = 'VERY_LIKELY'
    vision_client.safe_search_detection = MagicMock(return_value=result)

    filename = str(uuid.uuid4())
    data = {
      'resource_state': '',
      'bucket': 'my-bucket',
      'name': filename
    }

    main.blur_offensive_images(data, None)

    out, _ = capsys.readouterr()
    assert 'Analyzing %s.' % filename in out
    assert 'The image %s was detected as inappropriate.' % filename in out
    assert main.__blur_image.called


@patch('main.__blur_image')
@patch('main.vision_client')
@patch('main.storage_client')
def test_process_safe_image(
  __blur_image,
  vision_client,
  storage_client,
  capsys):
    result = DictObject()
    result.safe_search_annotation = DictObject()
    result.safe_search_annotation.adult = 'VERY_UNLIKELY'
    result.safe_search_annotation.violence = 'VERY_UNLIKELY'
    vision_client.safe_search_detection = MagicMock(return_value=result)

    filename = str(uuid.uuid4())
    data = {
      'resource_state': '',
      'bucket': 'my-bucket',
      'name': filename
    }

    main.blur_offensive_images(data, None)

    out, _ = capsys.readouterr()
    assert 'Analyzing %s.' % filename in out
    assert 'The image %s was detected as OK.' % filename in out
    assert __blur_image.called is False


@patch('main.os')
@patch('main.subprocess')
def test_blur_image(subprocess_mock, os_mock, capsys):
    filename = str(uuid.uuid4())

    os_mock.remove = MagicMock()
    os_mock.path = MagicMock()
    os_mock.path.basename = MagicMock(side_effect=(lambda x: x))

    subprocess_mock.check_call = MagicMock()

    blob_mock = MagicMock()
    blob_mock.upload_from_file = MagicMock()

    file = DictObject()
    file['name'] = filename
    file.download_to_filename = MagicMock()
    file.blob = MagicMock(return_value=blob_mock)

    main.__blur_image(file)

    out, _ = capsys.readouterr()

    assert 'Image %s was downloaded to /tmp/%s.' % (filename, filename) in out
    assert 'Image %s was blurred.' % filename in out
    assert 'Blurred image was uploaded to %s.' % filename in out
    assert os_mock.remove.called
    assert subprocess_mock.check_call.called
