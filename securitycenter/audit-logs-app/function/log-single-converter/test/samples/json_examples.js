'use strict';
function set_iam_policy_json() {
    return {
        "insertId": "-8l5j1zc1ia",
        "logName": "organizations/0000000000000/logs/cloudaudit.googleapis.com%2Factivity",
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "authenticationInfo": {
                "principalEmail": "johndoe@example.com"
            },
            "authorizationInfo": [
                {
                    "granted": true,
                    "permission": "resourcemanager.organizations.setIamPolicy",
                    "resource": "organizations/0000000000000"
                }
            ],
            "methodName": "SetIamPolicy",
            "request": {
                "@type": "type.googleapis.com/google.iam.v1.SetIamPolicyRequest",
                "policy": {
                    "bindings": [
                        {
                            "members": [
                                "user:johndoe@example.com"
                            ],
                            "role": "organizations/0000000000000/roles/custom.gaeAppCreator"
                        },
                        {
                            "members": [
                                "group:admin@example.com",
                            ],
                            "role": "roles/appengine.appAdmin"
                        }
                    ],
                    "etag": "BwV1D0Xh12s="
                },
                "resource": "organizations/0000000000000"
            },
            "requestMetadata": {
                "callerIp": "104.196.5.17",
                "callerSuppliedUserAgent": "google-cloud-sdk x_Tw5K8nnjoRAqULM9PFAC2b gcloud/214.0.0 command/gcloud.organizations.add-iam-policy-binding invocation-id/c14f0e0eb1884111ba565eb2f731a94a environment/devshell environment-version/None interactive/False from-script/True python/2.7.13 (Linux 4.14.33+),gzip(gfe)"
            },
            "resourceName": "organizations/0000000000000",
            "response": {
                "@type": "type.googleapis.com/google.iam.v1.Policy",
                "bindings": [
                    {
                        "members": [
                            "user:johndoe@example.com"
                        ],
                        "role": "organizations/0000000000000/roles/custom.gaeAppCreator"
                    },
                    {
                        "members": [
                            "group:admin@example.com",
                        ],
                        "role": "roles/appengine.appAdmin"
                    },
                    {
                        "members": [
                            "serviceAccount:forseti@example.iam.gserviceaccount.com",
                        ],
                        "role": "roles/compute.securityAdmin"
                    }
                ],
                "etag": "BwV1D0YhdTM="
            },
            "serviceData": {
                "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
                "policyDelta": {
                    "bindingDeltas": [
                        {
                            "action": "ADD",
                            "member": "serviceAccount:forseti@example.iam.gserviceaccount.com",
                            "role": "roles/compute.securityAdmin"
                        }
                    ]
                }
            },
            "serviceName": "cloudresourcemanager.googleapis.com",
            "status": {}
        },
        "receiveTimestamp": "2018-09-04T17:49:06.124104262Z",
        "resource": {
            "labels": {
                "organization_id": "0000000000000"
            },
            "type": "organization"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-04T17:49:04.584Z"
    }
};

module.exports.set_iam_policy_json = set_iam_policy_json;