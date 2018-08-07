# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example DAG demonstrating Kubernetes Pod Operator."""

# [START composer_kubernetespodoperator]
import datetime

from airflow import models
# [END composer_kubernetespodoperator]
from airflow.contrib.kubernetes import pod
from airflow.contrib.kubernetes import secret
# [START composer_kubernetespodoperator]
from airflow.contrib.operators import kubernetes_pod_operator

# [END composer_kubernetespodoperator]

# A Secret is an object that contains a small amount of sensitive data such as
# a password, a token, or a key. Such information might otherwise be put in a
# Pod specification or in an image; putting it in a Secret object allows for
# more control over how it is used, and reduces the risk of accidental
# exposure.
secret_file = secret.Secret(
    # Mounts the secret as a file in RAM-backed tmpfs.
    deploy_type='volume',
    # File path of where to deploy the target, since deploy_type is 'volume'
    # rather than 'env'.
    deploy_target='/etc/sql_conn',
    # Name of secret in Kubernetes, if the secret is not already defined in
    # Kubernetes using kubectl the Pod will fail to find the secret, and in
    # turn, fail to launch.
    secret='airflow-secrets',
    # Key of the secret within Kubernetes.
    key='sql_alchemy_conn')

secret_env = secret.Secret(
    # Expose the secret as environment variable.
    deploy_type='env',
    # The name of the environment variable, since deploy_type is `env` rather
    # than `volume`.
    deploy_target='SQL_CONN',
    secret='airflow-secrets',
    key='sql_alchemy_conn')

# [START composer_kubernetespodoperator]
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

# If a Pod fails to launch, or has an error occur in the container, Airflow
# will show the task as failed, as well as contain all of the task logs
# required to debug.
with models.DAG(
        dag_id='composer_sample_kubernetes_pod',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:
    # Only name, namespace, image, and task_id are required to create a
    # KubernetesPodOperator. In Cloud Composer, currently the operator defaults
    # to using the config file found at `/home/airflow/composer_kube_config if
    # no `config_file` parameter is specified. By default it will contain the
    # credentials for Cloud Composer's Google Kubernetes Engine cluster that is
    # created upon environment creation.
    kubernetes_min_pod = kubernetes_pod_operator.KubernetesPodOperator(
        # The ID specified for the task.
        task_id='pod-ex-minimum',
        # Name of task you want to run, used to generate Pod ID.
        name='pod-ex-minimum',
        # The namespace to run within Kubernetes, default namespace is
        # `default`. There is the potential for the resource starvation of
        # Airflow workers and scheduler within the Cloud Composer environment,
        # the recommended solution is to increase the amount of nodes in order
        # to satisfy the computing requirements. Alternatively, launching pods
        # into a custom namespace will stop fighting over resources.
        namespace='default',
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images.
        image='gcr.io/gcp-runtimes/ubuntu_16_0_4')
    # [END composer_kubernetespodoperator]

    kubenetes_template_ex = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-kube-templates',
        name='ex-kube-templates',
        namespace='default',
        image='bash',
        # All parameters below are able to be templated with jinja -- cmds,
        # arguments, env_vars, and config_file. For more information visit:
        # https://airflow.apache.org/code.html#default-variables

        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=['echo'],
        # DS in jinja is the execution date as YYYY-MM-DD, this docker image
        # will echo the execution date. Arguments to the entrypoint. The docker
        # image's CMD is used if this is not provided. The arguments parameter
        # is templated.
        arguments=['{{ ds }}'],
        # The var template variable allows you to access variables defined in
        # Airflow UI. In this case we are getting the value of my_value and
        # setting the environment variable `MY_VALUE`. The pod will fail if
        # `my_value` is not set in the Airflow UI.
        env_vars={'MY_VALUE': '{{ var.value.my_value }}'},
        # Sets the config file to the specified airflow.cfg airflow home. If
        # the configuration file does not exist or does not provide valid
        # credentials the pod will fail to launch.
        config_file="{{ conf.get('core', 'airflow_home') }}/config")

    kubernetes_secret_vars_ex = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-kube-secrets',
        name='ex-kube-secrets',
        namespace='default',
        image='ubuntu',
        # The secrets to pass to Pod, the Pod will fail to create if the
        # secrets you specify in a Secret object do not exist in Kubernetes.
        secrets=[secret_env, secret_file],
        # env_vars allows you to specify environment variables for your
        # container to use. env_vars is templated.
        env_vars={'EXAMPLE_VAR': '/example/value'})

    # [START composer_kubernetespodaffinity]
    kubernetes_affinity_ex = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-pod-affinity',
        name='ex-pod-affinity',
        namespace='default',
        image='perl',
        cmds=['perl'],
        arguments=['-Mbignum=bpi', '-wle', 'print bpi(2000)'],
        # affinity allows you to constrain which nodes your pod is eligible to
        # be scheduled on, based on labels on the node. In this case, if the
        # label 'cloud.google.com/gke-nodepool' with value
        # 'nodepool-label-value' or 'nodepool-label-value2' is not found on any
        # nodes, it will fail to schedule.
        affinity={
            'nodeAffinity': {
                # requiredDuringSchedulingIgnoredDuringExecution means in order
                # for a pod to be scheduled on a node, the node must have the
                # specified labels. However, if labels on a node change at
                # runtime such that the affinity rules on a pod are no longer
                # met, the pod will still continue to run on the node.
                'requiredDuringSchedulingIgnoredDuringExecution': {
                    'nodeSelectorTerms': [{
                        'matchExpressions': [{
                            # When nodepools are created in Google Kubernetes
                            # Engine, the nodes inside of that nodepool are
                            # automatically assigned the label
                            # 'cloud.google.com/gke-nodepool' with the value of
                            # the nodepool's name.
                            'key': 'cloud.google.com/gke-nodepool',
                            'operator': 'In',
                            # The label key's value that pods can be scheduled
                            # on.
                            'values': [
                                'node-pool-name-1',
                                'node-pool-name-2',
                            ]
                        }]
                    }]
                }
            }
        })
    # [END composer_kubernetespodaffinity]

    kubernetes_full_pod = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-all-configs',
        name='pi',
        namespace='default',
        image='perl',
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=['perl'],
        # Arguments to the entrypoint. The docker image's CMD is used if this
        # is not provided. The arguments parameter is templated.
        arguments=['-Mbignum=bpi', '-wle', 'print bpi(2000)'],
        # The secrets to pass to Pod, the Pod will fail to create if the
        # secrets you specify in a Secret object do not exist in Kubernetes.
        secrets=[],
        # Labels to apply to the Pod.
        labels={'pod-label': 'label-name'},
        # Timeout to start up the Pod, default is 120.
        startup_timeout_seconds=120,
        # The environment variables to be initialized in the container
        # env_vars are templated.
        env_vars={'EXAMPLE_VAR': '/example/value'},
        # If true, logs stdout output of container. Defaults to True.
        get_logs=True,
        # Determines when to pull a fresh image, if 'IfNotPresent' will cause
        # the Kubelet to skip pulling an image if it already exists. If you
        # want to always pull a new image, set it to 'Always'.
        image_pull_policy='Always',
        # Annotations are non-identifying metadata you can attach to the Pod.
        # Can be a large range of data, and can include characters that are not
        # permitted by labels.
        annotations={'key1': 'value1'},
        # Resource specifications for Pod, this will allow you to set both cpu
        # and memory limits and requirements.
        resources=pod.Resources(),
        # Specifies path to kubernetes config. If no config is specified will
        # default to '~/.kube/config'. The config_file is templated.
        config_file='/home/airflow/composer_kube_config',
        # If true, the content of /airflow/xcom/return.json from container will
        # also be pushed to an XCom when the container ends.
        xcom_push=False,
        # List of Volume objects to pass to the Pod.
        volumes=[],
        # List of VolumeMount objects to pass to the Pod.
        volume_mounts=[],
        # Affinity determines which nodes the Pod can run on based on the
        # config. For more information see:
        # https://kubernetes.io/docs/concepts/configuration/assign-pod-node/
        affinity={})
