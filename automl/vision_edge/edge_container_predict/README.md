# AutoML Vision Edge Container Prediction

This is an example to show how to predict with AutoML Vision Edge Containers.
The test (automl_vision_edge_container_predict_test.py) shows an automatical way
to run the prediction.

If you want to try the test manually with a sample model, please install
[gsutil tools](https://cloud.google.com/storage/docs/gsutil_install) and
[Docker CE](https://docs.docker.com/install/) first, and then follow the steps
below. All the following instructions with commands assume you are in this
folder with system variables as

```bash
$ CONTAINER_NAME=AutomlVisionEdgeContainerPredict
$ PORT=8505
```

+   Step 1. Pull the Docker image.

```bash
# This is a CPU TFServing 1.14.0 with some default settings compiled from
# https://hub.docker.com/r/tensorflow/serving.
$ DOCKER_GCS_DIR=gcr.io/cloud-devrel-public-resources
$ CPU_DOCKER_GCS_PATH=${DOCKER_GCS_DIR}/gcloud-container-1.14.0:latest
$ sudo docker pull ${CPU_DOCKER_GCS_PATH}
```

+   Step 2. Get a sample saved model.

```bash
$ MODEL_GCS_DIR=gs://cloud-samples-data/vision/edge_container_predict
$ SAMPLE_SAVED_MODEL=${MODEL_GCS_DIR}/saved_model.pb
$ mkdir model_path
$ YOUR_MODEL_PATH=$(realpath model_path)
$ gsutil -m cp ${SAMPLE_SAVED_MODEL} ${YOUR_MODEL_PATH}
```

+   Step 3. Run the Docker container.

```bash
$ sudo docker run --rm --name ${CONTAINER_NAME} -p ${PORT}:8501 -v \
    ${YOUR_MODEL_PATH}:/tmp/mounted_model/0001 -t ${CPU_DOCKER_GCS_PATH}
```

+   Step 4. Send a prediction request.

```bash
$ python automl_vision_edge_container_predict.py --image_file_path=./test.jpg \
    --image_key=1 --port_number=${PORT}
```

The outputs are

```
{
    'predictions':
    [
        {
            'scores': [0.0914393, 0.458942, 0.027604, 0.386767, 0.0352474],
            labels': ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips'],
            'key': '1'
        }
    ]
}
```

+   Step 5. Stop the container.

```bash
sudo docker stop ${CONTAINER_NAME}
```

Note: The docker image is uploaded with the following command.

```bash
gcloud builds --project=cloud-devrel-public-resources \
  submit --config cloudbuild.yaml
```
