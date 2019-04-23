# AutoML Vision Edge Container Prediction

This is an example to show how to predict with AutoML Vision Edge Containers.
The test (freeze_meta_graph_lib_test.py) shows an automatical way to run the
prediction.

If you want to try the test manually with a sample model, please install
[gsutil tools](https://cloud.google.com/storage/docs/gsutil_install) and
[Docker CE](https://docs.docker.com/install/) first, and then follow the steps
below. All the following instructions with commands assume you are in this
folder.

+   Step 1. Pull the Docker image.

```bash
$ CPU_DOCKER_GCS_PATH=gcr.io/automl-vision-ondevice/gcloud-container-1.12.0:latest
$ sudo docker pull ${CPU_DOCKER_GCS_PATH}
```

+   Step 2. Get a sample saved model.

```bash
$ SAMPLE_SAVED_MODEL=gs://cloud-samples-data/vision/edge_container_predict/saved_model.pb
$ mkdir model_path
$ YOUR_MODEL_PATH=$(realpath model_path)
$ gsutil -m cp ${SAMPLE_SAVED_MODEL} ${YOUR_MODEL_PATH}
```

+   Step 3. Run the Docker container.

```bash
$ CONTAINER_NAME=AutomlVisionEdgeContainerPredict
$ PORT=8501
$ sudo docker run --rm --name ${CONTAINER_NAME} -p ${PORT}:8501 -v ${YOUR_MODEL_PATH}:/tmp/mounted_model/0001 -t ${CPU_DOCKER_GCS_PATH}
```

+   Step 4. Send a prediction request.

```bash
$ # The port number should be the same when you run the docker container above.
$ PORT=8501
$ python automl_vision_edge_container_predict.py --image_file_path=./test.jpg --image_key=1 --port_number=${PORT}
```

+   Step 5. Stop the container.

```bash
$ # The container name should be the same when you run the docker container above.
sudo docker stop ${CONTAINER_NAME}
```
