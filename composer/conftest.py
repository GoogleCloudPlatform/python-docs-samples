# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import tempfile

import pytest


# this fixture initializes the Airflow DB once per session
# it is used by DAGs in both the blogs and workflows directories,
# unless there exists a conftest at a lower level
@pytest.fixture(scope="session")
def airflow_database():
    import airflow.utils.db

    # We use separate directory for local db path per session
    # by setting AIRFLOW_HOME env var, which is done in noxfile_config.py.

    assert 'AIRFLOW_HOME' in os.environ

    airflow_home = os.environ["AIRFLOW_HOME"]
    airflow_db = f"{airflow_home}/airflow.db"

    # reset both resets and initializes a new database
    airflow.utils.db.resetdb()

    # Making sure we are using a data file there.
    assert os.path.isfile(airflow_db)

# this fixture initializes the Airflow DB once per session
# it is used by DAGs in both the blogs and workflows directories
@pytest.fixture(scope="session")
def airflow_database():
    import airflow.utils.db

    # We use separate directory for local db path per session
    # by setting AIRFLOW_HOME env var, which is done in noxfile_config.py.

    assert 'AIRFLOW_HOME' in os.environ

    airflow_home = os.environ["AIRFLOW_HOME"]
    airflow_db = f"{airflow_home}/airflow.db"

    # reset both resets and initializes a new database
    airflow.utils.db.resetdb()

    # Making sure we are using a data file there.
    assert os.path.isfile(airflow_db)
