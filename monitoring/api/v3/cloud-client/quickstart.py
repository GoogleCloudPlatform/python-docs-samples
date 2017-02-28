# Copyright 2017 Google Inc.
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


def run_quickstart():
    # [START monitoring_quickstart]
    from google.cloud import monitoring

    client = monitoring.Client()

    resource = client.resource(
        type_='gce_instance',
        labels={
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-f',
        }
    )

    metric = client.metric(
        type_='custom.googleapis.com/my_metric',
        labels={}
    )

    # Default arguments use endtime datetime.utcnow()
    client.write_point(metric, resource, 3.14)
    print('Successfully wrote time series.')
    # [END monitoring_quickstart]


if __name__ == '__main__':
    run_quickstart()
