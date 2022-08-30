# Copyright 2022 Google LLC
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


"""Example Airflow DAG that sends an email message through SendGrid.

You must configure email notifications so that Airflow sends email through
SendGrid. For more information, see
https://cloud.google.com/composer/docs/composer-2/configure-email#sendgrid

"""

# [START composer_email_operator_sendgrid]

import datetime

import airflow
from airflow.operators.email import EmailOperator


with airflow.DAG(
    "composer_sample_sendgrid",
    start_date=datetime.datetime(2022, 1, 1),
) as dag:

    task_email = EmailOperator(
        task_id="send-email",
        conn_id="sendgrid_default",
        # You can specify more than one recipient with a list.
        to="user@example.com",
        subject="EmailOperator test for SendGrid",
        html_content="This is a test message sent through SendGrid.",
        dag=dag,
    )

# [END composer_email_operator_sendgrid]
