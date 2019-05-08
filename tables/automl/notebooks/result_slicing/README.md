Copyright 2019 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

### Summary: Use open source tools to slice and analyze a classification model built in AutoML Tables


# Result Slicing with a model built in AutoML Tables


AutoML Tables enables you to build machine learning models based on tables of your own data and host them on Google Cloud for scalability. This solution demonstrates how you can use open source tools to analyze a classification model's output by slicing the results to understand performance discrepancies. This should serve as an introduction to a couple of tools that make in-depth model analysis simpler for AutoML Tables users. 

Our exercise will

1. Preprocess the output data
2. Examine the dataset in the What-If Tool
3. Use TFMA to slice the data for analysis


## Problem Description

Top-level metrics don't always tell the whole story of how a model is performing. Sometimes, specific characteristics of the data may make certain subclasses of the dataset harder to predict accurately. This notebook will give some examples of how to use open source tools to slice data results from an AutoML Tables classification model, and discover potential performance discrepancies.


## Data Preprocessing

### Prerequisite

To perform this exercise, you need to have a GCP (Google Cloud Platform) account. If you don't have a GCP account, see [Create a GCP project](https://cloud.google.com/resource-manager/docs/creating-managing-projects). If you'd like to try analyzing your own model, you also need to have already built a model in AutoML Tables and exported its results to BigQuery.

### Data

The data we use in this exercise is a public dataset, the [Default of Credit Card Clients](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients) dataset, for analysis. This dataset was collected to help compare different methods of predicting credit card default. Using this colab to analyze your own dataset may require a little adaptation, but should be possible. The data was already used in AutoML Tables to train a binary classifier which attempts to predict whether or not the customer will default in the following month.

If you'd like to try using your own data in this notebook, you'll need to [train an AutoML Tables model](https://cloud.google.com/automl-tables/docs/beginners-guide) and export the results to BigQuery using the link on the Evaluate tab. Once the BigQuery table is finished exporting, you can copy the Table ID from GCP console into the notebook's "table_name" parameter to import it. There are several other parameters you'll need to update, such as sampling rates and field names.

### Format for Analysis

Many of the tools we use to analyze models and data expect to find their inputs in the [tensorflow.Example](https://www.tensorflow.org/tutorials/load_data/tf_records) format. In the Colab, we'll show code to preprocess our data into tf.Examples, and also extract the predicted class from our classifier, which is binary.


## What-If Tool

The [What-If Tool](https://pair-code.github.io/what-if-tool/) is a powerful visual interface to explore data, models, and predictions. Because we're reading our results from BigQuery, we aren't able to use the features of the What-If Tool that query the model directly. But we can still use many of its other features to explore our data distribution in depth.

## Tensorflow Model Analysis

This section of the tutorial will use [TFMA](https://github.com/tensorflow/model-analysis) model agnostic analysis capabilities.

TFMA generates sliced metrics graphs and confusion matrices. We can use these to dig deeper into the question of how well this model performs on different classes of inputs, using the given dataset as a motivating example.

