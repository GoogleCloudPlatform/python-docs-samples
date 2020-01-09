AutoML Tables enables your entire team to automatically build and deploy state-of-the-art machine learning models on structured data at massively increased speed and scale.


## Problem Description
The model uses a real dataset from the [Census Income Dataset](https://archive.ics.uci.edu/ml/datasets/Census+Income).


The goal is the predict if a given individual has an income above or below 50k, given information like the person's age, education level, marital-status, occupation etc... 
This is framed as a binary classification model, to label the individual as either having an income above or below 50k.






Dataset Details


The dataset consists of over 30k rows, where each row corresponds to a different person. For a given row, there are 14 features that the model conditions on to predict the income of the person. A few of the features are named above, and the exhaustive list can be found both in the dataset link above or seen in the colab.




## Solution Walkthrough
The solution has been developed using [Google Colab Notebook](https://colab.research.google.com/notebooks/welcome.ipynb) or in Jupyter (see [AI Platform Notebooks](https://cloud.google.com/ai-platform-notebooks/)). 




Steps Involved


### 1. Set up
The first step in this process was to set up the project. We referred to the [AutoML tables documentation](https://cloud.google.com/automl-tables/docs/) and take the following steps if run in Colab:
* Create a Google Cloud Platform (GCP) project
* Enable billing
* Enable the AutoML API
* Enable the AutoML Tables API
* Create a service account, grant required permissions, and download the service account private key.

**If you are using AI Platform Notebooks**, your environment is already authenticated

### 2. Initialize and authenticate


The client library installation is entirely self explanatory in the colab. 


The authentication process is only slightly more complex: run the second code block entitled "Authenticate using service account key" and then upload the service account key you created in the set up step.


To make sure your colab was authenticated and has access to your project, replace the project_id with your project_id, and run the subsequent code blocks. You should see the lists of your datasets and any models you made previously in AutoML Tables.


### 3. Import training data


This section has you create a dataset and import the data. You have both the option of using the csv import from a Cloud Storage bucket, or you can upload the csv into Big Query and import it from there. 




### 4. Update dataset: assign a label column and enable nullable columns


This section is important, as it is where you specify which column (meaning which feature) you will use as your label. This label feature will then be predicted using all other features in the row.


### 5. Creating a model


This section is where you train your model. You can specify how long you want your model to train for. 


### 6. Make a prediction


This section gives you the ability to do a single online prediction. You can toggle exactly which values you want for all of the numeric features, and choose from the drop down windows which values you want for the categorical features. 


The model takes a while to deploy online, and currently there does not exist a feedback mechanism in the sdk, so you will need to wait until the model finishes deployment to run the online prediction.
When the deployment code ```response = client.deploy_model(model_name)``` finishes, you will be able to see this on the [UI](https://console.cloud.google.com/automl-tables). 


To see when it finishes, click on the UI link above and navitage to the dataset you just uploaded, and go to the predict tab. You should see "online prediction" text near the top, click on it, and it will take you to a view of your online prediction interface. You should see "model deployed" on the far right of the screen if the model is deployed, or a "deploying model" message if it is still deploying.


Once the model finishes deployment, go ahead and run the ```prediction_client.predict(model_name, payload)``` line.


Note: If the model has not finished deployment, the prediction will NOT work.


### 7. Batch Prediction


There is a validation csv file provided with a few rows of data not used in the training or testing for you to run a batch prediction with. The csv is linked in the text of the colab as well as [here](https://storage.cloud.google.com/cloud-ml-data/automl-tables/notebooks/census_income_batch_prediction_input.csv) .
