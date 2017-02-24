# Copyright 2016 Google Inc. All Rights Reserved. Licensed under the Apache
# License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Examples of using the Cloud ML Engine's online prediction service."""

# [START import_libraries]
import googleapiclient.discovery
# [END import_libraries]


# [START authenticating]
def get_ml_engine_service():
    return googleapiclient.discovery.build('ml', 'v1beta1')
# [END authenticating]


# [START predict_json]
def predict_json(project, model, instances, version=None):
    """Send data instances to a deployed model for prediction
    Args:
        project: str, project where the Cloud ML Engine Model is deployed.
        model: str, model name.
        instances: [dict], dictionaries from string keys defined by the model
        to data.
        version: [optional] str, version of the model to target.
    Returns:
        A dictionary of prediction results defined by the model.
    """
    service = get_ml_engine_service()
    name = 'projects/{}/models/{}'.format(project, model)
    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']
# [END predict_json]


# [START predict_tf_records]
def predict_tf_records(project,
                       model,
                       example_bytes_list,
                       key='tfrecord',
                       version=None):
    """Send data instances to a deployed model for prediction
    Args:
        project: str, project where the Cloud ML Engine Model is deployed
        model: str, model name.
        example_bytes_list: [str], Serialized tf.train.Example protos.
        version: str, version of the model to target.
    Returns:
        A dictionary of prediction results defined by the model.
    """
    import base64
    service = get_ml_engine_service()
    name = 'projects/{}/models/{}'.format(project, model)
    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': [
            {key: {'b64': base64.b64encode(example_bytes)}}
            for example_bytes in example_bytes_list
        ]}
    ).execute()
    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']
# [END predict_tf_records]


# [START census_to_example_bytes]
def census_to_example_bytes(json_instance):
    """Serialize a JSON example to the bytes of a tf.train.Example.
    This method is specific to the signature of the Census example.
    Args:
        json_instance: dict, representing data to be serialized.
    Returns:
        A string (as a container for bytes).
    """
    import tensorflow as tf
    feature_dict = {}
    for key, data in json_instance.iteritems():
        if isinstance(data, str) or isinstance(data, unicode):
            feature_dict[key] = tf.train.Feature(
                bytes_list=tf.train.BytesList(value=[str(data)]))
        elif isinstance(data, int) or isinstance(data, float):
            feature_dict[key] = tf.train.Feature(
                float_list=tf.train.FloatList(value=[data]))
    return tf.train.Example(
        features=tf.train.Features(
            feature=feature_dict
        )
    ).SerializeToString()
# [END census_to_example_bytes]


# [START predict_from_files]
def predict_from_files(project,
                       model,
                       files,
                       version=None,
                       force_tfrecord=False):
    import json
    import itertools
    instances = (json.loads(line)
                 for f in files
                 for line in f.readlines())

    # Requests to online prediction
    # can have at most 100 instances
    args = [instances] * 100
    instance_batches = itertools.izip(*args)

    results = []
    for batch in instance_batches:
        if force_tfrecord:
            example_bytes_list = [
                census_to_example_bytes(instance)
                for instance in batch
            ]
            results.append(predict_tf_records(
                project,
                model,
                example_bytes_list,
                version=version
            ))
        else:
            results.append(predict_json(
                project,
                model,
                batch,
                version=version
            ))
    return results
# [END predict_from_files]


if __name__ == '__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_files',
        help='File paths with examples to predict',
        nargs='+',
        type=os.path.abspath
    )
    parser.add_argument(
        '--project',
        help='Project in which the model is deployed',
        type=str,
        required=True
    )
    parser.add_argument(
        '--model',
        help='Model name',
        type=str,
        required=True
    )
    parser.add_argument(
        '--version',
        help='Name of the version.',
        type=str
    )
    parser.add_argument(
        '--force-tfrecord',
        help='Send predictions as TFRecords rather than raw JSON',
        action='store_true',
        default=False
    )
    args = parser.parse_args()
    predict_from_files(**args.__dict__)
