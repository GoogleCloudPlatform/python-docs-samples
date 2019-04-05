'use strict';
function createBucket() {
    return {
        "insertId": "-kso07befzst0",
        "logName": "projects/noti-201808221442-a/logs/cloudaudit.googleapis.com%2Factivity",
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "dandrade@ciandt.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "storage.buckets.create",
                    "resource": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                    "resourceAttributes": {}
                }
            ],
            "methodName": "storage.buckets.create",
            "request": {
                "defaultObjectAcl": {
                    "@type": "type.googleapis.com/google.iam.v1.Policy",
                    "bindings": [
                        {
                            "members": [
                                "projectOwner:noti-201808221442-a",
                                "projectEditor:noti-201808221442-a"
                            ],
                            "role": "roles/storage.legacyObjectOwner"
                        },
                        {
                            "members": [
                                "projectViewer:noti-201808221442-a"
                            ],
                            "role": "roles/storage.legacyObjectReader"
                        }
                    ]
                }
            },
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36,gzip(gfe)",
                "destinationAttributes": {},
                "requestAttributes": {}
            },
            "resourceName": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
            "serviceData": {
                "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
                "policyDelta": {
                    "bindingDeltas": [
                        {
                            "action": "ADD",
                            "member": "projectOwner:noti-201808221442-a",
                            "role": "roles/storage.legacyBucketOwner"
                        },
                        {
                            "action": "ADD",
                            "member": "projectEditor:noti-201808221442-a",
                            "role": "roles/storage.legacyBucketOwner"
                        },
                        {
                            "action": "ADD",
                            "member": "projectViewer:noti-201808221442-a",
                            "role": "roles/storage.legacyBucketReader"
                        }
                    ]
                }
            },
            "serviceName": "storage.googleapis.com",
            "status": {}
        },
        "receiveTimestamp": "2018-09-05T19:40:27.073258630Z",
        "resource": {
            "labels": {
                "bucket_name": "n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                "location": "US-CENTRAL1",
                "project_id": "noti-201808221442-a"
            },
            "type": "gcs_bucket"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-05T19:40:26.201Z"
    }
}

function deleteBucket() {
    return {
        "insertId": "-bxdo97egtutc",
        "logName": "projects/noti-201808221442-a/logs/cloudaudit.googleapis.com%2Factivity",
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "dandrade@ciandt.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "storage.buckets.delete",
                    "resource": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                    "resourceAttributes": {}
                },
                {
                    "granted": true,
                    "permission": "storage.buckets.getIamPolicy",
                    "resource": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                    "resourceAttributes": {}
                }
            ],
            "methodName": "storage.buckets.delete",
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36,gzip(gfe)",
                "destinationAttributes": {},
                "requestAttributes": {}
            },
            "resourceName": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
            "serviceName": "storage.googleapis.com",
            "status": {}
        },
        "receiveTimestamp": "2018-09-05T19:45:16.649725867Z",
        "resource": {
            "labels": {
                "bucket_name": "n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                "location": "US-CENTRAL1",
                "project_id": "noti-201808221442-a"
            },
            "type": "gcs_bucket"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-05T19:45:16.090Z"
    }
}


function setIamPermissions() {
    return {
        "insertId": "u60vqeg4wcc",
        "logName": "projects/noti-201808221442-a/logs/cloudaudit.googleapis.com%2Factivity",
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "dandrade@ciandt.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "storage.buckets.setIamPolicy",
                    "resource": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                    "resourceAttributes": {}
                }
            ],
            "methodName": "storage.setIamPermissions",
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36,gzip(gfe)",
                "destinationAttributes": {},
                "requestAttributes": {}
            },
            "resourceName": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
            "serviceData": {
                "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
                "policyDelta": {
                    "bindingDeltas": [
                        {
                            "action": "ADD",
                            "member": "user:dandrade@ciandt.com",
                            "role": "roles/storage.objectViewer"
                        }
                    ]
                }
            },
            "serviceName": "storage.googleapis.com",
            "status": {}
        },
        "receiveTimestamp": "2018-09-05T19:41:09.236028827Z",
        "resource": {
            "labels": {
                "bucket_name": "n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                "location": "US-CENTRAL1",
                "project_id": "noti-201808221442-a"
            },
            "type": "gcs_bucket"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-05T19:41:08.205Z"
    }
};

function updateBucket() {
    return {
        "insertId": "-wqn6mteg5upq",
        "logName": "projects/noti-201808221442-a/logs/cloudaudit.googleapis.com%2Factivity",
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "dandrade@ciandt.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "storage.objects.update",
                    "resource": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5/objects/set_iam_policy.json",
                    "resourceAttributes": {}
                },
                {
                    "granted": true,
                    "permission": "storage.objects.setIamPolicy",
                    "resource": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5/objects/set_iam_policy.json",
                    "resourceAttributes": {}
                },
                {
                    "granted": true,
                    "permission": "storage.objects.getIamPolicy",
                    "resource": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5/objects/set_iam_policy.json",
                    "resourceAttributes": {}
                }
            ],
            "methodName": "storage.objects.update",
            "requestMetadata": {
                "callerIp": "177.185.2.139",
                "callerSuppliedUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36,gzip(gfe)",
                "destinationAttributes": {},
                "requestAttributes": {}
            },
            "resourceName": "projects/_/buckets/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5/objects/set_iam_policy.json",
            "serviceData": {
                "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
                "policyDelta": {
                    "bindingDeltas": [
                        {
                            "action": "REMOVE",
                            "member": "projectEditor:noti-201808221442-a",
                            "role": "roles/storage.legacyObjectReader"
                        },
                        {
                            "action": "ADD",
                            "member": "projectEditor:noti-201808221442-a",
                            "role": "roles/storage.legacyObjectOwner"
                        }
                    ]
                }
            },
            "serviceName": "storage.googleapis.com",
            "status": {}
        },
        "receiveTimestamp": "2018-09-05T19:44:57.199406146Z",
        "resource": {
            "labels": {
                "bucket_name": "n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5",
                "location": "US-CENTRAL1",
                "project_id": "noti-201808221442-a"
            },
            "type": "gcs_bucket"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-05T19:44:56.669Z"
    }
};

module.exports.deleteBucket = deleteBucket;
module.exports.createBucket = createBucket;
module.exports.updateBucket = updateBucket;
module.exports.setIamPermissions = setIamPermissions;