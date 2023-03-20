# Copyright 2022 Google LLC
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

# [START firestore_query_composite_filter_or]
from google.cloud import firestore

def query_or_composite_filter(project_id : str,
                              collection_name: str,
                              field_1_name: str,
                              field_1_value: str,
                              field_2_name: str,
                              field_2_value: str) -> None:
    
    # Instantiate the Firestore client
    client = firestore.Client(project=project_id)
    col_ref = client.collection(collection_name)

    query_1 = col_ref.where(field_1_name, '==', field_1_value)
    query_2 = col_ref.where(field_2_name, '==', field_2_value)
    

    

# [END firestore_query_composite_filter_or]
