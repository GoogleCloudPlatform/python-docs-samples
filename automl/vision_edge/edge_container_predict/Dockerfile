# Copyright 2019 Google LLC
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

ARG TF_SERVING_IMAGE_TAG
FROM tensorflow/serving:${TF_SERVING_IMAGE_TAG}

ENV GCS_READ_CACHE_MAX_STALENESS 300
ENV GCS_STAT_CACHE_MAX_AGE 300
ENV GCS_MATCHING_PATHS_CACHE_MAX_AGE 300

EXPOSE 8500
EXPOSE 8501
ENTRYPOINT /usr/bin/tensorflow_model_server \
              --port=8500 \
              --rest_api_port=8501 \
              --model_base_path=/tmp/mounted_model/ \
              --tensorflow_session_parallelism=0 \
              --file_system_poll_wait_seconds=31540000
