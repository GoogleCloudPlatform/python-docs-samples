
all: build

PREFIX = gcr.io/ziwei-trace-demo-app
IMAGE_NAME = cloud-trace-demo
TAG = latest

container:
	sudo docker build --pull --tag ${PREFIX}/${IMAGE_NAME}:${TAG} ./app

push: container
	sudo gcloud docker -- push ${PREFIX}/${IMAGE_NAME}:${TAG}