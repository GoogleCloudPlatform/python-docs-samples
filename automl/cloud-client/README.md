# AutoML Samples

<a href="https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=automl/cloud-client/README.md">
<img alt="Open in Cloud Shell" src ="http://gstatic.com/cloudssh/images/open-btn.png"></a>


This directory contains samples for the [Google Cloud AutoML APIs](https://cloud.google.com/automl/) - [docs](https://cloud.google.com/automl/docs/)

We highly recommend that you refer to the official documentation pages:
* AutoML Natural Language
  * [Classification](https://cloud.google.com/natural-language/automl/docs)
  * [Entity Extraction](https://cloud.google.com/natural-language/automl/entity-analysis/docs)
  * [Sentiment Analysis](https://cloud.google.com/natural-language/automl/sentiment/docs)
* [AutoML Translation](https://cloud.google.com/translate/automl/docs)
* AutoML Vision
  * [Classification](https://cloud.google.com/vision/automl/docs)
  * [Object Detection](https://cloud.google.com/vision/automl/object-detection/docs)

This API is part of the larger collection of Cloud Machine Learning APIs.

These Python samples demonstrate how to access the Cloud AutoML API
using the [Google Cloud Client Library for Python][google-cloud-python].

[google-cloud-python]: https://github.com/GoogleCloudPlatform/google-cloud-python


## Sample Types
There are two types of samples: Base and API Specific.

The base samples make up a set of samples that have code that
is identical or nearly identical for each AutoML Type. Meaning that for "Base" samples you can use them with any AutoML
Type. However, for API Specific samples, there will be a unique sample for each AutoML type. See the below list for more info.

## Base Samples
### Dataset Management
* [Import Dataset](import_dataset.py)
* [List Datasets](list_datasets.py) - For each AutoML Type the `metadata` field inside the dataset is unique, therefore each AutoML Type will have a
small section of code to print out the `metadata` field. 
* [Get Dataset](get_dataset.py) - For each AutoML Type the `metadata` field inside the dataset is unique, therefore each AutoML Type will have a
small section of code to print out the `metadata` field. 
* [Export Dataset](export_dataset.py)
* [Delete Dataset](delete_dataset.py)
### Model Management
* [List Models](list_models.py)
* [List Model Evaluation](list_model_evaluations.py) - For each AutoML Type the `metrics` field inside the model is unique, therefore each AutoML Type will have a
small section of code to print out the `metrics` field. 
* [Get Model](get_model.py)
* [Get Model Evaluation](get_model_evaluation.py) - For each AutoML Type the `metrics` field inside the model is unique, therefore each AutoML Type will have a
small section of code to print out the `metrics` field. 
* [Delete Model](delete_model.py)
* [Deploy Model](deploy_model.py) - Not supported by Translation
* [Undeploy Model](undeploy_model.py) - Not supported by Translation

### Batch Prediction
* [Batch Predict](batch_predict.py)

### Operation Management
* [List Operation Statuses](list_operation_status.py)
* [Get Operation Status](get_operation_status.py)

## AutoML Type Specific Samples
### Translation
* [Translate Create Dataset](translate_create_dataset.py)
* [Translate Create Model](translate_create_model.py)
* [Translate Predict](translate_predict.py)

### Natural Language Entity Extraction
* [Entity Extraction Create Dataset](language_entity_extraction_create_dataset.py)
* [Entity Extraction Create Model](language_entity_extraction_create_model.py)
* [Entity Extraction Predict](language_entity_extraction_predict.py)

### Natural Language Sentiment Analysis
* [Sentiment Analysis Create Dataset](language_sentiment_analysis_create_dataset.py)
* [Sentiment Analysis Create Model](language_sentiment_analysis_create_model.py)
* [Sentiment Analysis Predict](language_sentiment_analysis_predict.py)

### Natural Language Text Classification
* [Text Classification Create Dataset](language_text_classification_create_dataset.py)
* [Text Classification Create Model](language_text_classification_create_model.py)
* [Text Classification Predict](language_text_classification_predict.py)

### Vision Classification
* [Classification Create Dataset](vision_classification_create_dataset.py)
* [Classification Create Model](vision_classification_create_model.py)
* [Classification Predict](vision_classification_predict.py)
* [Deploy Node Count](vision_classification_deploy_model_node_count.py)

### Vision Object Detection
* [Object Detection Create Dataset](vision_object_detection_create_dataset.py)
* [Object Detection Create Model](vision_object_detection_create_model.py)
* [Object Detection Predict](vision_object_detection_predict.py)
* [Deploy Node Count](vision_object_detection_deploy_model_node_count.py)
