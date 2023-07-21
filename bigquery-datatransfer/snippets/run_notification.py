# Copyright 2021 Google LLC
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


def run_notification(transfer_config_name, pubsub_topic):
    orig_transfer_config_name = transfer_config_name
    orig_pubsub_topic = pubsub_topic
    # [START bigquerydatatransfer_run_notification]
    transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
    pubsub_topic = "projects/PROJECT-ID/topics/TOPIC-ID"
    # [END bigquerydatatransfer_run_notification]
    transfer_config_name = orig_transfer_config_name
    pubsub_topic = orig_pubsub_topic

    # [START bigquerydatatransfer_run_notification]
    from google.cloud import bigquery_datatransfer
    from google.protobuf import field_mask_pb2

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    transfer_config = bigquery_datatransfer.TransferConfig(name=transfer_config_name)
    transfer_config.notification_pubsub_topic = pubsub_topic
    update_mask = field_mask_pb2.FieldMask(paths=["notification_pubsub_topic"])

    transfer_config = transfer_client.update_transfer_config(
        {"transfer_config": transfer_config, "update_mask": update_mask}
    )

    print(f"Updated config: '{transfer_config.name}'")
    print(f"Notification Pub/Sub topic: '{transfer_config.notification_pubsub_topic}'")
    # [END bigquerydatatransfer_run_notification]
    # Return the config name for testing purposes, so that it can be deleted.
    return transfer_config
