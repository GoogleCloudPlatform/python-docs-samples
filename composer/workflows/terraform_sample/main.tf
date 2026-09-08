# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

variable "project_id" {
  type        = string
  description = "Google Cloud Project ID"
}

variable "bucket_name_prefix" {
  type        = string
  default     = "composer-tf-sample"
  description = "Prefix for the created GCS bucket name"
}

variable "location" {
  type        = string
  default     = "US"
  description = "Google Cloud Storage bucket location"
}

provider "google" {
  project = var.project_id
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "sample_bucket" {
  name                        = "${var.bucket_name_prefix}-${random_id.bucket_suffix.hex}"
  location                    = var.location
  project                     = var.project_id
  force_destroy               = true
  uniform_bucket_level_access = true

  labels = {
    managed_by = "composer_terraform_operator"
  }
}

output "bucket_name" {
  value       = google_storage_bucket.sample_bucket.name
  description = "Name of the created Cloud Storage bucket"
}
