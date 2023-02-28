#!/usr/bin/env python
# Copyright 2021 Google, Inc
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
#
# All Rights Reserved.

# [START recaptcha_enterprise_get_metrics_site_key]
from google.cloud import recaptchaenterprise_v1


def get_metrics(project_id: str, recaptcha_site_key: str) -> None:
    """Get metrics specific to a recaptcha site key.
        E.g: score bucket count for a key or number of
        times the checkbox key failed/ passed etc.,
    Args:
    project_id: Google Cloud Project ID.
    recaptcha_site_key: Specify the site key to get metrics.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    metrics_name = f"projects/{project_id}/keys/{recaptcha_site_key}/metrics"
    request = recaptchaenterprise_v1.GetMetricsRequest()
    request.name = metrics_name

    response = client.get_metrics(request)

    # Retrieve the metrics you want from the key.
    # If the site key is checkbox type: then use response.challenge_metrics
    # instead of response.score_metrics
    for day_metric in response.score_metrics:
        # Each 'day_metric' is in the granularity of one day.
        score_bucket_count = day_metric.overall_metrics.score_buckets
        print(score_bucket_count)

    print(f"Retrieved the bucket count for score based key: {recaptcha_site_key}")


# [END recaptcha_enterprise_get_metrics_site_key]
