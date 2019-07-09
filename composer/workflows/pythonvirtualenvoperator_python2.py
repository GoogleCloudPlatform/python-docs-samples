# Copyright 2018 Google LLC
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

# [START composer_pythonvirtualenvoperator_python2]
import datetime

from airflow import models
from airflow.operators import python_operator


def python2_function():
    """A function which has not been converted to Python 3."""
    # Use the global variable virtualenv_string_args to pass in values when the
    # Python version differs from that used by the Airflow process.
    global virtualenv_string_args

    # Imports must happen within the function when run with the
    # PythonVirtualenvOperator.
    import cStringIO
    import logging

    arg0 = virtualenv_string_args[0]
    buffer = cStringIO.StringIO()
    buffer.write('Wrote an ASCII string to buffer:\n')
    buffer.write(arg0)
    logging.info(buffer.getvalue())


yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())


default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
}

with models.DAG(
        'composer_sample_pythonvirtualenvoperator_python2',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    # Use the PythonVirtualenvOperator to select an explicit python_version.
    run_python2 = python_operator.PythonVirtualenvOperator(
        task_id='run_python2',
        python_callable=python2_function,
        python_version='2',
        string_args=['An example input string'],
    )
# [END composer_pythonvirtualenvoperator_python2]
