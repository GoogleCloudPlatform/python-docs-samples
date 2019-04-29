#!/bin/python
# Copyright 2019 Google Inc. All Rights Reserved.
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

# [START import_libraries]
from kfp import compiler
import kfp.dsl as dsl
import kfp.components as comp
# [END import_libraries]

# [START load_component_url]
scikit_learn_train = comp.load_component_from_url('[COMPONENT_URL_FROM_AI_HUB]')
# [END load_component_url]

# [START create_pipeline]
# Use the @dsl.pipeline decorator to add a name and description to your pipeline definition.
@dsl.pipeline(
    name='scikit-learn Trainer',
    description='Trains a scikit-learn model')
# Use a function to define the pipeline.
def scikit_learn_trainer(
    training_data_path='gs://cloud-samples-data/ml-engine/iris/classification/train.csv',
    test_data_path='gs://cloud-samples-data/ml-engine/iris/classification/evaluate.csv',
    output_dir='/tmp',
    estimator_name='GradientBoostingClassifier',
    hyperparameters='n_estimators 100 max_depth 4'):

    # Use the component you loaded in the previous step to create a pipeline operation.
    sklearn_op = scikit_learn_train(training_data_path, test_data_path, output_dir,
                                    estimator_name, hyperparameters)
# [END create_pipeline]

# [START compile_pipeline]
compiler.Compiler().compile(scikit_learn_trainer, '[PATH_TO_YOUR_NEW_PIPELINE]')
# [END compile_pipeline]