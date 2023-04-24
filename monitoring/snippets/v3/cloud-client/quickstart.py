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


def run_quickstart(project=""):
    # [START monitoring_quickstart]
    from google.cloud import monitoring_v3

    import time

    client = monitoring_v3.MetricServiceClient()
    # project = 'my-project'  # TODO: Update to your project ID.
    project_name = f"projects/{project}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/my_metric"
    series.metric.labels["store_id"] = "Pittsburgh"
    series.resource.type = "gce_instance"
    series.resource.labels["instance_id"] = "1234567890123456789"
    series.resource.labels["zone"] = "us-central1-f"
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    point = monitoring_v3.Point({"interval": interval, "value": {"double_value": 3.14}})
    series.points = [point]
    client.create_time_series(request={"name": project_name, "time_series": [series]})
    print("Successfully wrote time series.")
    # [END monitoring_quickstart]


if __name__ == "__main__":
    run_quickstart()
