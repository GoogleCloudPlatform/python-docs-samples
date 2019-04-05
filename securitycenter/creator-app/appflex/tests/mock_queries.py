from client.scc_client_beta import Asset, Finding


def transform_json_to_asset_list(result_list):
    asset_list = []
    for result in result_list:
        asset = Asset(result['asset'], result['state'])
        asset_list.append(asset)
    return asset_list


def transform_json_to_findings_list(result_list):
    findings_list = []
    for result in result_list:
        finding = Finding(result)
        findings_list.append(finding)
    return findings_list


def mock_two_steps_asset_properties_query():
    results = [
        {
            "asset": {
                "name": "organizations/688851828130/assets/6935692701314546019",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceOwners": [
                        "user:dandrade@gcp-sec-demo-org.joonix.net",
                        "user:lucasbr@gcp-sec-demo-org.joonix.net",
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "name": "asset-dev-project",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "asset-dev-project",
                    "createTime": "2018-02-19t17:02:09.842z",
                    "projectNumber": 138150943629
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/6935692701314546019/securityMarks",
                    "marks": {
                        "scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f": "working_6f04f632-3276-4ff3-b32a-92f794fb0f2f",
                        "scc_query_e4b06e13-2cf7-4372-9c65-ab36039a985d": "true",
                        "new": "1",
                        "environment": "development",
                        "folder": "group1",
                        "test2": "2",
                        "test1": "1",
                        "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                    }
                },
                "createTime": "2018-10-17T22:03:23.376Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/16389676671780941579",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/592766336107",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/592766336107",
                    "resourceOwners": [
                        "user:dandrade@ciandt.com"
                    ]
                },
                "resourceProperties": {
                    "name": "joonix-net-forseti-22",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "joonix-net-forseti-22",
                    "createTime": "2018-08-31t16:08:58.752z",
                    "projectNumber": 592766336107
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/16389676671780941579/securityMarks",
                    "marks": {
                        "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                    }
                },
                "createTime": "2018-09-01T00:34:42.555Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        }
    ]
    return transform_json_to_asset_list(results)


def mock_two_steps_asset_mark_query():
    results = [
        {
            "asset": {
                "name": "organizations/1055058813388/assets/18376495389127139332",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/620146303431",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/1055058813388",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/620146303431",
                    "resourceOwners": [
                        "user:dandrade@ciandt.com"
                    ]
                },
                "resourceProperties": {
                    "name": "gce-audit-logs-216020",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"1055058813388\",\"type\":\"organization\"}",
                    "projectId": "gce-audit-logs-216020",
                    "createTime": "2018-09-10t20:41:27.103z",
                    "projectNumber": 620146303431
                },
                "securityMarks": {
                    "name": "organizations/1055058813388/assets/18376495389127139332/securityMarks",
                    "marks": {
                        "scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f": "working_6f04f632-3276-4ff3-b32a-92f794fb0f2f"
                    }
                },
                "createTime": "2018-10-02T20:54:33.270Z",
                "updateTime": "2018-10-23T17:17:03.783Z"
            },
            "state": "UNUSED"
        }
    ]
    return transform_json_to_asset_list(results)


def mock_two_steps_asset_finding():
    results = [
        {
            "name": "organizations/688851828130/sources/16462884240065277753/findings/fyihx3ltua4xcMSigwngXX1EP108LG",
            "parent": "organizations/688851828130/sources/16462884240065277753",
            "resourceName": "//compute.googleapis.com/projects/binary-authorization-demo/global/firewalls/gke-bin-auth-demo-cluster-5dd7583a-all",
            "state": "ACTIVE",
            "category": "3-category-3",
            "externalUri": "9CltdW6OyGxvyusZxCiyaTnkxhI0cBDEdKeyWmmZcp85op7FdN",
            "sourceProperties": {
                "property-13": "property-13-value-06Flzv19yin9e4VKfQBckUBmI0nYJ0WxsKkwm8ZITuf73G24E2kk1wVQ1UwwKF2bGkMtEXcxAq",
                "property-12": "property-12-value-fVYpB0a7Nyt0pI7YS2XcxsAvJNNDkDEyJUfHEFsUIWI8IjgH0eMmnDWbuM5LmWp",
                "property-15": "property-15-value-HWO",
                "property-14": "property-14-value-kSlG9GUTA1tIpXBUW4QjzaMzY58vEml7iU8enMIwGqC8khImQQHvSMMlYxFN",
                "property-9": "property-9-value-e1XlCxaPMBR6OGNWOA1CmJiqMoG9F4Z4M4c8znRUEKM7ikKVZfXQVfZzqdV2jZLFH73Oq4GUO8fsOg74",
                "property-7": "property-7-value-",
                "property-8": "property-8-value-zGcVjW6xcmqcWD052fjUFGz2zdZHH6eoCQC6jXwy7SJKh4wrn52JlAvjxXe0",
                "property-1": "property-1-value-qdrwCF8kQxKeBHL8fATQH0pbVfaNoFslRYhXy8OPmHAbhy6fMtgOSYkFrSk",
                "property-2": "property-2-value-W2qVytwbvtNU6l37FUHOpXy3ehjIpClM",
                "property-11": "property-11-value-dJtY27neNNogPHi2ofmQQSfnb4N3Baz7VeWi57zc9a",
                "property-0": "property-0-value-XVQOUE7CQeIYD",
                "property-10": "property-10-value-YyS2JiSbyVvys3nsLnyd26DKGSlJJFT",
                "property-5": "property-5-value-fPgPsNOXNuv2hjM9oJx7b6dzFMAGrlLybUxIiEhbeqvP9ekOCF1zBWskhXZUyBrTv4B9qbIyLqoJt0TKSaRxbiml0pfMw",
                "property-6": "property-6-value-txiRJAM4qITnE5MpROii46wjXDqN2Rci1MTNcKmIvW9O9NDqVbrhLhOg53oxG0i070xsjOakRDBfJjqymE6ZmaBwa",
                "property-3": "property-3-value-P2jqV7vH8SXbdtQuG6f2Blaz4qtYxdVQ0Nt7zlQe2PA3PGyMZy1R10N6aE1v1GhvFyvI",
                "property-4": "property-4-value-4HqNxliXh0dcZ6bMZpwfmkm9miClUKuDBUdBOVITRKrxX7pNWjRCz2aS0tIZFhLnfCiNDpr"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/16462884240065277753/findings/fyihx3ltua4xcMSigwngXX1EP108LG/securityMarks",
                "marks": {
                    "test-mark": "test-mark-value-sz"
                }
            },
            "eventTime": "2018-11-01T17:04:15Z",
            "createTime": "2018-11-01T17:04:15Z"
        }
    ]
    return transform_json_to_findings_list(results)


def mock_two_steps_asset_attribute_query():
    results = [
        {
            "asset": {
                "name": "organizations/688851828130/assets/6935692701314546019",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceOwners": [
                        "user:dandrade@gcp-sec-demo-org.joonix.net",
                        "user:lucasbr@gcp-sec-demo-org.joonix.net",
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "name": "asset-dev-project",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "asset-dev-project",
                    "createTime": "2018-02-19t17:02:09.842z",
                    "projectNumber": 138150943629
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/6935692701314546019/securityMarks",
                    "marks": {
                        "scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f": "working_6f04f632-3276-4ff3-b32a-92f794fb0f2f",
                        "scc_query_e4b06e13-2cf7-4372-9c65-ab36039a985d": "true",
                        "new": "1",
                        "environment": "development",
                        "folder": "group1",
                        "test2": "2",
                        "test1": "1",
                        "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                    }
                },
                "createTime": "2018-10-17T22:03:23.376Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/15135412465687133887",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/1091116670070",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/1091116670070",
                    "resourceOwners": [
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "name": "processor-project",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "processor-project",
                    "createTime": "2018-02-27t13:54:54.507z",
                    "projectNumber": 1091116670070
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/15135412465687133887/securityMarks",
                    "marks": {
                        "scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f": "working_6f04f632-3276-4ff3-b32a-92f794fb0f2f",
                        "priority": "high-critical"
                    }
                },
                "createTime": "2018-10-17T22:03:23.376Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        }
    ]
    return transform_json_to_asset_list(results)


def mock_two_steps_asset_attribute_mult_query():
    results = [
        {
            "asset": {
                "name": "organizations/688851828130/assets/6935692701314546019",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceOwners": [
                        "user:dandrade@gcp-sec-demo-org.joonix.net",
                        "user:lucasbr@gcp-sec-demo-org.joonix.net",
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "name": "asset-dev-project",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "asset-dev-project",
                    "createTime": "2018-02-19t17:02:09.842z",
                    "projectNumber": 138150943629
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/6935692701314546019/securityMarks",
                    "marks": {
                        "scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f": "working_6f04f632-3276-4ff3-b32a-92f794fb0f2f",
                        "scc_query_e4b06e13-2cf7-4372-9c65-ab36039a985d": "true",
                        "new": "1",
                        "environment": "development",
                        "folder": "group1",
                        "test2": "2",
                        "test1": "1",
                        "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                    }
                },
                "createTime": "2018-10-17T22:03:23.376Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/16389676671780941579",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/592766336107",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/592766336107",
                    "resourceOwners": [
                        "user:dandrade@ciandt.com"
                    ]
                },
                "resourceProperties": {
                    "name": "joonix-net-forseti-22",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "joonix-net-forseti-22",
                    "createTime": "2018-08-31t16:08:58.752z",
                    "projectNumber": 592766336107
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/16389676671780941579/securityMarks",
                    "marks": {
                        "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                    }
                },
                "createTime": "2018-09-01T00:34:42.555Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/15135412465687133887",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/1091116670070",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/1091116670070",
                    "resourceOwners": [
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "name": "processor-project",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "processor-project",
                    "createTime": "2018-02-27t13:54:54.507z",
                    "projectNumber": 1091116670070
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/15135412465687133887/securityMarks",
                    "marks": {
                        "scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f": "working_6f04f632-3276-4ff3-b32a-92f794fb0f2f",
                        "priority": "high-critical"
                    }
                },
                "createTime": "2018-10-17T22:03:23.376Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/16315672115541834147",
                "securityCenterProperties": {
                    "resourceName": "//cloudresourcemanager.googleapis.com/projects/926212738021",
                    "resourceType": "google.cloud.resourcemanager.Project",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/organizations/688851828130",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/926212738021",
                    "resourceOwners": [
                        "user:lucasbr@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "name": "public-firing-range-test",
                    "lifecycleState": "active",
                    "parent": "{\"id\":\"688851828130\",\"type\":\"organization\"}",
                    "projectId": "public-firing-range-test",
                    "createTime": "2018-04-02t18:52:04.595z",
                    "projectNumber": 926212738021
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/16315672115541834147/securityMarks",
                    "marks": {
                        "environment": "development",
                        "scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f": "working_6f04f632-3276-4ff3-b32a-92f794fb0f2f"
                    }
                },
                "createTime": "2018-10-17T22:03:23.376Z",
                "updateTime": "2018-10-17T22:03:23.376Z"
            },
            "state": "UNUSED"
        }
    ]
    return transform_json_to_asset_list(results)


def mock_one_step_asset_from_reference_time_timestamp():
    results = [
        {
            "asset": {
                "name": "organizations/688851828130/assets/3995505764686144800",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/asset-dev-project/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceOwners": [
                        "user:dandrade@gcp-sec-demo-org.joonix.net",
                        "user:lucasbr@gcp-sec-demo-org.joonix.net",
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-02-22t05:51:04.672-08:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-east2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west1/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "2032409055311655975"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/3995505764686144800/securityMarks",
                    "marks": {
                        "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                    }
                },
                "createTime": "2018-04-20T17:34:14.579Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/7138906440330386899",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/bin-auth-playground/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/246054159221",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/246054159221",
                    "resourceOwners": [
                        "user:andychang@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-09-24t14:18:40.340-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/asia-east2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/bin-auth-playground/regions/europe-west1/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/bin-auth-playground/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "2683120970314869343"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/7138906440330386899/securityMarks"
                },
                "createTime": "2018-10-17T22:03:23.376Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/9602302522585090921",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/binary-authorization-demo/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                    "resourceOwners": [
                        "user:andychang@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-09-24t14:10:12.622-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/europe-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/asia-east2/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "1936045996547304539"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/9602302522585090921/securityMarks"
                },
                "createTime": "2018-09-26T06:14:11.188Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/14944354827709073870",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/binary-authorization-demo/global/networks/ba-vpc-custom",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                    "resourceOwners": [
                        "user:andychang@google.com"
                    ]
                },
                "resourceProperties": {
                    "peerings": "[{\"autoCreateRoutes\":true,\"name\":\"marine-physics-196005\",\"network\":\"https://www.googleapis.com/compute/v1/projects/marine-physics-196005/global/networks/shared-vpc\",\"state\":\"ACTIVE\",\"stateDetails\":\"[2018-11-13T08:50:23.126-08:00]: Connected.\"}]",
                    "creationTimestamp": "2018-11-13t06:08:43.992-08:00",
                    "name": "ba-vpc-custom",
                    "autoCreateSubnetworks": False,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/northamerica-northeast1/subnetworks/ba-vpc-custom\"]",
                    "description": "ba-vpc-custom",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/networks/ba-vpc-custom",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "7301632490643874820"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/14944354827709073870/securityMarks"
                },
                "createTime": "2018-11-13T14:44:40.325Z",
                "updateTime": "2018-11-13T21:24:32.909Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/3333634753517903522",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/cai-demo-spanner/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/581282749270",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/581282749270",
                    "resourceOwners": [
                        "user:andychang@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-10-24t10:00:03.542-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/asia-east2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/regions/europe-west1/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/cai-demo-spanner/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "6058293682417507324"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/3333634753517903522/securityMarks"
                },
                "createTime": "2018-10-25T03:36:48.744Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/5059612515522354630",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/connector-project/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/520732501711",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/520732501711",
                    "resourceOwners": [
                        "user:andychang@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-03-16t19:13:01.367-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-east2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west1/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/connector-project/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "1071120697868273474"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/5059612515522354630/securityMarks"
                },
                "createTime": "2018-04-20T17:34:19.079Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/5167317835587742874",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/container-security-demo/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/267334838076",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/267334838076",
                    "resourceOwners": [
                        "user:andychang@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-07-20t07:15:38.664-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/asia-east2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/europe-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/container-security-demo/regions/us-west2/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/container-security-demo/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "575990502877057125"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/5167317835587742874/securityMarks"
                },
                "createTime": "2018-07-20T14:35:21.085Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/1069234652890424427",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/dev-gcpsec-dns-control/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/861568220405",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/861568220405",
                    "resourceOwners": [
                        "user:joaog@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-06-14t08:21:48.894-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/europe-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/regions/asia-east2/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/dev-gcpsec-dns-control/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "5785702394588247779"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/1069234652890424427/securityMarks"
                },
                "createTime": "2018-06-15T00:42:06.922Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/2961395655930947049",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/jonnys-demo/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/544181147435",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/544181147435",
                    "resourceOwners": [
                        "serviceAccount:dlp-cscc@jonnys-demo.iam.gserviceaccount.com",
                        "user:jonshannon@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-11-01t08:51:25.598-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/asia-east2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/europe-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/jonnys-demo/regions/asia-south1/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/jonnys-demo/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "8001545648307871250"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/2961395655930947049/securityMarks"
                },
                "createTime": "2018-11-01T22:16:11.646Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/2308216065789111595",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/joonix-net-forseti-22/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/592766336107",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/592766336107",
                    "resourceOwners": [
                        "user:dandrade@ciandt.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-09-06t07:00:41.463-07:00",
                    "name": "default",
                    "autoCreateSubnetworks": True,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/europe-north1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/us-central1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/asia-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/asia-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/northamerica-northeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/southamerica-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/us-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/us-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/us-east4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/europe-west1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/asia-south1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/europe-west4/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/europe-west3/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/us-east1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/australia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/europe-west2/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/asia-southeast1/subnetworks/default\",\"https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/regions/asia-east2/subnetworks/default\"]",
                    "description": "default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/joonix-net-forseti-22/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "4704048626643275238"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/2308216065789111595/securityMarks",
                    "marks": {
                        "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                    }
                },
                "createTime": "2018-09-07T12:11:01.823Z",
                "updateTime": "2018-11-09T14:42:52.490Z"
            },
            "state": "UNUSED"
        },{
            "asset": {
                "name": "organizations/688851828130/assets/2214089322352174761",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/marine-physics-196005/global/networks/shared-vpc",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/1000586090784",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/1000586090784",
                    "resourceOwners": [
                        "serviceAccount:catman-demo-controller@marine-physics-196005.iam.gserviceaccount.com",
                        "user:iben@google.com"
                    ]
                },
                "resourceProperties": {
                    "peerings": "[{\"autoCreateRoutes\":true,\"name\":\"vpc-network-peering\",\"network\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/networks/ba-vpc-custom\",\"state\":\"ACTIVE\",\"stateDetails\":\"[2018-11-13T08:50:23.126-08:00]: Connected.\"}]",
                    "creationTimestamp": "2018-11-13t06:00:32.359-08:00",
                    "name": "shared-vpc",
                    "autoCreateSubnetworks": False,
                    "subnetwork": "[\"https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/northamerica-northeast1/subnetworks/shared-vpc\"]",
                    "description": "shared-vpc",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/marine-physics-196005/global/networks/shared-vpc",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": "1338429274730227695"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/2214089322352174761/securityMarks"
                },
                "createTime": "2018-11-13T14:44:40.325Z",
                "updateTime": "2018-11-13T21:24:32.909Z"
            },
            "state": "UNUSED"
        }
    ]
    return transform_json_to_asset_list(results)


def mock_one_step_finding_from_reference_time_fromnow():
    results = [
        {
            "name": "organizations/688851828130/sources/10525437515560121179/findings/ac785971e7024c609d91f47211519d3e",
            "parent": "organizations/688851828130/sources/10525437515560121179",
            "resourceName": "//compute.googleapis.com/projects/container-security-demo/zones/us-central1-a/instances/gke-cluster-sec-demo-tar-default-pool-0dfce3bb-mnrn",
            "state": "ACTIVE",
            "category": "CONTAINER_RUNTIME_ANOMALY-HIGH_RISK_IP",
            "externalUri": "http://35.197.45.209:8081/#!/login",
            "sourceProperties": {
                "host": "liron-srv",
                "sccCategory": "Container Runtime Anomaly - High Risk IP",
                "sccStatus": "ACTIVE",
                "msg": "Connection to high risk IP 54.88.32.27:80, which is explicitly blocked in the runtime rule",
                "sccStat": "info​",
                "container": "/nifty_poincare",
                "url": "http://35.197.45.209:8081/#!/login",
                "scc_status": "ACTIVE",
                "scc_source_category_id": "CONTAINER_RUNTIME_ANOMALY-HIGH_RISK_IP",
                "sccSeverity": "high",
                "image": "alpine:3.7",
                "rule": "Default - alert on suspicious runtime behavior"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/10525437515560121179/findings/ac785971e7024c609d91f47211519d3e/securityMarks"
            },
            "eventTime": "2018-07-20T18:31:29Z",
            "createTime": "2018-07-20T18:31:29Z"
        }
    ]
    return transform_json_to_findings_list(results)

def mock_two_step_asset_from_reference_time_with_duration():
    results = [
        {
            "name": "organizations/688851828130/sources/2290967579963267363/findings/4001d015826143da8cffb19fadf11486",
            "parent": "organizations/688851828130/sources/2290967579963267363",
            "resourceName": "//storage.googleapis.com/findings-joonix-20180316",
            "state": "ACTIVE",
            "category": "ADDED",
            "sourceProperties": {
                "inventory_data": "{\"bindings\":[{\"role\":\"organizations/389856079330/roles/custom.gaeAppCreator\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/accesscontextmanager.policyAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:doctorevil@gmail.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyEditor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyReader\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.appAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.appViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.deployer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.serviceAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengineflex.serviceAgent\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/bigquery.dataViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/billing.admin\",\"members\":[\"user:andychang@google.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/billing.creator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\"]},{\"role\":\"roles/billing.user\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/browser\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudfunctions.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudfunctions.serviceAgent\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudsecurityscanner.editor\",\"members\":[\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudsql.viewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudtasks.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/compute.networkViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/compute.securityAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.admin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/datastore.owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/deploymentmanager.editor\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/dlp.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.organizationRoleAdmin\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\"]},{\"role\":\"roles/iam.securityReviewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.serviceAccountActor\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/orgpolicy.policyAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/pubsub.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/resourcemanager.folderAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderCreator\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\",\"user:joaov@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationViewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectCreator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:cscc-prod-forseti@csccapi389856079330.iam.gserviceaccount.com\",\"serviceAccount:cscc-stage-forseti@csccstagingapi389856079330.iam.gserviceaccount.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.serviceAgent\",\"members\":[\"serviceAccount:service-682621944808@security-center-api.iam.gserviceaccount.com\",\"serviceAccount:service-833212224379@security-center-api-staging.iam.gserviceaccount.com\"]},{\"role\":\"roles/securitycenter.viewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:gcp-sec-demo-org-forseti-cscc-whitelist@googlegroups.com\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/servicemanagement.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/storage.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/storage.objectAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]}],\"etag\":\"BwVnpyK7WKU=\"}",
                "summary": "Allow only IAM members in my domain to have VPC service control roles",
                "resource_id": "389856079330",
                "inventory_index_id": "2018-03-19T17:10:16.51699",
                "resource_type": "organization",
                "rule_index": "2",
                "url": "",
                "scc_status": "ACTIVE",
                "violation_data": "{\"member\":\"user:doctorevil@gmail.com\",\"role\":\"roles/accesscontextmanager.policyAdmin\",\"full_name\":\"organization/389856079330/\"}",
                "scc_source_category_id": "ADDED"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/2290967579963267363/findings/4001d015826143da8cffb19fadf11486/securityMarks"
            },
            "eventTime": "2018-03-19T17:10:51Z",
            "createTime": "2018-03-19T17:10:51Z"
        },
        {
            "name": "organizations/688851828130/sources/2290967579963267363/findings/5962be65012b445a9d2004bf3359683a",
            "parent": "organizations/688851828130/sources/2290967579963267363",
            "resourceName": "//storage.googleapis.com/findings-joonix-20180316",
            "state": "ACTIVE",
            "category": "ADDED",
            "sourceProperties": {
                "inventory_data": "{\"bindings\":[{\"role\":\"organizations/389856079330/roles/custom.gaeAppCreator\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/accesscontextmanager.policyAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:doctorevil@gmail.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyEditor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyReader\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.appAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.appViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.deployer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.serviceAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengineflex.serviceAgent\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/bigquery.dataViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/billing.admin\",\"members\":[\"user:andychang@google.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/billing.creator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\"]},{\"role\":\"roles/billing.user\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/browser\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudfunctions.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudfunctions.serviceAgent\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudsecurityscanner.editor\",\"members\":[\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudsql.viewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudtasks.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/compute.networkViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/compute.securityAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.admin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/datastore.owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/deploymentmanager.editor\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/dlp.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.organizationRoleAdmin\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\"]},{\"role\":\"roles/iam.securityReviewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.serviceAccountActor\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/orgpolicy.policyAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/pubsub.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/resourcemanager.folderAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderCreator\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\",\"user:joaov@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationViewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectCreator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:cscc-prod-forseti@csccapi389856079330.iam.gserviceaccount.com\",\"serviceAccount:cscc-stage-forseti@csccstagingapi389856079330.iam.gserviceaccount.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.serviceAgent\",\"members\":[\"serviceAccount:service-682621944808@security-center-api.iam.gserviceaccount.com\",\"serviceAccount:service-833212224379@security-center-api-staging.iam.gserviceaccount.com\"]},{\"role\":\"roles/securitycenter.viewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:gcp-sec-demo-org-forseti-cscc-whitelist@googlegroups.com\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/servicemanagement.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/storage.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/storage.objectAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]}],\"etag\":\"BwVnpyK7WKU=\"}",
                "summary": "Allow only IAM members in my domain to have VPC service control roles",
                "resource_id": "389856079330",
                "inventory_index_id": "2018-03-19T17:12:16.00823",
                "resource_type": "organization",
                "rule_index": "2",
                "url": "",
                "scc_status": "ACTIVE",
                "violation_data": "{\"member\":\"user:doctorevil@gmail.com\",\"role\":\"roles/accesscontextmanager.policyAdmin\",\"full_name\":\"organization/389856079330/\"}",
                "scc_source_category_id": "ADDED"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/2290967579963267363/findings/5962be65012b445a9d2004bf3359683a/securityMarks"
            },
            "eventTime": "2018-03-19T17:12:50Z",
            "createTime": "2018-03-19T17:12:50Z"
        },
        {
            "name": "organizations/688851828130/sources/2290967579963267363/findings/5b59267902874adea483f261d6cc87ba",
            "parent": "organizations/688851828130/sources/2290967579963267363",
            "resourceName": "//storage.googleapis.com/findings-joonix-20180316",
            "state": "ACTIVE",
            "category": "ADDED",
            "sourceProperties": {
                "inventory_data": "{\"bindings\":[{\"role\":\"organizations/389856079330/roles/custom.gaeAppCreator\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/accesscontextmanager.policyAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:doctorevil@gmail.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyEditor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyReader\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.appAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.appViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.deployer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.serviceAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengineflex.serviceAgent\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/bigquery.dataViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/billing.admin\",\"members\":[\"user:andychang@google.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/billing.creator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\"]},{\"role\":\"roles/billing.user\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/browser\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudfunctions.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudfunctions.serviceAgent\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudsecurityscanner.editor\",\"members\":[\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudsql.viewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudtasks.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/compute.networkViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/compute.securityAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.admin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/datastore.owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/deploymentmanager.editor\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/dlp.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.organizationRoleAdmin\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\"]},{\"role\":\"roles/iam.securityReviewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.serviceAccountActor\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/orgpolicy.policyAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/pubsub.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/resourcemanager.folderAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderCreator\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\",\"user:joaov@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationViewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectCreator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:cscc-prod-forseti@csccapi389856079330.iam.gserviceaccount.com\",\"serviceAccount:cscc-stage-forseti@csccstagingapi389856079330.iam.gserviceaccount.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.serviceAgent\",\"members\":[\"serviceAccount:service-682621944808@security-center-api.iam.gserviceaccount.com\",\"serviceAccount:service-833212224379@security-center-api-staging.iam.gserviceaccount.com\"]},{\"role\":\"roles/securitycenter.viewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:gcp-sec-demo-org-forseti-cscc-whitelist@googlegroups.com\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/servicemanagement.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/storage.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/storage.objectAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]}],\"etag\":\"BwVnpyK7WKU=\"}",
                "summary": "Allow only IAM members in my domain to have VPC service control roles",
                "resource_id": "389856079330",
                "inventory_index_id": "2018-03-19T17:18:16.43799",
                "resource_type": "organization",
                "rule_index": "2",
                "url": "",
                "scc_status": "ACTIVE",
                "violation_data": "{\"member\":\"user:doctorevil@gmail.com\",\"role\":\"roles/accesscontextmanager.policyAdmin\",\"full_name\":\"organization/389856079330/\"}",
                "scc_source_category_id": "ADDED"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/2290967579963267363/findings/5b59267902874adea483f261d6cc87ba/securityMarks"
            },
            "eventTime": "2018-03-19T17:18:51Z",
            "createTime": "2018-03-19T17:18:51Z"
        },
        {
            "name": "organizations/688851828130/sources/2290967579963267363/findings/d5112eb4dc6a43efbe94bf86754be5b9",
            "parent": "organizations/688851828130/sources/2290967579963267363",
            "resourceName": "//storage.googleapis.com/findings-joonix-20180316",
            "state": "ACTIVE",
            "category": "ADDED",
            "sourceProperties": {
                "inventory_data": "{\"bindings\":[{\"role\":\"organizations/389856079330/roles/custom.gaeAppCreator\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/accesscontextmanager.policyAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:doctorevil@gmail.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyEditor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyReader\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.appAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.appViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.deployer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.serviceAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengineflex.serviceAgent\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/bigquery.dataViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/billing.admin\",\"members\":[\"user:andychang@google.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/billing.creator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\"]},{\"role\":\"roles/billing.user\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/browser\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudfunctions.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudfunctions.serviceAgent\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudsecurityscanner.editor\",\"members\":[\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudsql.viewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudtasks.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/compute.networkViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/compute.securityAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.admin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/datastore.owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/deploymentmanager.editor\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/dlp.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.organizationRoleAdmin\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\"]},{\"role\":\"roles/iam.securityReviewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.serviceAccountActor\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/orgpolicy.policyAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/pubsub.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/resourcemanager.folderAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderCreator\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\",\"user:joaov@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationViewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectCreator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:cscc-prod-forseti@csccapi389856079330.iam.gserviceaccount.com\",\"serviceAccount:cscc-stage-forseti@csccstagingapi389856079330.iam.gserviceaccount.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.serviceAgent\",\"members\":[\"serviceAccount:service-682621944808@security-center-api.iam.gserviceaccount.com\",\"serviceAccount:service-833212224379@security-center-api-staging.iam.gserviceaccount.com\"]},{\"role\":\"roles/securitycenter.viewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:gcp-sec-demo-org-forseti-cscc-whitelist@googlegroups.com\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/servicemanagement.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/storage.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/storage.objectAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]}],\"etag\":\"BwVnpyK7WKU=\"}",
                "summary": "Allow only IAM members in my domain to have VPC service control roles",
                "resource_id": "389856079330",
                "inventory_index_id": "2018-03-19T17:14:16.49436",
                "resource_type": "organization",
                "rule_index": "2",
                "url": "",
                "scc_status": "ACTIVE",
                "violation_data": "{\"member\":\"user:doctorevil@gmail.com\",\"role\":\"roles/accesscontextmanager.policyAdmin\",\"full_name\":\"organization/389856079330/\"}",
                "scc_source_category_id": "ADDED"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/2290967579963267363/findings/d5112eb4dc6a43efbe94bf86754be5b9/securityMarks"
            },
            "eventTime": "2018-03-19T17:14:51Z",
            "createTime": "2018-03-19T17:14:51Z"
        },
        {
            "name": "organizations/688851828130/sources/2290967579963267363/findings/d6bd689a59b94beea1049de4cf51d50f",
            "parent": "organizations/688851828130/sources/2290967579963267363",
            "resourceName": "//storage.googleapis.com/findings-joonix-20180316",
            "state": "ACTIVE",
            "category": "ADDED",
            "sourceProperties": {
                "inventory_data": "{\"bindings\":[{\"role\":\"organizations/389856079330/roles/custom.gaeAppCreator\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/accesscontextmanager.policyAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:doctorevil@gmail.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyEditor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyReader\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.appAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.appViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.deployer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.serviceAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengineflex.serviceAgent\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/bigquery.dataViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/billing.admin\",\"members\":[\"user:andychang@google.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/billing.creator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\"]},{\"role\":\"roles/billing.user\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/browser\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudfunctions.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudfunctions.serviceAgent\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudsecurityscanner.editor\",\"members\":[\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudsql.viewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudtasks.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/compute.networkViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/compute.securityAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.admin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/datastore.owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/deploymentmanager.editor\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/dlp.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.organizationRoleAdmin\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\"]},{\"role\":\"roles/iam.securityReviewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.serviceAccountActor\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/orgpolicy.policyAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/pubsub.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/resourcemanager.folderAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderCreator\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\",\"user:joaov@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationViewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectCreator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:cscc-prod-forseti@csccapi389856079330.iam.gserviceaccount.com\",\"serviceAccount:cscc-stage-forseti@csccstagingapi389856079330.iam.gserviceaccount.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.serviceAgent\",\"members\":[\"serviceAccount:service-682621944808@security-center-api.iam.gserviceaccount.com\",\"serviceAccount:service-833212224379@security-center-api-staging.iam.gserviceaccount.com\"]},{\"role\":\"roles/securitycenter.viewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:gcp-sec-demo-org-forseti-cscc-whitelist@googlegroups.com\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/servicemanagement.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/storage.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/storage.objectAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]}],\"etag\":\"BwVnpyK7WKU=\"}",
                "summary": "Allow only IAM members in my domain to have VPC service control roles",
                "resource_id": "389856079330",
                "inventory_index_id": "2018-03-19T17:16:16.68258",
                "resource_type": "organization",
                "rule_index": "2",
                "url": "",
                "scc_status": "ACTIVE",
                "violation_data": "{\"member\":\"user:doctorevil@gmail.com\",\"role\":\"roles/accesscontextmanager.policyAdmin\",\"full_name\":\"organization/389856079330/\"}",
                "scc_source_category_id": "ADDED"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/2290967579963267363/findings/d6bd689a59b94beea1049de4cf51d50f/securityMarks"
            },
            "eventTime": "2018-03-19T17:16:52Z",
            "createTime": "2018-03-19T17:16:52Z"
        },
        {
            "name": "organizations/688851828130/sources/2290967579963267363/findings/f7309aa80c3b42e18ba5acc50fcb742c",
            "parent": "organizations/688851828130/sources/2290967579963267363",
            "resourceName": "//storage.googleapis.com/findings-joonix-20180316",
            "state": "ACTIVE",
            "category": "ADDED",
            "sourceProperties": {
                "inventory_data": "{\"bindings\":[{\"role\":\"organizations/389856079330/roles/custom.gaeAppCreator\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/accesscontextmanager.policyAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:doctorevil@gmail.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyEditor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/accesscontextmanager.policyReader\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.appAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.appViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/appengine.deployer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengine.serviceAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/appengineflex.serviceAgent\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/bigquery.dataViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/billing.admin\",\"members\":[\"user:andychang@google.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/billing.creator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\"]},{\"role\":\"roles/billing.user\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/browser\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudfunctions.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudfunctions.serviceAgent\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudsecurityscanner.editor\",\"members\":[\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/cloudsql.viewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/cloudtasks.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/compute.networkViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/compute.securityAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.admin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/container.developer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/datastore.owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/deploymentmanager.editor\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/dlp.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.organizationRoleAdmin\",\"members\":[\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\"]},{\"role\":\"roles/iam.securityReviewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/iam.serviceAccountActor\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/orgpolicy.policyAdmin\",\"members\":[\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/owner\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/pubsub.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]},{\"role\":\"roles/resourcemanager.folderAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderCreator\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.folderIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:jamesharding@gcp-sec-demo-org-forseti.joonix.net\",\"user:joaov@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.organizationViewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectCreator\",\"members\":[\"domain:gcp-sec-demo-org-forseti.joonix.net\",\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:1068660800787@cloudservices.gserviceaccount.com\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/resourcemanager.projectIamAdmin\",\"members\":[\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"group:security-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:andychang@google.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.editor\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:cscc-prod-forseti@csccapi389856079330.iam.gserviceaccount.com\",\"serviceAccount:cscc-stage-forseti@csccstagingapi389856079330.iam.gserviceaccount.com\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/securitycenter.serviceAgent\",\"members\":[\"serviceAccount:service-682621944808@security-center-api.iam.gserviceaccount.com\",\"serviceAccount:service-833212224379@security-center-api-staging.iam.gserviceaccount.com\"]},{\"role\":\"roles/securitycenter.viewer\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:gcp-sec-demo-org-forseti-cscc-whitelist@googlegroups.com\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"user:raghuagarwal@google.com\"]},{\"role\":\"roles/servicemanagement.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/servicemanagement.quotaViewer\",\"members\":[\"serviceAccount:forseti-server-gcp-0045@forseti-196022.iam.gserviceaccount.com\",\"serviceAccount:forseti-server-gcp-3806@forseti-196022.iam.gserviceaccount.com\"]},{\"role\":\"roles/storage.admin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"group:partner-access@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\",\"user:tribeiro@gcp-sec-demo-org-forseti.joonix.net\"]},{\"role\":\"roles/storage.objectAdmin\",\"members\":[\"group:admins@gcp-sec-demo-org-forseti.joonix.net\",\"serviceAccount:creator@connector-project-forseti.iam.gserviceaccount.com\"]}],\"etag\":\"BwVnpyK7WKU=\"}",
                "summary": "Allow only IAM members in my domain to have VPC service control roles",
                "resource_id": "389856079330",
                "inventory_index_id": "2018-03-19T17:16:16.68258",
                "resource_type": "organization",
                "rule_index": "2",
                "url": "",
                "scc_status": "ACTIVE",
                "violation_data": "{\"member\":\"user:doctorevil@gmail.com\",\"role\":\"roles/accesscontextmanager.policyAdmin\",\"full_name\":\"organization/389856079330/\"}",
                "scc_source_category_id": "ADDED"
            },
            "securityMarks": {
                "name": "organizations/688851828130/sources/2290967579963267363/findings/f7309aa80c3b42e18ba5acc50fcb742c/securityMarks"
            },
            "eventTime": "2018-03-19T17:16:52Z",
            "createTime": "2018-03-19T17:16:52Z"
        }
    ]
    return transform_json_to_findings_list(results)