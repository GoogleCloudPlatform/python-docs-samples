# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def delete_context_caches(cache_name: str) -> str:
    # [START googlegenaisdk_contentcache_delete]
    from google import genai

    client = genai.Client()
    # Delete content cache using name
    # E.g cache_name = 'projects/111111111111/locations/us-central1/cachedContents/1111111111111111111'
    client.caches.delete(name=cache_name)
    print("Deleted Cache", cache_name)
    # Example response
    #   Deleted Cache projects/111111111111/locations/us-central1/cachedContents/1111111111111111111
    # [END googlegenaisdk_contentcache_delete]
    return cache_name


if __name__ == "__main__":
    cache_name = input("Cache Name: ")
    delete_context_caches(cache_name)
