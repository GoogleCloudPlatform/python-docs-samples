# Copyright 2018 Google LLC
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

# [START gae_python37_bigquery]
from flask import Flask, render_template
from google.cloud import bigquery

app = Flask(__name__)
bigquery_client = bigquery.Client()


@app.route('/')
def main():
    query_job = bigquery_client.query("""
        SELECT
        CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
        view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10
    """)

    results = query_job.result()
    return render_template('query_result.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
# [END gae_python37_bigquery]
