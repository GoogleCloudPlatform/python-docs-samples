# AutoML Samples

<a href="https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/java-docs-samples&page=editor&open_in_editor=vision/beta/cloud-client/README.md">
<img alt="Open in Cloud Shell" src ="http://gstatic.com/cloudssh/images/open-btn.png"></a>


This directory contains samples for the [Google Cloud AutoML APIs](https://cloud.google.com/automl/) - [docs](https://cloud.google.com/automl/docs/)

We highly reccommend that you refer to the official documentation pages:
<!--* AutoML Natural Language
  * [Classification](https://cloud.google.com/natural-language/automl/docs)
  * [Entity Extraction](https://cloud.google.com/natural-language/automl/entity-analysis/docs)
  * [Sentiment Analysis](https://cloud.google.com/natural-language/automl/sentiment/docs) -->
* [AutoML Translation](https://cloud.google.com/translate/automl/docs)
<!--* AutoML Video Intelligence
  * [Classification](https://cloud.google.com/video-intelligence/automl/docs)
  * [Object Tracking](https://cloud.google.com/video-intelligence/automl/object-tracking/docs)
* AutoML Vision
  * [Classification](https://cloud.google.com/vision/automl/docs)
  * [Edge](https://cloud.google.com/vision/automl/docs/edge-quickstart)
  * [Object Detection](https://cloud.google.com/vision/automl/object-detection/docs)
* [AutoML Tables](https://cloud.google.com/automl-tables/docs)-->

This API is part of the larger collection of Cloud Machine Learning APIs.

These Java samples demonstrates how to access the Cloud AutoML API
using the [Google Cloud Client Library for Java][google-cloud-java].

[google-cloud-java]: https://github.com/GoogleCloudPlatform/google-cloud-java

## Build the samples

Install [Maven](http://maven.apache.org/).

Build your project with:

```
mvn clean package
```

## Sample Types
There are two types of samples: Base and API Specific

The base samples make up a set of samples that have code that
is identical or nearly identical for each AutoML Type. Meaning that for "Base" samples you can use them with any AutoML
Type. However, for API Specific samples, there will be a unique sample for each AutoML type. See the below list for more info.

## Base Samples
### Dataset Management
* [Import Dataset](src/main/java/com/example/automl/ImportDataset.java)
* [List Datasets](src/main/java/com/example/automl/ListDatasets.java) - For each AutoML Type the `metadata` field inside the dataset is unique, therefore each AutoML Type will have a
small section of code to print out the `metadata` field. 
* [Get Dataset](src/main/java/com/example/automl/GetDataset.java) - For each AutoML Type the `metadata` field inside the dataset is unique, therefore each AutoML Type will have a
small section of code to print out the `metadata` field. 
* [Export Dataset](src/main/java/com/example/automl/ExportDataset.java)
* [Delete Dataset](src/main/java/com/example/automl/DeleteDataset.java)
### Model Management
* [List Models](src/main/java/com/example/automl/ListModels.java)
* [List Model Evaluation](src/main/java/com/example/automl/ListModelEvaluations.java)
* [Get Model](src/main/java/com/example/automl/)
* [Get Model Evaluation](src/main/java/com/example/automl/GetModelEvaluation.java)
* [Delete Model](src/main/java/com/example/automl/DeleteModel.java)

### Operation Management
* [List Operation Statuses](src/main/java/com/example/automl/ListOperationStatus.java)
* [Get Operation Status](src/main/java/com/example/automl/GetOperationStatus.java)

## AutoML Type Specific Samples
### Translation
* [Translate Create Dataset](src/main/java/com/example/automl/TranslateCreateDataset.java)
* [Translate Create Model](src/main/java/com/example/automl/TranslateCreateModel.java)
* [Translate Predict](src/main/java/com/example/automl/TranslatePredict.java)