#!/usr/bin/env python

# Copyright 2022 Google LLC
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

# [START privateca_monitor_ca_expiry]
import google.cloud.monitoring_v3 as monitoring_v3


def create_ca_monitor_policy(project_id: str) -> None:
    """
    Create a monitoring policy that notifies you 30 days before a managed CA expires.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
    """

    alertPolicyServiceClient = monitoring_v3.AlertPolicyServiceClient()
    notificationChannelServiceClient = monitoring_v3.NotificationChannelServiceClient()

    # Query which indicates the resource to monitor and the constraints.
    # Here, the alert policy notifies you 30 days before a managed CA expires.
    # For more information on creating queries, see: https://cloud.google.com/monitoring/mql/alerts
    query = (
        "fetch privateca.googleapis.com/CertificateAuthority"
        "| metric 'privateca.googleapis.com/ca/cert_chain_expiration'"
        "| group_by 5m,"
        "[value_cert_chain_expiration_mean: mean(value.cert_chain_expiration)]"
        "| every 5m"
        "| condition val() < 2.592e+06 's'"
    )

    # Create a notification channel.
    notification_channel = monitoring_v3.NotificationChannel(
        type_="email",
        labels={"email_address": "python-docs-samples-testing@google.com"},
    )
    channel = notificationChannelServiceClient.create_notification_channel(
        name=notificationChannelServiceClient.common_project_path(project_id),
        notification_channel=notification_channel,
    )

    # Set the query and notification channel.
    alert_policy = monitoring_v3.AlertPolicy(
        display_name="policy-name",
        conditions=[
            monitoring_v3.AlertPolicy.Condition(
                display_name="ca-cert-chain-expiration",
                condition_monitoring_query_language=monitoring_v3.AlertPolicy.Condition.MonitoringQueryLanguageCondition(
                    query=query,
                ),
            )
        ],
        combiner=monitoring_v3.AlertPolicy.ConditionCombinerType.AND,
        notification_channels=[channel.name],
    )

    policy = alertPolicyServiceClient.create_alert_policy(
        name=notificationChannelServiceClient.common_project_path(project_id),
        alert_policy=alert_policy,
    )

    print("Monitoring policy successfully created!", policy.name)


# [END privateca_monitor_ca_expiry]
