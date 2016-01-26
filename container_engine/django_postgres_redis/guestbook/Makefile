GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/guestbook .

.PHONY: push
push: build
	gcloud docker push gcr.io/$(GCLOUD_PROJECT)/guestbook

.PHONY: delete
delete:
	kubectl delete rc guestbook
	kubectl delete service guestbook
