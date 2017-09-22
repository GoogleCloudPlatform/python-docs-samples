#!/bin/python
# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Examples of using the Cloud ML Engine's online prediction service."""
import argparse
import base64
import json

# [START import_libraries]
import googleapiclient.discovery
# [END import_libraries]
import six


# [START predict_json]
def predict_json(project, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    service = googleapiclient.discovery.build('ml', 'v1')
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
def predict_examples(project,
                     model,
                     example_bytes_list,
                     version=None):
    """Send protocol buffer data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        example_bytes_list ([str]): A list of bytestrings representing
            serialized tf.train.Example protocol buffers. The contents of this
            protocol buffer will change depending on the signature of your
            deployed model.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    service = googleapiclient.discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': [
            {'b64': base64.b64encode(example_bytes).decode('utf-8')}
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
    See: https://cloud.google.com/ml-engine/docs/concepts/prediction-overview
    for details.

    Args:
        json_instance (Mapping[str: Any]): Keys should be the names of Tensors
            your deployed model expects to parse using it's tf.FeatureSpec.
            Values should be datatypes convertible to Tensors, or (potentially
            nested) lists of datatypes convertible to tensors.
    Returns:
        str: A string as a container for the serialized bytes of
            tf.train.Example protocol buffer.
    """
    import tensorflow as tf
    feature_dict = {}
    for key, data in six.iteritems(json_instance):
        if isinstance(data, six.string_types):
            feature_dict[key] = tf.train.Feature(
                bytes_list=tf.train.BytesList(value=[data.encode('utf-8')]))
        elif isinstance(data, float):
            feature_dict[key] = tf.train.Feature(
                float_list=tf.train.FloatList(value=[data]))
        elif isinstance(data, int):
            feature_dict[key] = tf.train.Feature(
                int64_list=tf.train.Int64List(value=[data]))
    return tf.train.Example(
        features=tf.train.Features(
            feature=feature_dict
        )
    ).SerializeToString()
# [END census_to_example_bytes]


def main(project, model, version=None, force_tfrecord=False):
    """Send user input to the prediction service."""
    while True:
        try:
            user_input = json.loads(raw_input("Valid JSON >>>"))
        except KeyboardInterrupt:
            return

        if not isinstance(user_input, list):
            user_input = [user_input]
        try:
            if force_tfrecord:
                example_bytes_list = [
                    census_to_example_bytes(e)
                    for e in user_input
                ]
                result = predict_examples(
                    project, model, example_bytes_list, version=version)
            else:
                result = predict_json(
                    project, model, user_input, version=version)
        except RuntimeError as err:
            print(str(err))
        else:
            print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
    main(
        args.project,
        args.model,
        version=args.version,
        force_tfrecord=args.force_tfrecord
    )
