#!/usr/bin/env python
# # Copyright 2022 Google LLC
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

import abc
from google.cloud import aiplatform
from typing import Any
from proto.datetime_helpers import DatetimeWithNanoseconds
from google.cloud.aiplatform import base

# If a resource was updated within this number of seconds, do not delete.
RESOURCE_UPDATE_BUFFER_IN_SECONDS = 60 * 60 * 8


class ResourceCleanupManager(abc.ABC):
    @property
    @abc.abstractmethod
    def type_name(str) -> str:
        pass

    @abc.abstractmethod
    def list(self) -> Any:
        pass

    @abc.abstractmethod
    def resource_name(self, resource: Any) -> str:
        pass

    @abc.abstractmethod
    def delete(self, resource: Any):
        pass

    @abc.abstractmethod
    def get_seconds_since_modification(self, resource: Any) -> float:
        pass

    def is_deletable(self, resource: Any) -> bool:
        time_difference = self.get_seconds_since_modification(resource)

        if self.resource_name(resource).startswith("perm"):
            print(f"Skipping '{resource}' due to name starting with 'perm'.")
            return False

        # Check that it wasn't created too recently, to prevent race conditions
        if time_difference <= RESOURCE_UPDATE_BUFFER_IN_SECONDS:
            print(
                f"Skipping '{resource}' due update_time being '{time_difference}', which is less than '{RESOURCE_UPDATE_BUFFER_IN_SECONDS}'."
            )
            return False

        return True


class VertexAIResourceCleanupManager(ResourceCleanupManager):
    @property
    @abc.abstractmethod
    def vertex_ai_resource(self) -> base.VertexAiResourceNounWithFutureManager:
        pass

    @property
    def type_name(self) -> str:
        return self.vertex_ai_resource._resource_noun

    def list(self) -> Any:
        return self.vertex_ai_resource.list()

    def resource_name(self, resource: Any) -> str:
        return resource.display_name

    def delete(self, resource):
        resource.delete()

    def get_seconds_since_modification(self, resource: Any) -> bool:
        update_time = resource.update_time
        current_time = DatetimeWithNanoseconds.now(tz=update_time.tzinfo)
        return (current_time - update_time).total_seconds()


class DatasetResourceCleanupManager(VertexAIResourceCleanupManager):
    vertex_ai_resource = aiplatform.datasets._Dataset


class EndpointResourceCleanupManager(VertexAIResourceCleanupManager):
    vertex_ai_resource = aiplatform.Endpoint

    def delete(self, resource):
        resource.delete(force=True)


class ModelResourceCleanupManager(VertexAIResourceCleanupManager):
    vertex_ai_resource = aiplatform.Model
