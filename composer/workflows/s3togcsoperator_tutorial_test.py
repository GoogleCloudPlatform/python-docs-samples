# Copyright 2022 Google LLC
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

import internal_unit_testing


def test_dag_import():
    """Test that the DAG file can be successfully imported.
<<<<<<< HEAD
    
=======

>>>>>>> 803b71b37 (fixed style and format problems according to Leah and Dan)
    This tests that the DAG can be parsed, but does not run it in an Airflow
    environment. This is a recommended confidence check by the official Airflow
    docs: https://airflow.incubator.apache.org/tutorial.html#testing
    """

<<<<<<< HEAD
    import s3togcsoperator_tutorial
=======
    from . import s3togcsoperator_tutorial
>>>>>>> 803b71b37 (fixed style and format problems according to Leah and Dan)

    internal_unit_testing.assert_has_valid_dag(s3togcsoperator_tutorial)
