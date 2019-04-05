'use strict';
function createBigQueryJson() {
    return {
        "insertId": "-hr89esd36d9",
        "logName": "projects/gce-logging-audit/logs/cloudaudit.googleapis.com%2Factivity",
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "tribeiro@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "bigquery.datasets.create",
                    "resource": "projects/gce-logging-audit"
                }
            ],
            "methodName": "datasetservice.insert",
            "requestMetadata": {
                "callerIp": "201.48.150.197",
                "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36,gzip(gfe)"
            },
            "resourceLocation": {
                "currentLocations": [
                    "US"
                ]
            },
            "resourceName": "projects/gce-logging-audit/datasets",
            "serviceData": {
                "@type": "type.googleapis.com/google.cloud.bigquery.logging.v1.AuditData",
                "datasetInsertRequest": {
                    "resource": {
                    "acl": {},
                    "datasetName": {
                        "datasetId": "log_test",
                        "projectId": "gce-logging-audit"
                    },
                    "info": {}
                    }
                },
                "datasetInsertResponse": {
                    "resource": {
                        "acl": {
                            "entries": [
                                {
                                    "role": "WRITER",
                                    "specialGroup": "PROJECT_WRITERS",
                                    "viewName": {}
                                },
                                {
                                    "role": "OWNER",
                                    "specialGroup": "PROJECT_OWNERS",
                                    "viewName": {}
                                },
                                {
                                    "role": "OWNER",
                                    "specialGroup": "PROJECT_OWNERS",
                                    "userEmail": "tribeiro@clsecteam.com",
                                    "viewName": {}
                                },
                                {
                                    "role": "READER",
                                    "specialGroup": "PROJECT_READERS",
                                    "viewName": {}
                                }
                            ]
                        },
                        "createTime": "2018-09-12T18:55:36.439Z",
                        "datasetName": {
                            "datasetId": "log_test",
                            "projectId": "gce-logging-audit"
                        },
                        "info": {},
                        "updateTime": "2018-09-12T18:55:36.439Z"
                    }
                }
            },
            "serviceName": "bigquery.googleapis.com",
            "status": {}
        },
        "receiveTimestamp": "2018-09-12T18:55:37.479627103Z",
        "resource": {
            "labels": {
                "project_id": "gce-logging-audit"
            },
            "type": "bigquery_resource"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-12T18:55:36.507Z"
    }
};

function createSpannerJson() {
    return {
        "insertId": "12uncdwa6",
        "logName": "projects/gce-logging-audit/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
            "first": true,
            "id": "projects/gce-logging-audit/instances/test-spanner/operations/5e6f76628f83a262",
            "producer": "spanner.googleapis.com"
        },
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "tribeiro@clsecteam.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "spanner.instances.create",
                    "resource": "projects/gce-logging-audit",
                    "resourceAttributes": {
                        "name": "projects/gce-logging-audit/instances/test-spanner",
                        "service": "spanner",
                        "type": "spanner.instances"
                    }
                }
            ],
            "methodName": "google.spanner.admin.instance.v1.InstanceAdmin.CreateInstance",
            "request": {
                "@type": "type.googleapis.com/google.spanner.admin.instance.v1.CreateInstanceRequest",
                "instance": {
                    "config": "projects/gce-logging-audit/instanceConfigs/regional-asia-east1",
                    "displayName": "Test",
                    "nodeCount": 1
                },
                "instanceId": "test-spanner"
            },
            "requestMetadata": {
                "callerIp": "201.48.150.197",
                "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36,gzip(gfe)"
            },
            "resourceName": "projects/gce-logging-audit/instances/test-spanner",
            "serviceName": "spanner.googleapis.com"
        },
        "receiveTimestamp": "2018-09-12T18:41:25.645217530Z",
        "resource": {
            "labels": {
                "instance_config": "",
                "instance_id": "test-spanner",
                "location": "",
                "project_id": "gce-logging-audit"
            },
            "type": "spanner_instance"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-12T18:41:24.411089344Z"
    }
}

module.exports.createBigQueryJson = createBigQueryJson;
module.exports.createSpannerJson = createSpannerJson;