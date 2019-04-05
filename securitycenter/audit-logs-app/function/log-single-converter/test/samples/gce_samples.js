'use strict';

function createInstance() {
    return {
        "insertId": "-6xb03le1a09m",
        "logName": "projects/gce-audit-logs-216020/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
          "first": true,
          "id": "operation-1536615686183-5758b38219858-53b1bb82-d6cc63f7",
          "producer": "type.googleapis.com"
        },
        "protoPayload": {
          "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
          "authenticationInfo": {
            "principalEmail": "dandrade@ciandt.com"
          },
          "authorizationInfo": [
            {
              "granted": true,
              "permission": "compute.instances.create",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
                "service": "compute",
                "type": "compute.instances"
              }
            },
            {
              "granted": true,
              "permission": "compute.disks.create",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020/zones/us-east1-b/disks/instance-victim-1",
                "service": "compute",
                "type": "compute.disks"
              }
            },
            {
              "granted": true,
              "permission": "compute.subnetworks.use",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020/regions/us-east1/subnetworks/default",
                "service": "compute",
                "type": "compute.subnetworks"
              }
            },
            {
              "granted": true,
              "permission": "compute.subnetworks.useExternalIp",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020/regions/us-east1/subnetworks/default",
                "service": "compute",
                "type": "compute.subnetworks"
              }
            },
            {
              "granted": true,
              "permission": "compute.instances.setMetadata",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
                "service": "compute",
                "type": "compute.instances"
              }
            },
            {
              "granted": true,
              "permission": "compute.instances.setServiceAccount",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
                "service": "compute",
                "type": "compute.instances"
              }
            }
          ],
     "methodName": "beta.compute.instances.insert",
    "request": {
      "@type": "type.googleapis.com/compute.instances.insert",
      "canIpForward": false,
      "deletionProtection": false,
      "description": "",
      "disks": [
        {
          "autoDelete": true,
          "boot": true,
          "deviceName": "instance-victim-1",
          "initializeParams": {
            "diskSizeGb": "10",
            "diskType": "projects/gce-audit-logs-216020/zones/us-east1-b/diskTypes/pd-standard",
            "sourceImage": "projects/debian-cloud/global/images/debian-9-stretch-v20180820"
          },
          "mode": "READ_WRITE",
          "type": "PERSISTENT"
        }
      ],
      "machineType": "projects/gce-audit-logs-216020/zones/us-east1-b/machineTypes/n1-standard-1",
      "name": "instance-victim-1",
      "networkInterfaces": [
        {
          "accessConfigs": [
            {
              "name": "External NAT",
              "networkTier": "PREMIUM",
              "type": "ONE_TO_ONE_NAT"
            }
          ],
          "subnetwork": "projects/gce-audit-logs-216020/regions/us-east1/subnetworks/default"
        }
      ],
      "scheduling": {
        "automaticRestart": true,
        "onHostMaintenance": "MIGRATE",
        "preemptible": false
      },
      "serviceAccounts": [
        {
          "email": "620146303431-compute@developer.gserviceaccount.com",
          "scopes": [
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring.write",
            "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/service.management.readonly",
            "https://www.googleapis.com/auth/trace.append"
          ]
        }
      ]
    },
    "requestMetadata": {
      "callerIp": "2002:a30:178a:0:0:0:0:0",
      "callerSuppliedUserAgent": "Pantheon Google-API-Java-Client Google-HTTP-Java-Client/1.25.0-SNAPSHOT (gzip)"
    },
    "resourceLocation": {
      "currentLocations": [
        "us-east1-b"
      ]
    },
    "resourceName": "projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
    "response": {
      "@type": "type.googleapis.com/operation",
      "id": "284992393952582632",
      "insertTime": "2018-09-10T14:41:27.400-07:00",
      "name": "operation-1536615686183-5758b38219858-53b1bb82-d6cc63f7",
      "operationType": "insert",
      "progress": "0",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/gce-audit-logs-216020/zones/us-east1-b/operations/operation-1536615686183-5758b38219858-53b1bb82-d6cc63f7",
      "status": "PENDING",
      "targetId": "7001864148707138537",
      "targetLink": "https://www.googleapis.com/compute/beta/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
      "user": "dandrade@ciandt.com",
      "zone": "https://www.googleapis.com/compute/beta/projects/gce-audit-logs-216020/zones/us-east1-b"
    },
    "serviceName": "compute.googleapis.com"
  },
  "receiveTimestamp": "2018-09-10T21:41:27.940788716Z",
  "resource": {
    "labels": {
      "instance_id": "7001864148707138537",
      "project_id": "gce-audit-logs-216020",
      "zone": "us-east1-b"
    },
    "type": "gce_instance"
  },
  "severity": "NOTICE",
  "timestamp": "2018-09-10T21:41:26.260Z"
}
};

function deleteInstance() {
    return {
        "insertId": "-epdbpzcec8",
        "logName": "projects/gce-audit-logs-216020/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
          "id": "operation-1536619956944-5758c36b03c81-c8f9dce5-51951898",
          "last": true,
          "producer": "compute.googleapis.com"
        },
        "protoPayload": {
          "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
          "authenticationInfo": {
            "principalEmail": "dandrade@ciandt.com"
          },
          "methodName": "v1.compute.instances.delete",
          "requestMetadata": {
            "callerIp": "2002:ae8:6843:0:0:0:0:0",
            "callerSuppliedUserAgent": "Pantheon Google-API-Java-Client Google-HTTP-Java-Client/1.25.0-SNAPSHOT (gzip)"
          },
          "resourceName": "projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
          "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-10T22:53:30.771542180Z",
        "resource": {
          "labels": {
            "instance_id": "7001864148707138537",
            "project_id": "gce-audit-logs-216020",
            "zone": "us-east1-b"
          },
          "type": "gce_instance"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-10T22:53:29.697Z"
      }
};

function setTags() {
    return {
        "insertId": "-27nm5hd57h6",
        "logName": "projects/gce-audit-logs-216020/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
          "first": true,
          "id": "operation-1536615818747-5758b40085c78-3f1cc68c-91fcf10e",
          "producer": "type.googleapis.com"
        },
        "protoPayload": {
          "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
          "authenticationInfo": {
            "principalEmail": "dandrade@ciandt.com"
          },
          "authorizationInfo": [
            {
              "granted": true,
              "permission": "compute.instances.setTags",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
                "service": "compute",
                "type": "compute.instances"
              }
            }
          ],
          "methodName": "v1.compute.instances.setTags",
          "request": {
            "@type": "type.googleapis.com/compute.instances.setTags",
            "fingerprint": "\ufffde\ufffdJ\ufffd|\ufffd#",
            "tags": [
              "https-server"
            ]
          },
          "requestMetadata": {
            "callerIp": "2002:a60:2696:0:0:0:0:0",
            "callerSuppliedUserAgent": "Pantheon Google-API-Java-Client Google-HTTP-Java-Client/1.25.0-SNAPSHOT (gzip)"
          },
          "resourceLocation": {
            "currentLocations": [
              "us-east1-b"
            ]
          },
          "resourceName": "projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
          "response": {
            "@type": "type.googleapis.com/operation",
            "id": "6509938961358216036",
            "insertTime": "2018-09-10T14:43:39.506-07:00",
            "name": "operation-1536615818747-5758b40085c78-3f1cc68c-91fcf10e",
            "operationType": "setTags",
            "progress": "0",
            "selfLink": "https://www.googleapis.com/compute/v1/projects/gce-audit-logs-216020/zones/us-east1-b/operations/operation-1536615818747-5758b40085c78-3f1cc68c-91fcf10e",
            "status": "PENDING",
            "targetId": "7001864148707138537",
            "targetLink": "https://www.googleapis.com/compute/v1/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
            "user": "dandrade@ciandt.com",
            "zone": "https://www.googleapis.com/compute/v1/projects/gce-audit-logs-216020/zones/us-east1-b"
          },
          "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-10T21:43:39.878224747Z",
        "resource": {
          "labels": {
            "instance_id": "7001864148707138537",
            "project_id": "gce-audit-logs-216020",
            "zone": "us-east1-b"
          },
          "type": "gce_instance"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-10T21:43:39.041Z"
      }
};

function setCommonInstanceMetadata() {
    return {
        "insertId": "hhf75me1k034",
        "logName": "projects/gce-audit-logs-216020/logs/cloudaudit.googleapis.com%2Factivity",
        "operation": {
          "first": true,
          "id": "operation-1536619316006-5758c107c4c70-e5cf514c-0e0b4dc7",
          "producer": "type.googleapis.com"
        },
        "protoPayload": {
          "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
          "authenticationInfo": {
            "principalEmail": "dandrade@ciandt.com"
          },
          "authorizationInfo": [
            {
              "granted": true,
              "permission": "compute.projects.setCommonInstanceMetadata",
              "resourceAttributes": {
                "name": "projects/gce-audit-logs-216020",
                "service": "compute",
                "type": "compute.projects"
              }
            }
          ],
          "methodName": "v1.compute.projects.setCommonInstanceMetadata",
          "request": {
            "@type": "type.googleapis.com/compute.projects.setCommonInstanceMetadata"
          },
          "requestMetadata": {
            "callerIp": "201.48.150.197",
            "callerSuppliedUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36,gzip(gfe)"
          },
          "resourceLocation": {
            "currentLocations": [
              "global"
            ]
          },
          "resourceName": "projects/gce-audit-logs-216020",
          "response": {
            "@type": "type.googleapis.com/operation",
            "id": "4030413268605160923",
            "insertTime": "2018-09-10T15:41:56.333-07:00",
            "name": "operation-1536619316006-5758c107c4c70-e5cf514c-0e0b4dc7",
            "operationType": "setMetadata",
            "progress": "0",
            "selfLink": "https://www.googleapis.com/compute/v1/projects/gce-audit-logs-216020/global/operations/operation-1536619316006-5758c107c4c70-e5cf514c-0e0b4dc7",
            "status": "PENDING",
            "targetId": "620146303431",
            "targetLink": "https://www.googleapis.com/compute/v1/projects/gce-audit-logs-216020",
            "user": "dandrade@ciandt.com"
          },
          "serviceName": "compute.googleapis.com"
        },
        "receiveTimestamp": "2018-09-10T22:41:56.846347572Z",
        "resource": {
          "labels": {
            "project_id": "620146303431"
          },
          "type": "gce_project"
        },
        "severity": "NOTICE",
        "timestamp": "2018-09-10T22:41:56.067Z"
      }
};

function deleteDnsZone() {
  return {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "status": {},
      "authenticationInfo": {
        "principalEmail": "amandak@clsecteam.com"
      },
      "requestMetadata": {
        "callerIp": "201.48.150.197",
        "callerSuppliedUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36,gzip(gfe)",
        "requestAttributes": {
          "time": "2018-10-31T16:32:35.898Z",
          "auth": {}
        },
        "destinationAttributes": {}
      },
      "serviceName": "dns.googleapis.com",
      "methodName": "dns.managedZones.delete",
      "authorizationInfo": [
        {
          "permission": "dns.managedZones.delete",
          "granted": true,
          "resourceAttributes": {}
        }
      ],
      "resourceName": "managedZones/demo-zone",
      "request": {
        "@type": "type.googleapis.com/cloud.dns.api.ManagedZonesDeleteRequest",
        "project": "clsecteam-dns-control",
        "managedZone": "demo-zone"
      },
      "response": {
        "@type": "type.googleapis.com/cloud.dns.api.ManagedZonesDeleteResponse"
      }
    },
    "insertId": "-i126b1d5av0",
    "resource": {
      "type": "dns_managed_zone",
      "labels": {
        "location": "global",
        "zone_name": "demo-zone",
        "project_id": "clsecteam-dns-control"
      }
    },
    "timestamp": "2018-10-31T16:32:35.675Z",
    "severity": "NOTICE",
    "logName": "projects/clsecteam-dns-control/logs/cloudaudit.googleapis.com%2Factivity",
    "receiveTimestamp": "2018-10-31T16:32:36.736833803Z"
  }
};


module.exports.createInstance = createInstance;
module.exports.deleteInstance = deleteInstance;
module.exports.setTags = setTags;
module.exports.setCommonInstanceMetadata = setCommonInstanceMetadata;
module.exports.deleteDnsZone = deleteDnsZone;