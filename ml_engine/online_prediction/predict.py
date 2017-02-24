import argparse
import json
# [START import_libraries]
import googleapiclient.discovery
# [END import_libraries]

# [START authenticating]
def get_ml_engine_service():
    return googleapiclient.discovery.build_from_document(
        json.load(open('staging_ml.json')))
# [END authenticating]

# [START predict_json]
def predict_json(project, model, instances, version=None):
    """Send data instances to a deployed model for prediction
    Args:
        project: str, project where the Cloud ML Engine Model is deployed
        model: str, model name
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
        body={"instances": instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']
# [END predict_json]

# [START predict_tf_records]
def predict_tf_records(project, model, example_bytes_list, key='tfrecord', version=None):
    """Send data instances to a deployed model for prediction
    Args:
        project: str, project where the Cloud ML Engine Model is deployed
        model: str, model name
        feature_dict_list: [dict], dictionaries from string keys to
          tf.train.Feature protos.
        version: [optional] str, version of the model to target.
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
        body={"instances": [
            {key: {'b64': base64.b64encode(example_bytes)}}
            for example_bytes in example_bytes_list
        ]}
    ).execute()
    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def census_to_example_bytes(json_instance):
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
# [END predict_tf_records]

if __name__=='__main__':
    import sys
    import base64
    import json
    with open(sys.argv[1]) as f:
        instances = [json.loads(line) for line in f.readlines()]

    with open(sys.argv[2], 'w') as f:
        for instance in instances:
            f.write(json.dumps(
                {'tfrecord': {'b64': base64.b64encode(
                    census_to_example_string(instance)
                )}}))
