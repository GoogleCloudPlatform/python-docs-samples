'use strict';

function denyByDefaultRuleDeployUnauthorizedImage() {
  return {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "principalEmail": "amandak@clsecteam.com"
      },
      "authorizationInfo": [
        {
          "permission": "io.k8s.core.v1.pods.create",
          "resource": "core/v1/namespaces/default/pods/image-without-attestation"
        }
      ],
      "methodName": "io.k8s.core.v1.pods.create",
      "request": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "annotations": {
            "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{},\"name\":\"image-without-attestation\",\"namespace\":\"default\"},\"spec\":{\"containers\":[{\"image\":\"gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba\",\"name\":\"image-without-attestation\"}]}}\n"
          },
          "creationTimestamp": null,
          "name": "image-without-attestation",
          "namespace": "default"
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-without-attestation",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "terminationGracePeriodSeconds": 30
        },
        "status": {}
      },
      "requestMetadata": {
        "callerIp": "179.220.250.109"
      },
      "resourceName": "core/v1/namespaces/default/pods/image-without-attestation",
      "response": {
        "@type": "core.k8s.io/v1.Status",
        "apiVersion": "v1",
        "code": 403,
        "details": {
          "kind": "pods",
          "name": "image-without-attestation"
        },
        "kind": "Status",
        "message": "pods \"image-without-attestation\" is forbidden: image policy webhook backend denied one or more images: Denied by cluster admission rule for us-central1-a.test-cluster. Overridden by evaluation mode",
        "metadata": {},
        "reason": "Forbidden",
        "status": "Failure"
      },
      "serviceName": "k8s.io",
      "status": {
        "code": 7,
        "message": "Forbidden"
      }
    },
    "insertId": "dac513c6-3104-4bb2-a526-b3926d2a1401",
    "resource": {
      "type": "k8s_cluster",
      "labels": {
        "project_id": "binary-control-clsecteam",
        "cluster_name": "test-cluster",
        "location": "us-central1-a"
      }
    },
    "timestamp": "2019-02-15T11:43:23.897797Z",
    "labels": {
      "authorization.k8s.io/decision": "allow",
      "authorization.k8s.io/reason": ""
    },
    "logName": "projects/binary-control-clsecteam/logs/cloudaudit.googleapis.com%2Factivity",
    "operation": {
      "id": "dac513c6-3104-4bb2-a526-b3926d2a1401",
      "producer": "k8s.io",
      "first": true,
      "last": true
    },
    "receiveTimestamp": "2019-02-15T11:43:54.317031365Z"
  }
}

function allowDeployAuthorizedImage() {
  return {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "principalEmail": "system:serviceaccount:kube-system:replicaset-controller"
      },
      "authorizationInfo": [
        {
          "granted": true,
          "permission": "io.k8s.core.v1.pods.create",
          "resource": "core/v1/namespaces/default/pods"
        }
      ],
      "methodName": "io.k8s.core.v1.pods.create",
      "request": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "creationTimestamp": null,
          "generateName": "image-path-exempt-from-policy-c5b7ff9fc-",
          "labels": {
            "pod-template-hash": "716399597",
            "run": "image-path-exempt-from-policy"
          },
          "ownerReferences": [
            {
              "apiVersion": "apps/v1",
              "blockOwnerDeletion": true,
              "controller": true,
              "kind": "ReplicaSet",
              "name": "image-path-exempt-from-policy-c5b7ff9fc",
              "uid": "510bd168-310b-11e9-b8fc-42010a8000d6"
            }
          ]
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-path-exempt-from-policy",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "terminationGracePeriodSeconds": 30
        },
        "status": {}
      },
      "requestMetadata": {
        "callerIp": "::1"
      },
      "resourceName": "core/v1/namespaces/default/pods",
      "response": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "annotations": {
            "kubernetes.io/limit-ranger": "LimitRanger plugin set: cpu request for container image-path-exempt-from-policy"
          },
          "creationTimestamp": "2019-02-15T10:23:13Z",
          "generateName": "image-path-exempt-from-policy-c5b7ff9fc-",
          "labels": {
            "pod-template-hash": "716399597",
            "run": "image-path-exempt-from-policy"
          },
          "name": "image-path-exempt-from-policy-c5b7ff9fc-xnxd5",
          "namespace": "default",
          "ownerReferences": [
            {
              "apiVersion": "apps/v1",
              "blockOwnerDeletion": true,
              "controller": true,
              "kind": "ReplicaSet",
              "name": "image-path-exempt-from-policy-c5b7ff9fc",
              "uid": "510bd168-310b-11e9-b8fc-42010a8000d6"
            }
          ],
          "resourceVersion": "25189410",
          "selfLink": "/api/v1/namespaces/default/pods/image-path-exempt-from-policy-c5b7ff9fc-xnxd5",
          "uid": "b32357ba-310b-11e9-b8fc-42010a8000d6"
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-path-exempt-from-policy",
              "resources": {
                "requests": {
                  "cpu": "100m"
                }
              },
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File",
              "volumeMounts": [
                {
                  "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount",
                  "name": "default-token-b5fct",
                  "readOnly": true
                }
              ]
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "priority": 0,
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "serviceAccount": "default",
          "serviceAccountName": "default",
          "terminationGracePeriodSeconds": 30,
          "tolerations": [
            {
              "effect": "NoExecute",
              "key": "node.kubernetes.io/not-ready",
              "operator": "Exists",
              "tolerationSeconds": 300
            },
            {
              "effect": "NoExecute",
              "key": "node.kubernetes.io/unreachable",
              "operator": "Exists",
              "tolerationSeconds": 300
            }
          ],
          "volumes": [
            {
              "name": "default-token-b5fct",
              "secret": {
                "defaultMode": 420,
                "secretName": "default-token-b5fct"
              }
            }
          ]
        },
        "status": {
          "phase": "Pending",
          "qosClass": "Burstable"
        }
      },
      "serviceName": "k8s.io",
      "status": {}
    },
    "insertId": "c52cd26e-d71e-4515-953b-60da855101c5",
    "resource": {
      "type": "k8s_cluster",
      "labels": {
        "location": "us-central1-a",
        "project_id": "binary-control-clsecteam",
        "cluster_name": "test-cluster"
      }
    },
    "timestamp": "2019-02-15T10:23:13.158589Z",
    "labels": {
      "authorization.k8s.io/reason": "RBAC: allowed by ClusterRoleBinding \"system:controller:replicaset-controller\" of ClusterRole \"system:controller:replicaset-controller\" to ServiceAccount \"replicaset-controller/kube-system\"",
      "authorization.k8s.io/decision": "allow"
    },
    "logName": "projects/binary-control-clsecteam/logs/cloudaudit.googleapis.com%2Factivity",
    "operation": {
      "id": "c52cd26e-d71e-4515-953b-60da855101c5",
      "producer": "k8s.io",
      "first": true,
      "last": true
    },
    "receiveTimestamp": "2019-02-15T10:23:18.370540129Z"
  }
}

function allowDeployWithBreakGlass() {
  return {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "principalEmail": "amandak@clsecteam.com"
      },
      "authorizationInfo": [
        {
          "granted": true,
          "permission": "io.k8s.core.v1.pods.create",
          "resource": "core/v1/namespaces/default/pods/image-without-attestation"
        }
      ],
      "methodName": "io.k8s.core.v1.pods.create",
      "request": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "annotations": {
            "alpha.image-policy.k8s.io/break-glass": "true",
            "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{\"alpha.image-policy.k8s.io/break-glass\":\"true\"},\"name\":\"image-without-attestation\",\"namespace\":\"default\"},\"spec\":{\"containers\":[{\"image\":\"gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba\",\"name\":\"image-without-attestation\"}]}}\n"
          },
          "creationTimestamp": null,
          "name": "image-without-attestation",
          "namespace": "default"
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-without-attestation",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "terminationGracePeriodSeconds": 30
        },
        "status": {}
      },
      "requestMetadata": {
        "callerIp": "179.220.250.109"
      },
      "resourceName": "core/v1/namespaces/default/pods/image-without-attestation",
      "response": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "annotations": {
            "alpha.image-policy.k8s.io/break-glass": "true",
            "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{\"alpha.image-policy.k8s.io/break-glass\":\"true\"},\"name\":\"image-without-attestation\",\"namespace\":\"default\"},\"spec\":{\"containers\":[{\"image\":\"gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba\",\"name\":\"image-without-attestation\"}]}}\n",
            "kubernetes.io/limit-ranger": "LimitRanger plugin set: cpu request for container image-without-attestation"
          },
          "creationTimestamp": "2019-02-15T10:20:30Z",
          "name": "image-without-attestation",
          "namespace": "default",
          "resourceVersion": "25189041",
          "selfLink": "/api/v1/namespaces/default/pods/image-without-attestation",
          "uid": "5245e14a-310b-11e9-b8fc-42010a8000d6"
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-without-attestation",
              "resources": {
                "requests": {
                  "cpu": "100m"
                }
              },
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File",
              "volumeMounts": [
                {
                  "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount",
                  "name": "default-token-b5fct",
                  "readOnly": true
                }
              ]
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "priority": 0,
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "serviceAccount": "default",
          "serviceAccountName": "default",
          "terminationGracePeriodSeconds": 30,
          "tolerations": [
            {
              "effect": "NoExecute",
              "key": "node.kubernetes.io/not-ready",
              "operator": "Exists",
              "tolerationSeconds": 300
            },
            {
              "effect": "NoExecute",
              "key": "node.kubernetes.io/unreachable",
              "operator": "Exists",
              "tolerationSeconds": 300
            }
          ],
          "volumes": [
            {
              "name": "default-token-b5fct",
              "secret": {
                "defaultMode": 420,
                "secretName": "default-token-b5fct"
              }
            }
          ]
        },
        "status": {
          "phase": "Pending",
          "qosClass": "Burstable"
        }
      },
      "serviceName": "k8s.io",
      "status": {}
    },
    "insertId": "4a64e55c-0818-440d-8dfa-a8e40e9430ce",
    "resource": {
      "type": "k8s_cluster",
      "labels": {
        "project_id": "binary-control-clsecteam",
        "cluster_name": "test-cluster",
        "location": "us-central1-a"
      }
    },
    "timestamp": "2019-02-15T10:20:30.823262Z",
    "labels": {
      "authorization.k8s.io/decision": "allow",
      "authorization.k8s.io/reason": ""
    },
    "logName": "projects/binary-control-clsecteam/logs/cloudaudit.googleapis.com%2Factivity",
    "operation": {
      "id": "4a64e55c-0818-440d-8dfa-a8e40e9430ce",
      "producer": "k8s.io",
      "first": true,
      "last": true
    },
    "receiveTimestamp": "2019-02-15T10:21:03.513440757Z"
  }
}

function allowDeployWithBreakGlassNewFormat() {
  return   {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "principalEmail": "dandrade@ciandt.com"
      },
      "authorizationInfo": [
        {
          "granted": true,
          "permission": "io.k8s.core.v1.pods.create",
          "resource": "core/v1/namespaces/default/pods/brake-glass-deploy"
        }
      ],
      "methodName": "io.k8s.core.v1.pods.create",
      "request": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "annotations": {
            "alpha.image-policy.k8s.io/break-glass": "true"
          },
          "creationTimestamp": null,
          "name": "brake-glass-deploy",
          "namespace": "default"
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4",
              "imagePullPolicy": "IfNotPresent",
              "name": "brake-glass-deploy",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "terminationGracePeriodSeconds": 30
        },
        "status": {}
      },
      "requestMetadata": {
        "callerIp": "35.196.195.21"
      },
      "resourceName": "core/v1/namespaces/default/pods/brake-glass-deploy",
      "response": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "annotations": {
            "alpha.image-policy.k8s.io/break-glass": "true",
            "kubernetes.io/limit-ranger": "LimitRanger plugin set: cpu request for container brake-glass-deploy"
          },
          "creationTimestamp": "2019-02-28T14:13:13Z",
          "name": "brake-glass-deploy",
          "namespace": "default",
          "resourceVersion": "2282",
          "selfLink": "/api/v1/namespaces/default/pods/brake-glass-deploy",
          "uid": "fc277189-3b62-11e9-aa7c-42010a9a017f"
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4",
              "imagePullPolicy": "IfNotPresent",
              "name": "brake-glass-deploy",
              "resources": {
                "requests": {
                  "cpu": "100m"
                }
              },
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File",
              "volumeMounts": [
                {
                  "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount",
                  "name": "default-token-l6kqm",
                  "readOnly": true
                }
              ]
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "priority": 0,
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "serviceAccount": "default",
          "serviceAccountName": "default",
          "terminationGracePeriodSeconds": 30,
          "tolerations": [
            {
              "effect": "NoExecute",
              "key": "node.kubernetes.io/not-ready",
              "operator": "Exists",
              "tolerationSeconds": 300
            },
            {
              "effect": "NoExecute",
              "key": "node.kubernetes.io/unreachable",
              "operator": "Exists",
              "tolerationSeconds": 300
            }
          ],
          "volumes": [
            {
              "name": "default-token-l6kqm",
              "secret": {
                "defaultMode": 420,
                "secretName": "default-token-l6kqm"
              }
            }
          ]
        },
        "status": {
          "phase": "Pending",
          "qosClass": "Burstable"
        }
      },
      "serviceName": "k8s.io",
      "status": {}
    },
    "insertId": "e614539a-c867-4299-89b1-a21408dacc3b",
    "resource": {
      "type": "k8s_cluster",
      "labels": {
        "project_id": "binary-control-clsecteam-beta",
        "cluster_name": "test-europe-west2-a-cluster",
        "location": "europe-west2-a"
      }
    },
    "timestamp": "2019-02-28T14:13:13.724890Z",
    "labels": {
      "imagepolicywebhook.image-policy.k8s.io/overridden-verification-result": "'gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4': Image gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4 denied by projects/binary-control-clsecteam-beta/attestors/dandrade-attestor: Signature verified, but unexpected message was signed: * Line 1, Column 1\n  Syntax error: value, object or array expected.\n\n",
      "imagepolicywebhook.image-policy.k8s.io/break-glass": "true",
      "authorization.k8s.io/reason": "",
      "authorization.k8s.io/decision": "allow"
    },
    "logName": "projects/binary-control-clsecteam-beta/logs/cloudaudit.googleapis.com%2Factivity",
    "operation": {
      "id": "e614539a-c867-4299-89b1-a21408dacc3b",
      "producer": "k8s.io",
      "first": true,
      "last": true
    },
    "receiveTimestamp": "2019-02-28T14:13:24.110515138Z"
  }
}

function denyDeployWithAttestors() {
  return {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "status": {
        "code": 7,
        "message": "Forbidden"
      },
      "authenticationInfo": {
        "principalEmail": "system:serviceaccount:kube-system:replicaset-controller"
      },
      "requestMetadata": {
        "callerIp": "::1"
      },
      "serviceName": "k8s.io",
      "methodName": "io.k8s.core.v1.pods.create",
      "authorizationInfo": [
        {
          "resource": "core/v1/namespaces/kube-system/pods",
          "permission": "io.k8s.core.v1.pods.create"
        }
      ],
      "resourceName": "core/v1/namespaces/kube-system/pods",
      "request": {
        "status": {},
        "kind": "Pod",
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "metadata": {
          "creationTimestamp": null,
          "labels": {
            "pod-template-hash": "1045328927",
            "k8s-app": "kube-dns"
          },
          "annotations": {
            "scheduler.alpha.kubernetes.io/critical-pod": "",
            "seccomp.security.alpha.kubernetes.io/pod": "docker/default"
          },
          "ownerReferences": [
            {
              "apiVersion": "apps/v1",
              "kind": "ReplicaSet",
              "name": "kube-dns-548976df6c",
              "uid": "6f236ead-e686-11e8-aae7-42010a80005c",
              "controller": true,
              "blockOwnerDeletion": true
            }
          ],
          "generateName": "kube-dns-548976df6c-"
        },
        "spec": {
          "securityContext": {},
          "containers": [
            {
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File",
              "imagePullPolicy": "IfNotPresent",
              "name": "kubedns",
              "args": [
                "--domain=cluster.local.",
                "--dns-port=10053",
                "--config-dir=/kube-dns-config",
                "--v=2"
              ],
              "ports": [
                {
                  "protocol": "UDP",
                  "name": "dns-local",
                  "containerPort": 10053
                },
                {
                  "name": "dns-tcp-local",
                  "containerPort": 10053,
                  "protocol": "TCP"
                },
                {
                  "protocol": "TCP",
                  "name": "metrics",
                  "containerPort": 10055
                }
              ],
              "env": [
                {
                  "name": "PROMETHEUS_PORT",
                  "value": "10055"
                }
              ],
              "readinessProbe": {
                "successThreshold": 1,
                "failureThreshold": 3,
                "httpGet": {
                  "path": "/readiness",
                  "port": 8081,
                  "scheme": "HTTP"
                },
                "initialDelaySeconds": 3,
                "timeoutSeconds": 5,
                "periodSeconds": 10
              },
              "resources": {
                "limits": {
                  "memory": "170Mi"
                },
                "requests": {
                  "cpu": "100m",
                  "memory": "70Mi"
                }
              },
              "volumeMounts": [
                {
                  "name": "kube-dns-config",
                  "mountPath": "/kube-dns-config"
                }
              ],
              "image": "k8s.gcr.io/k8s-dns-kube-dns-amd64:1.14.13",
              "livenessProbe": {
                "failureThreshold": 5,
                "httpGet": {
                  "path": "/healthcheck/kubedns",
                  "port": 10054,
                  "scheme": "HTTP"
                },
                "initialDelaySeconds": 60,
                "timeoutSeconds": 5,
                "periodSeconds": 10,
                "successThreshold": 1
              }
            },
            {
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File",
              "name": "dnsmasq",
              "args": [
                "-v=2",
                "-logtostderr",
                "-configDir=/etc/k8s/dns/dnsmasq-nanny",
                "-restartDnsmasq=true",
                "--",
                "-k",
                "--cache-size=1000",
                "--no-negcache",
                "--log-facility=-",
                "--server=/cluster.local/127.0.0.1#10053",
                "--server=/in-addr.arpa/127.0.0.1#10053",
                "--server=/ip6.arpa/127.0.0.1#10053"
              ],
              "livenessProbe": {
                "initialDelaySeconds": 60,
                "timeoutSeconds": 5,
                "periodSeconds": 10,
                "successThreshold": 1,
                "failureThreshold": 5,
                "httpGet": {
                  "scheme": "HTTP",
                  "path": "/healthcheck/dnsmasq",
                  "port": 10054
                }
              },
              "imagePullPolicy": "IfNotPresent",
              "image": "k8s.gcr.io/k8s-dns-dnsmasq-nanny-amd64:1.14.13",
              "ports": [
                {
                  "name": "dns",
                  "containerPort": 53,
                  "protocol": "UDP"
                },
                {
                  "protocol": "TCP",
                  "name": "dns-tcp",
                  "containerPort": 53
                }
              ],
              "resources": {
                "requests": {
                  "cpu": "150m",
                  "memory": "20Mi"
                }
              },
              "volumeMounts": [
                {
                  "name": "kube-dns-config",
                  "mountPath": "/etc/k8s/dns/dnsmasq-nanny"
                }
              ]
            },
            {
              "name": "sidecar",
              "resources": {
                "requests": {
                  "memory": "20Mi",
                  "cpu": "10m"
                }
              },
              "args": [
                "--v=2",
                "--logtostderr",
                "--probe=kubedns,127.0.0.1:10053,kubernetes.default.svc.cluster.local,5,SRV",
                "--probe=dnsmasq,127.0.0.1:53,kubernetes.default.svc.cluster.local,5,SRV"
              ],
              "imagePullPolicy": "IfNotPresent",
              "ports": [
                {
                  "protocol": "TCP",
                  "name": "metrics",
                  "containerPort": 10054
                }
              ],
              "terminationMessagePath": "/dev/termination-log",
              "image": "k8s.gcr.io/k8s-dns-sidecar-amd64:1.14.13",
              "livenessProbe": {
                "successThreshold": 1,
                "failureThreshold": 5,
                "httpGet": {
                  "port": 10054,
                  "scheme": "HTTP",
                  "path": "/metrics"
                },
                "initialDelaySeconds": 60,
                "timeoutSeconds": 5,
                "periodSeconds": 10
              },
              "terminationMessagePolicy": "File"
            },
            {
              "command": [
                "/monitor",
                "--component=kubedns",
                "--target-port=10054",
                "--stackdriver-prefix=container.googleapis.com/internal/addons",
                "--api-override=https://monitoring.googleapis.com/",
                "--whitelisted-metrics=probe_kubedns_latency_ms,probe_kubedns_errors,dnsmasq_misses,dnsmasq_hits",
                "--pod-id=$(POD_NAME)",
                "--namespace-id=$(POD_NAMESPACE)",
                "--v=2"
              ],
              "env": [
                {
                  "name": "POD_NAME",
                  "valueFrom": {
                    "fieldRef": {
                      "apiVersion": "v1",
                      "fieldPath": "metadata.name"
                    }
                  }
                },
                {
                  "name": "POD_NAMESPACE",
                  "valueFrom": {
                    "fieldRef": {
                      "apiVersion": "v1",
                      "fieldPath": "metadata.namespace"
                    }
                  }
                }
              ],
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File",
              "imagePullPolicy": "IfNotPresent",
              "name": "prometheus-to-sd",
              "image": "gcr.io/google-containers/prometheus-to-sd:v0.2.3"
            }
          ],
          "serviceAccountName": "kube-dns",
          "tolerations": [
            {
              "key": "CriticalAddonsOnly",
              "operator": "Exists"
            }
          ],
          "schedulerName": "default-scheduler",
          "volumes": [
            {
              "name": "kube-dns-config",
              "configMap": {
                "name": "kube-dns",
                "defaultMode": 420,
                "optional": true
              }
            }
          ],
          "restartPolicy": "Always",
          "serviceAccount": "kube-dns",
          "priorityClassName": "system-cluster-critical",
          "dnsPolicy": "Default",
          "terminationGracePeriodSeconds": 30
        }
      },
      "response": {
        "code": 403,
        "@type": "core.k8s.io/v1.Status",
        "kind": "Status",
        "apiVersion": "v1",
        "metadata": {},
        "status": "Failure",
        "message": "pods \"kube-dns-548976df6c-f5gn4\" is forbidden: image policy webhook backend denied one or more images: Denied by default admission rule. Denied by Attestor. Image gcr.io/google-containers/prometheus-to-sd:v0.2.3 denied by projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor",
        "reason": "Forbidden",
        "details": {
          "name": "kube-dns-548976df6c-f5gn4",
          "kind": "pods"
        }
      }
    },
    "insertId": "ujcfwqentsny",
    "resource": {
      "type": "k8s_cluster",
      "labels": {
        "project_id": "binary-control-clsecteam",
        "cluster_name": "test-cluster",
        "location": "us-central1-a"
      }
    },
    "timestamp": "2019-01-16T18:40:22.051381Z",
    "severity": "ERROR",
    "labels": {
      "authorization.k8s.io/reason": "RBAC: allowed by ClusterRoleBinding \"system:controller:replicaset-controller\" of ClusterRole \"system:controller:replicaset-controller\" to ServiceAccount \"replicaset-controller/kube-system\"",
      "authorization.k8s.io/decision": "allow",
      "cluster_version": "1.11.2-gke.25"
    },
    "logName": "projects/binary-control-clsecteam/logs/cloudaudit.googleapis.com%2Factivity",
    "operation": {
      "id": "1159e3dd-b15f-4008-873f-d6a954f1601b",
      "producer": "k8s.io",
      "first": true,
      "last": true
    },
    "receiveTimestamp": "2019-01-16T18:40:30.219538007Z"
  }
}

function denyByDefaultRuleMultipleImagesByMultipleAttestors() {
  return {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "principalEmail": "system:serviceaccount:kube-system:replicaset-controller"
      },
      "authorizationInfo": [
        {
          "permission": "io.k8s.core.v1.pods.create",
          "resource": "core/v1/namespaces/default/pods"
        }
      ],
      "methodName": "io.k8s.core.v1.pods.create",
      "request": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "creationTimestamp": null,
          "generateName": "image-mixed-attestation-5947994cf8-",
          "labels": {
            "pod-template-hash": "1503550794",
            "run": "image-mixed-attestation"
          },
          "ownerReferences": [
            {
              "apiVersion": "apps/v1",
              "blockOwnerDeletion": true,
              "controller": true,
              "kind": "ReplicaSet",
              "name": "image-mixed-attestation-5947994cf8",
              "uid": "50af96e6-310b-11e9-b8fc-42010a8000d6"
            }
          ]
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-with-attestation",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            },
            {
              "image": "gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-without-attestation",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "terminationGracePeriodSeconds": 30
        },
        "status": {}
      },
      "requestMetadata": {
        "callerIp": "::1"
      },
      "resourceName": "core/v1/namespaces/default/pods",
      "response": {
        "@type": "core.k8s.io/v1.Status",
        "apiVersion": "v1",
        "code": 403,
        "details": {
          "kind": "pods",
          "name": "image-mixed-attestation-5947994cf8-wwsq6"
        },
        "kind": "Status",
        "message": "pods \"image-mixed-attestation-5947994cf8-wwsq6\" is forbidden: image policy webhook backend denied one or more images: Denied by default admission rule. Denied by Attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014 denied by projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor. Denied by default admission rule. Denied by Attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba denied by projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba denied by projects/binary-control-clsecteam/attestors/amandak-deployment: No attestations found that were valid and signed by a key trusted by the attestor",
        "metadata": {},
        "reason": "Forbidden",
        "status": "Failure"
      },
      "serviceName": "k8s.io",
      "status": {
        "code": 7,
        "message": "Forbidden"
      }
    },
    "insertId": "a12d0474-a94c-4eb4-8f10-144aecf3c43f",
    "resource": {
      "type": "k8s_cluster",
      "labels": {
        "project_id": "binary-control-clsecteam",
        "cluster_name": "test-cluster",
        "location": "us-central1-a"
      }
    },
    "timestamp": "2019-02-15T10:20:31.010329Z",
    "labels": {
      "authorization.k8s.io/reason": "RBAC: allowed by ClusterRoleBinding \"system:controller:replicaset-controller\" of ClusterRole \"system:controller:replicaset-controller\" to ServiceAccount \"replicaset-controller/kube-system\"",
      "authorization.k8s.io/decision": "allow"
    },
    "logName": "projects/binary-control-clsecteam/logs/cloudaudit.googleapis.com%2Factivity",
    "operation": {
      "id": "a12d0474-a94c-4eb4-8f10-144aecf3c43f",
      "producer": "k8s.io",
      "first": true,
      "last": true
    },
    "receiveTimestamp": "2019-02-15T10:20:35.848763389Z"
  }
}

function denyByClustereRuleDeployWithoutAttestors() {
  return {
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "principalEmail": "system:serviceaccount:kube-system:replicaset-controller"
      },
      "authorizationInfo": [
        {
          "permission": "io.k8s.core.v1.pods.create",
          "resource": "core/v1/namespaces/default/pods"
        }
      ],
      "methodName": "io.k8s.core.v1.pods.create",
      "request": {
        "@type": "core.k8s.io/v1.Pod",
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "creationTimestamp": null,
          "generateName": "image-mixed-attestation-5b9bb876b9-",
          "labels": {
            "pod-template-hash": "1656643265",
            "run": "image-mixed-attestation"
          },
          "ownerReferences": [
            {
              "apiVersion": "apps/v1",
              "blockOwnerDeletion": true,
              "controller": true,
              "kind": "ReplicaSet",
              "name": "image-mixed-attestation-5b9bb876b9",
              "uid": "ef186128-312c-11e9-b8fc-42010a8000d6"
            }
          ]
        },
        "spec": {
          "containers": [
            {
              "image": "gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-with-attestation",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            },
            {
              "image": "gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-without-attestation",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            },
            {
              "image": "gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4",
              "imagePullPolicy": "IfNotPresent",
              "name": "image-exempt-path",
              "resources": {},
              "terminationMessagePath": "/dev/termination-log",
              "terminationMessagePolicy": "File"
            }
          ],
          "dnsPolicy": "ClusterFirst",
          "restartPolicy": "Always",
          "schedulerName": "default-scheduler",
          "securityContext": {},
          "terminationGracePeriodSeconds": 30
        },
        "status": {}
      },
      "requestMetadata": {
        "callerIp": "::1"
      },
      "resourceName": "core/v1/namespaces/default/pods",
      "response": {
        "@type": "core.k8s.io/v1.Status",
        "apiVersion": "v1",
        "code": 403,
        "details": {
          "kind": "pods",
          "name": "image-mixed-attestation-5b9bb876b9-bx7rv"
        },
        "kind": "Status",
        "message": "pods \"image-mixed-attestation-5b9bb876b9-bx7rv\" is forbidden: image policy webhook backend denied one or more images: Denied by cluster admission rule for us-central1-a.test-cluster. Denied by Attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba denied by projects/binary-control-clsecteam/attestors/amandak-deployment: No attestations found that were valid and signed by a key trusted by the attestor",
        "metadata": {},
        "reason": "Forbidden",
        "status": "Failure"
      },
      "serviceName": "k8s.io",
      "status": {
        "code": 7,
        "message": "Forbidden"
      }
    },
    "insertId": "70dea306-5485-4d4c-83af-303886df4ec7",
    "resource": {
      "type": "k8s_cluster",
      "labels": {
        "project_id": "binary-control-clsecteam",
        "cluster_name": "test-cluster",
        "location": "us-central1-a"
      }
    },
    "timestamp": "2019-02-15T14:59:40.037234Z",
    "labels": {
      "authorization.k8s.io/reason": "RBAC: allowed by ClusterRoleBinding \"system:controller:replicaset-controller\" of ClusterRole \"system:controller:replicaset-controller\" to ServiceAccount \"replicaset-controller/kube-system\"",
      "authorization.k8s.io/decision": "allow"
    },
    "logName": "projects/binary-control-clsecteam/logs/cloudaudit.googleapis.com%2Factivity",
    "operation": {
      "id": "70dea306-5485-4d4c-83af-303886df4ec7",
      "producer": "k8s.io",
      "first": true,
      "last": true
    },
    "receiveTimestamp": "2019-02-15T15:00:21.157812798Z"
  }
}

module.exports.allowDeployAuthorizedImage = allowDeployAuthorizedImage;
module.exports.denyByDefaultRuleDeployUnauthorizedImage = denyByDefaultRuleDeployUnauthorizedImage;
module.exports.allowDeployWithBreakGlass = allowDeployWithBreakGlass;
module.exports.allowDeployWithBreakGlassNewFormat = allowDeployWithBreakGlassNewFormat;
module.exports.denyDeployWithAttestors = denyDeployWithAttestors;
module.exports.denyByDefaultRuleMultipleImagesByMultipleAttestors = denyByDefaultRuleMultipleImagesByMultipleAttestors;
module.exports.denyByClustereRuleDeployWithoutAttestors = denyByClustereRuleDeployWithoutAttestors;