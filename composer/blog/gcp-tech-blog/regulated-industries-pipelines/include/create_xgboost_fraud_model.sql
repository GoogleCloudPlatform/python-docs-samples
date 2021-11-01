/*

# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

This query create the BQML XGBoost Boosted Tree Classifier Model, with the input label 'Class' - this is either 0 or 1 - 1 if it is a fraudulent transaction and 0 if it is not

*/


CREATE OR REPLACE MODEL
  `rp_demo_cmek.ulb_xgboost_fraud_classifier_model` OPTIONS(MODEL_TYPE='BOOSTED_TREE_CLASSIFIER',
    BOOSTER_TYPE='GBTREE',
    NUM_PARALLEL_TREE=1,
    MAX_ITERATIONS=50,
    TREE_METHOD='AUTO',
    EARLY_STOP=FALSE,
    SUBSAMPLE=1,
    INPUT_LABEL_COLS=['Class']) AS
SELECT
  *
FROM
  `rp_demo_cmek.ulb_fraud_training_sample_table`