# Copyright 2017 Google Inc. All rights reserved.
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

"""Creates the backend Environment."""


def GenerateConfig(context):
    """Creates backend properties to configure environment."""

    region = context.properties['region']
    cf_bucket = context.properties['cfbucket']
    organization_id = context.properties['organization_id']
    scc_api_key = context.properties['scc_api_key']
    audit_logs_source_id = context.properties['audit_logs_source_id']
    binary_authorization_source_id = context.properties['binary_authorization_source_id']
    project_id = context.env['project']
    gce_types_filters = ["gce_instance", "gce_disk", "gce_node_group",
                         "gce_node_template", "gce_target_pool",
                         "gce_autoscaler", "gce_backend_service",
                         "gce_backend_bucket", "gce_client_ssl_policy",
                         "gce_commitment", "gce_license", "gce_health_check",
                         "gce_url_map", "gce_project", "gce_snapshot",
                         "gce_ssl_certificate", "gce_image",
                         "gce_instance_group", "gce_instance_group_manager",
                         "gce_instance_template", "gce_operation"]
    network_types_filters = ["gce_subnetwork", "gce_firewall_rule",
                             "gce_forwarding_rule", "gce_network", "gce_route",
                             "gce_reserved_address", "gce_target_http_proxy",
                             "gce_target_https_proxy", "gce_target_ssl_proxy",
                             "gce_router", "vpn_gateway", "dns_managed_zone",
                             "network_security_policy"]
    sink_iam_filter = 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND protoPayload.methodName=SetIamPolicy'
    sink_network_filter = 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type=({})'.format(' OR '.join(network_types_filters))
    sink_gce_filter = 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type=({})'.format(' OR '.join(gce_types_filters))
    sink_gcs_filter = 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type="gcs_bucket"'
    sink_binauthz_filter = 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type="k8s_cluster" AND protoPayload.methodName="io.k8s.core.v1.pods.create" AND (protoPayload.response.code=403 OR protoPayload.request.metadata.annotations."alpha.image-policy.k8s.io/break-glass"="true" OR labels."imagepolicywebhook.image-policy.k8s.io/break-glass"="true")'

    single_sinks = {
        'sink_network_single': sink_network_filter,
        'sink_gce_single': sink_gce_filter,
        'sink_gcs_single': sink_gcs_filter,
        'sink_binauthz_single': sink_binauthz_filter
    }

    aggregated_sinks = {
        'sink_iam_aggregated': sink_iam_filter
    }

    topic_single = 'log_sink_single'
    topic_single_findings = 'topic_single_findings'
    subscription_single_findings = 'subscription_single_findings'

    topic_aggregated = 'log_sink_aggregated'
    subscription_aggregated_logs = 'subscription_aggregated_logs'
    topic_aggregated_findings = 'topic_aggregated_findings'
    subscription_aggregated_findings = 'subscription_aggregated_findings'

    topic_findings_to_save = 'findings_to_save'

    resources = [{
        'name': topic_single,
        'type': 'pubsub_topic.py'
    }, {
        'name': topic_single_findings,
        'type': 'pubsub_topic.py'
    }, {
        'name': topic_aggregated,
        'type': 'pubsub_topic.py'
    }, {
        'name': topic_aggregated_findings,
        'type': 'pubsub_topic.py'
    }, {
        'name': topic_findings_to_save,
        'type': 'pubsub_topic.py'
    }, {
        'name': 'log-single-converter',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': topic_single,
            'function_name': 'log-single-converter',
            'entryPoint': 'convert',
            'bucket': cf_bucket
        }
    }, {
        'name': 'finding-scc-writer',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': topic_findings_to_save,
            'function_name': 'finding-scc-writer',
            'entryPoint': 'sendFinding',
            'bucket': cf_bucket,
            'organization_id': organization_id,
            'scc_api_key': scc_api_key,
            'audit_logs_source_id': audit_logs_source_id,
            'binary_authorization_source_id': binary_authorization_source_id
        }
    }, {
        'name': subscription_single_findings,
        'type': 'pubsub.v1.subscription',
        'metadata': {
            'dependsOn': [topic_single_findings]
        },
        'properties': {
            'subscription': subscription_single_findings,
            'topic': 'projects/{}/topics/{}'.format(project_id, topic_single_findings),
            'ackDeadlineSeconds': 300
        }
    }, {
        'name': subscription_aggregated_findings,
        'type': 'pubsub.v1.subscription',
        'metadata': {
            'dependsOn': [topic_aggregated_findings]
        },
        'properties': {
            'subscription': subscription_aggregated_findings,
            'topic': 'projects/{}/topics/{}'.format(project_id, topic_aggregated_findings),
            'ackDeadlineSeconds': 300
        }
    }, {
        'name': subscription_aggregated_logs,
        'type': 'pubsub.v1.subscription',
        'metadata': {
            'dependsOn': [topic_aggregated]
        },
        'properties': {
            'subscription': subscription_aggregated_logs,
            'topic': 'projects/{}/topics/{}'.format(project_id, topic_aggregated),
            'ackDeadlineSeconds': 300
        }
    }]

    for sink, _filter in single_sinks.items():
        resources.append({
            'name': sink,
            'type': 'logging_sink.py',
            'properties': {
                'organization_id': organization_id,
                'sink_name': sink,
                'filter': _filter,
                'destination': 'pubsub.googleapis.com/projects/{}/topics/{}'.format(project_id, topic_single)
            }
        })

    for sink, _filter in aggregated_sinks.items():
        resources.append({
            'name': sink,
            'type': 'logging_sink.py',
            'properties': {
                'organization_id': organization_id,
                'sink_name': sink,
                'filter': _filter,
                'destination': 'pubsub.googleapis.com/projects/{}/topics/{}'.format(project_id, topic_aggregated)
            }
        })

    return {'resources': resources}
