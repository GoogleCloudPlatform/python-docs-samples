# Copyright 2015 Google Inc.
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
# limitations under the License

GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")
ZONE=$(shell gcloud config list compute/zone --format="value(compute.zone)")
CLUSTER_NAME=guestbook
COOL_DOWN=15
MIN=2
MAX=15
TARGET=50
RC=frontend

.PHONY: all
all: deploy

.PHONY: create-cluster
create-cluster:
	gcloud container clusters create guestbook \
		--scope "https://www.googleapis.com/auth/userinfo.email","cloud-platform" \
		--num-nodes=$(MIN)
	gcloud container clusters get-credentials guestbook

.PHONY: create-bucket
create-bucket:
	gsutil mb gs://$(GCLOUD_PROJECT)
	gsutil defacl set public-read gs://$(GCLOUD_PROJECT)

.PHONY: template
template:
	sed -i ".tmpl" "s/\$$GCLOUD_PROJECT/$(GCLOUD_PROJECT)/g" kubernetes_configs/postgres.yaml
	sed -i ".tmpl" "s/\$$GCLOUD_PROJECT/$(GCLOUD_PROJECT)/g" kubernetes_configs/frontend.yaml
	sed -i ".tmpl" "s/\$$GCLOUD_PROJECT/$(GCLOUD_PROJECT)/g" kubernetes_configs/load_tester.yaml

.PHONY: deploy
deploy: push template
	kubectl create -f kubernetes_config/frontend.yaml

.PHONY: update
update:
	kubectl rolling-update guestbook --image=gcr.io/${GCLOUD_PROJECT}/guestbook

.PHONY: disk
disk:
	gcloud compute disks create pg-data  --size 500GB

.PHONY: firewall
firewall:
	gcloud compute firewall-rules create kubepostgres --allow tcp:30061

.PHONY: autoscale-on
autoscale-on:
	AUTOSCALE_GROUP=$(shell gcloud container clusters describe $(CLUSTER_NAME) --zone $(ZONE) --format yaml | grep -A 1 instanceGroupUrls | awk -F/ 'FNR ==2 {print $$NF}')
	gcloud compute instance-groups managed set-autoscaling $(AUTOSCALE_GROUP) \
	  --cool-down-period $(COOL_DOWN) \
	  --max-num-replicas $(MAX) \
	  --min-num-replicas $(MIN) \
	  --scale-based-on-cpu --target-cpu-utilization $(shell echo "scale=2; $(TARGET)/100" | bc)
	kubectl autoscale rc $(RC) --min=$(MIN) --max=$(MAX) --cpu-percent=$(TARGET)

.PHONY: db-setup
db-setup:
	POSTGRES_POD_NAME=$(shell kubectl get pods | grep postgres | awk '{print $$1}')
	kubectl exec $(POSTGRES_POD_NAME) -- /init_db.sh

.PHONY: migrations
migrations:
	FRONTEND_POD_NAME=$(shell kubectl get pods | grep frontend -m 1 | awk '{print $$1}' )
	kubectl exec $(FRONTEND_POD_NAME) -- python /app/manage.py migrate


.PHONY: delete
delete:
	gcloud container clusters delete guestbook
	gcloud compute disks delete pg-data
