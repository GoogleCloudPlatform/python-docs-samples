'use strict';
function createNetworkJson() {
    return {
        "insertId": "-xk3cz0dizzg",
        "logName": "projects/scc-log-pubsub/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
            "first": true,
            "id": "operation-1536173292885-57524376f940a-5cf2620d-f040eba8",
            "producer": "type.googleapis.com"
        },
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "lucasbr@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "compute.networks.create",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/global/networks/scc-log-network",
                        "service": "compute",
                        "type": "compute.networks"
                    }
                }
            ],
            "methodName": "v1.compute.networks.insert",
            "request": {
                "@type": "type.googleapis.com/compute.networks.insert",
                "autoCreateSubnetworks": true,
                "name": "scc-log-network",
                "routingConfig": {
                    "routingMode": "REGIONAL"
                }
            },
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "google-cloud-sdk gcloud/210.0.0 command/gcloud.compute.networks.create invocation-id/50c18b0082f84ecda313c3f4ee8361b6 environment/None environment-version/None interactive/True from-script/False python/2.7.12 (Linux 4.8.0-41-generic),gzip(gfe)"
            },
            "resourceLocation": {
                "currentLocations": [
                    "global"
                ]
            },
            "resourceName": "projects/scc-log-pubsub/global/networks/scc-log-network",
            "response": {
                "@type": "type.googleapis.com/operation",
                "id": "3788639165692615169",
                "insertTime": "2018-09-05T11:48:14.095-07:00",
                "name": "operation-1536173292885-57524376f940a-5cf2620d-f040eba8",
                "operationType": "insert",
                "progress": "0",
                "selfLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/operations/operation-1536173292885-57524376f940a-5cf2620d-f040eba8",
                "status": "PENDING",
                "targetId": "7505145839472187905",
                "targetLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/networks/scc-log-network",
                "user": "lucasbr@clsecteam.com"
            },
            "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-05T18:48:14.93451508Z",
        "resource": {
            "labels": {
                "network_id": "7505145839472187905",
                "project_id": "scc-log-pubsub"
            },
            "type": "gce_network"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-05T18:48:12.93Z"
    }
};


function deleteNetworkJson() {
    return {
        "insertId": "-cqydtcdqqqy",
        "logName": "projects/scc-log-pubsub/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
            "first": true,
            "id": "operation-1536175282906-57524ae0ce390-5ed314fd-5160f3f4",
            "producer": "type.googleapis.com"
        },
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "lucasbr@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "compute.networks.delete",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/global/networks/scc-log-network",
                        "service": "compute",
                        "type": "compute.networks"
                    }
                }
            ],
            "methodName": "v1.compute.networks.delete",
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "google-cloud-sdk gcloud/210.0.0 command/gcloud.compute.networks.delete invocation-id/a96047e9b2c2437b814bc6d05a863d5c environment/None environment-version/None interactive/True from-script/False python/2.7.12 (Linux 4.8.0-41-generic),gzip(gfe)"
            },
            "resourceLocation": {
                "currentLocations": [
                    "global"
                ]
            },
            "resourceName": "projects/scc-log-pubsub/global/networks/scc-log-network",
            "response": {
                "@type": "type.googleapis.com/operation",
                "id": "1055501396482036316",
                "insertTime": "2018-09-05T12:21:23.263-07:00",
                "name": "operation-1536175282906-57524ae0ce390-5ed314fd-5160f3f4",
                "operationType": "delete",
                "progress": "0",
                "selfLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/operations/operation-1536175282906-57524ae0ce390-5ed314fd-5160f3f4",
                "status": "PENDING",
                "targetId": "7505145839472187905",
                "targetLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/networks/scc-log-network",
                "user": "lucasbr@clsecteam.com"
            },
            "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-05T19:21:24.325767573Z",
        "resource": {
            "labels": {
                "network_id": "7505145839472187905",
                "project_id": "scc-log-pubsub"
            },
            "type": "gce_network"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-05T19:21:23.003Z"
    }
};

function createSubnetworkJson() {
    return {
        "insertId": "b3nu9bd2jr6",
        "logName": "projects/scc-log-pubsub/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
            "first": true,
            "id": "operation-1536243126580-5753479d93324-1b3fad86-181cd00f",
            "producer": "type.googleapis.com"
        },
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "lucasbr@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "compute.subnetworks.create",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01",
                        "service": "compute",
                        "type": "compute.subnetworks"
                    }
                },
                {
                    "granted": true,
                    "permission": "compute.networks.updatePolicy",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/global/networks/scc-network-01",
                        "service": "compute",
                        "type": "compute.networks"
                    }
                }
            ],
            "methodName": "v1.compute.subnetworks.insert",
            "request": {
                "@type": "type.googleapis.com/compute.subnetworks.insert",
                "ipCidrRange": "10.1.0.0/19",
                "name": "scc-subnetwork-01",
                "network": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/networks/scc-network-01",
                "privateIpGoogleAccess": false
            },
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "google-cloud-sdk gcloud/210.0.0 command/gcloud.compute.networks.subnets.create invocation-id/8c8bf7d978574872b0b9c93a1776dc88 environment/None environment-version/None interactive/True from-script/False python/2.7.12 (Linux 4.8.0-41-generic),gzip(gfe)"
            },
            "resourceLocation": {
                "currentLocations": [
                    "us-central1"
                ]
            },
            "resourceName": "projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01",
            "response": {
                "@type": "type.googleapis.com/operation",
                "id": "8384201181106047832",
                "insertTime": "2018-09-06T07:12:07.596-07:00",
                "name": "operation-1536243126580-5753479d93324-1b3fad86-181cd00f",
                "operationType": "insert",
                "progress": "0",
                "region": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/regions/us-central1",
                "selfLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/regions/us-central1/operations/operation-1536243126580-5753479d93324-1b3fad86-181cd00f",
                "status": "PENDING",
                "targetId": "6718876411500464984",
                "targetLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01",
                "user": "lucasbr@clsecteam.com"
            },
            "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-06T14:12:08.329961971Z",
        "resource": {
            "labels": {
                "location": "us-central1",
                "project_id": "scc-log-pubsub",
                "subnetwork_id": "6718876411500464984",
                "subnetwork_name": "scc-subnetwork-01"
            },
            "type": "gce_subnetwork"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-06T14:12:06.663Z"
    }
};

function deleteSubnetworkJson() {
    return {
        "insertId": "3c5prxcxki",
        "logName": "projects/scc-log-pubsub/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
            "first": true,
            "id": "operation-1536244633454-57534d3aa45b3-ca3bda91-f17355ed",
            "producer": "type.googleapis.com"
        },
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "lucasbr@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "compute.subnetworks.delete",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01",
                        "service": "compute",
                        "type": "compute.subnetworks"
                    }
                }
            ],
            "methodName": "beta.compute.subnetworks.delete",
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "google-cloud-sdk gcloud/210.0.0 command/gcloud.beta.compute.networks.subnets.delete invocation-id/39224248ecd746a9b3a7ceae5319e994 environment/None environment-version/None interactive/True from-script/False python/2.7.12 (Linux 4.8.0-41-generic),gzip(gfe)"
            },
            "resourceLocation": {
                "currentLocations": [
                    "us-central1"
                ]
            },
            "resourceName": "projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01",
            "response": {
                "@type": "type.googleapis.com/operation",
                "id": "3478238490481427830",
                "insertTime": "2018-09-06T07:37:14.039-07:00",
                "name": "operation-1536244633454-57534d3aa45b3-ca3bda91-f17355ed",
                "operationType": "delete",
                "progress": "0",
                "region": "https://www.googleapis.com/compute/beta/projects/scc-log-pubsub/regions/us-central1",
                "selfLink": "https://www.googleapis.com/compute/beta/projects/scc-log-pubsub/regions/us-central1/operations/operation-1536244633454-57534d3aa45b3-ca3bda91-f17355ed",
                "status": "PENDING",
                "targetId": "6718876411500464984",
                "targetLink": "https://www.googleapis.com/compute/beta/projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01",
                "user": "lucasbr@clsecteam.com"
            },
            "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-06T14:37:15.078510717Z",
        "resource": {
            "labels": {
                "location": "us-central1",
                "project_id": "scc-log-pubsub",
                "subnetwork_id": "6718876411500464984",
                "subnetwork_name": "scc-subnetwork-01"
            },
            "type": "gce_subnetwork"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-06T14:37:13.501Z"
    }
};

function createFirewallJson() {
    return {
        "insertId": "-v254mddkrwe",
        "logName": "projects/scc-log-pubsub/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
            "first": true,
            "id": "operation-1536243735684-575349e2763a1-12753d9a-f2c49099",
            "producer": "type.googleapis.com"
        },
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "lucasbr@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "compute.firewalls.create",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/global/firewalls/firewall-rule-01",
                        "service": "compute",
                        "type": "compute.firewalls"
                    }
                },
                {
                    "granted": true,
                    "permission": "compute.networks.updatePolicy",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/global/networks/default",
                        "service": "compute",
                        "type": "compute.networks"
                    }
                }
            ],
            "methodName": "v1.compute.firewalls.insert",
            "request": {
                "@type": "type.googleapis.com/compute.firewalls.insert",
                "alloweds": [
                    {
                        "IPProtocol": "tcp",
                        "ports": [
                            "80"
                        ]
                    },
                    {
                        "IPProtocol": "icmp"
                    }
                ],
                "direction": "INGRESS",
                "name": "firewall-rule-01",
                "network": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/networks/default"
            },
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "google-cloud-sdk gcloud/210.0.0 command/gcloud.compute.firewall-rules.create invocation-id/323f696f7f7140dbafe7dca8e5ee6678 environment/None environment-version/None interactive/True from-script/False python/2.7.12 (Linux 4.8.0-41-generic),gzip(gfe)"
            },
            "resourceLocation": {
                "currentLocations": [
                    "global"
                ]
            },
            "resourceName": "projects/scc-log-pubsub/global/firewalls/firewall-rule-01",
            "response": {
                "@type": "type.googleapis.com/operation",
                "id": "6391730053939234551",
                "insertTime": "2018-09-06T07:22:16.474-07:00",
                "name": "operation-1536243735684-575349e2763a1-12753d9a-f2c49099",
                "operationType": "insert",
                "progress": "0",
                "selfLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/operations/operation-1536243735684-575349e2763a1-12753d9a-f2c49099",
                "status": "PENDING",
                "targetId": "5133249119463966455",
                "targetLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/firewalls/firewall-rule-01",
                "user": "lucasbr@clsecteam.com"
            },
            "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-06T14:22:17.093074323Z",
        "resource": {
            "labels": {
                "firewall_rule_id": "5133249119463966455",
                "project_id": "scc-log-pubsub"
            },
            "type": "gce_firewall_rule"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-06T14:22:15.73Z"
    }
};

function deleteFirewallJson() {
    return {
        "insertId": "-mqyvccdqc10",
        "logName": "projects/scc-log-pubsub/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
            "first": true,
            "id": "operation-1536244143243-57534b6723ef8-aed03176-10620b2c",
            "producer": "type.googleapis.com"
        },
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "lucasbr@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "compute.firewalls.delete",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/global/firewalls/firewall-rule-01",
                        "service": "compute",
                        "type": "compute.firewalls"
                    }
                },
                {
                    "granted": true,
                    "permission": "compute.networks.updatePolicy",
                    "resourceAttributes": {
                        "name": "projects/scc-log-pubsub/global/networks/default",
                        "service": "compute",
                        "type": "compute.networks"
                    }
                }
            ],
            "methodName": "v1.compute.firewalls.delete",
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "google-cloud-sdk gcloud/210.0.0 command/gcloud.compute.firewall-rules.delete invocation-id/ca89c796d71d4142b99b45b21231b5e9 environment/None environment-version/None interactive/True from-script/False python/2.7.12 (Linux 4.8.0-41-generic),gzip(gfe)"
            },
            "resourceLocation": {
                "currentLocations": [
                    "global"
                ]
            },
            "resourceName": "projects/scc-log-pubsub/global/firewalls/firewall-rule-01",
            "response": {
                "@type": "type.googleapis.com/operation",
                "id": "7385586590040229696",
                "insertTime": "2018-09-06T07:29:03.475-07:00",
                "name": "operation-1536244143243-57534b6723ef8-aed03176-10620b2c",
                "operationType": "delete",
                "progress": "0",
                "selfLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/operations/operation-1536244143243-57534b6723ef8-aed03176-10620b2c",
                "status": "PENDING",
                "targetId": "5133249119463966455",
                "targetLink": "https://www.googleapis.com/compute/v1/projects/scc-log-pubsub/global/firewalls/firewall-rule-01",
                "user": "lucasbr@clsecteam.com"
            },
            "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-06T14:29:03.762223842Z",
        "resource": {
            "labels": {
                "firewall_rule_id": "5133249119463966455",
                "project_id": "scc-log-pubsub"
            },
            "type": "gce_firewall_rule"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-06T14:29:03.316Z"
    }
};

module.exports.createNetworkJson = createNetworkJson;
module.exports.deleteNetworkJson = deleteNetworkJson;
module.exports.createSubnetworkJson = createSubnetworkJson;
module.exports.deleteSubnetworkJson = deleteSubnetworkJson;
module.exports.createFirewallJson = createFirewallJson;
module.exports.deleteFirewallJson = deleteFirewallJson;