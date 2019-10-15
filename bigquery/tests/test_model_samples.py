# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .. import delete_model
from .. import get_model
from .. import list_models
from .. import update_model


def test_model_samples(capsys, client, dataset_id, model_id):
    """Since creating a model is a long operation, test all model samples in
    the same test, following a typical end-to-end flow.
    """
    get_model.get_model(client, model_id)
    out, err = capsys.readouterr()
    assert model_id in out

    list_models.list_models(client, dataset_id)
    out, err = capsys.readouterr()
    assert "Models contained in '{}':".format(dataset_id) in out

    update_model.update_model(client, model_id)
    out, err = capsys.readouterr()
    assert "This model was modified from a Python program." in out

    delete_model.delete_model(client, model_id)
    out, err = capsys.readouterr()
    assert "Deleted model '{}'.".format(model_id) in out
