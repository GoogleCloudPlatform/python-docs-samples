Copyright 2018 Google LLC 

Licensed under the Apache License, Version 2.0 (the "License");you may not use this file except in compliance with the License.You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0


Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


# Purchase Prediction using AutoML Tables
One of the most common use cases in Marketing is to predict the likelihood of conversion. Conversion could be defined by the marketer as taking a certain action like making a purchase, signing up for a free trial, subscribing to a newsletter, etc. Knowing the likelihood that a marketing lead or prospect will ‘convert’ can enable the marketer to target the lead with the right marketing campaign. This could take the form of remarketing, targeted email campaigns, online offers or other treatments.

Here we demonstrate how you can use Bigquery and AutoML Tables to build a supervised binary classification model for purchase prediction. 

## Problem Description
The model uses a real dataset from the [Google Merchandise store](www.googlemerchandisestore.com) consisting of Google Analytics web sessions.

The goal here is to predict the likelihood of a web visitor visiting the online Google Merchandise Store making a purchase on the website during that Google Analytics session. Past web interactions of the user on the store website in addition to information like browser details and geography are used to make this prediction.

This is framed as a binary classification model, to label a user during a session as either true (makes a purchase) or false (does not make a purchase).
Dataset Details
The dataset consists of a set of tables corresponding to Google Analytics sessions being tracked on the [Google Merchandise Store](https://www.googlemerchandisestore.com/). Each table is a single day of GA sessions. More details around the schema can be seen [here](https://support.google.com/analytics/answer/3437719?hl=en&ref_topic=3416089).

You can access the data on BigQuery [here](https://bigquery.cloud.google.com/dataset/bigquery-public-data:google_analytics_sample).

## Solution Walkthrough
The solution has been developed using [Google Colab Notebook](https://colab.research.google.com/notebooks/welcome.ipynb). Here are the thought process and specific steps that went into building the “Purchase Prediction with AutoML Tables” colab. The colab is broken into 7 parts; this write up will mirror that structure.

Before we dive in, a few housekeeping notes about setting up the colab or Jupyter.


Steps Involved

### 1. Set up

**If you are using AI Platform Notebooks**, your environment is alreadyauthenticated. Skip this step.

The first step in this process was to set up the project. We referred to the [AutoML tables documentation](https://cloud.google.com/automl-tables/docs/) and take the following steps:
* Create a Google Cloud Platform (GCP) project
* Enable billing
* Enable the AutoML API
* Enable the AutoML Tables API

There are a few options concerning how to host the colab: default hosted runtime, local runtime, or hosting the runtime on a Virtual Machine (VM). 

##### Default Hosted Runtime:

The hosted runtime is the simplest to use. It accesses a default VM already configured to host the colab notebook. Simply navigate to the upper right hand corner click on the connect drop down box, which will give you the option to “connect to hosted runtime”. 
Alternatively you can use the [AI Platform Notebooks] (https://cloud.google.com/ai-platform-notebooks/).

##### Local Runtime:
The local runtime takes a bit more work. It involves downloading jupyter notebooks onto your local machine, likely the desktop from which you access the colab. After downloading jupyter notebooks, you can connect to the local runtime. The colab notebook will run off of your local machine. Detailed instructions can be found [here](https://research.google.com/colaboratory/local-runtimes.html).

##### VM hosted Runtime:
Finally, the runtime hosted on the VM requires the most amount of set up, but gives you more control on the machine choice allowing you to access machines with more memory and processing.The instructions are similar to the steps taken for the local runtime, with one main distinction: the VM hosted runtime runs the colab notebook off of the VM, so you will need to set up everything on the VM rather than on your local machine.

To achieve this, create a Compute Engine VM instance. Then make sure that you have the firewall open to allow you to ssh into the VM. 

The firewall rules can be found in the VPC Network tab on the Cloud Console. Navigate into the firewall rules, and add a rule that allows your local IP address to allow ingress on tcp: 22.  To find your IP address, type into the terminal the following command:

```curl -4 ifconfig.co```

Once your firewall rules are created, you should be able to ssh into your VM instance. To ssh, run the following command: 

```gcloud compute ssh --zone YOUR_ZONE YOUR_INSTANCE_NAME -- -L 8888:localhost:8888```
	
This will allow your local terminal to ssh into the VM instance you created, which simultaneously port forwarding the port 8888 from your local machine to the VM. Once in the VM, you can download jupyter notebooks and open up a notebook as seen in the instructions [here](https://research.google.com/colaboratory/local-runtimes.html). Specifically steps 2, 3.
	
We recommend hosting using the VM for two main reasons:
1. The VM can be provisioned to be much, much more powerful than either your local machine or the default runtime allocated by the notebook. 
2. The notebook is currently configured to run on either your local machine or a VM. It requires you to install the AutoML client library and uplaod a service account key to the machine from which you are hosting the notebook. These two actions can be done the default hosted runtime, but would require a different set of instructions not detailed in this specific colab. To see them, refer to the AutoML Tables sample colab found in the tutorials section of the [documentation](https://cloud.google.com/automl-tables/docs/). Specifically step 2.


### 2. Initialize and authenticate
The client library installation is entirely self explanatory in the notebook.

The authentication process is only slightly more complex: run the second code block entitled "Authenticate using service account key  and create a client" and then upload the service account key you created in the set up step
	Would also recommend setting a global variable

```export GOOGLE_APPLICATION_CREDENTIALS=`<path to your service account key>` ```

Be sure to export whenever you boot up a new session.


### 3. Data Cleaning and Transformation
This step was by far the most involved. It includes a few sections that create an AutoML tables dataset, pull the Google merchandise store data from BigQuery, transform the data, and save it multiple times to csv files in google cloud storage.

The dataset that is made viewable in the AutoML Tables UI. It will eventually hold the training data after that training data is cleaned and transformed. 

This dataset has only around 1% of its values with a positive label value of True i.e. cases when a transaction was made. This is a class imbalance problem. There are several ways to handle class imbalance. We chose to oversample the positive class by random over sampling. This resulted in an artificial increase in the sessions with the positive label of true transaction value.

There were also many columns with either all missing or all constant values. These columns would not add any signal to our model, so we dropped them.

There were also columns with NaN rather than 0 values. For instance, rather than having a count of 0, a column might have a null value. So we added code to change some of these null values to 0, specifically in our target column, in which null values were not allowed by AutoML Tables. However, AutoML Tables can handle null values for the features.

### 4. Feature Engineering

The dataset had rich information on customer location and behavior; however, it can be improved by performing feature engineering. Moreover, there was a concern about data leakage. The decision to do feature engineering, therefore, had two contributing motivations: remove data leakage without too much loss of useful data, and to improve the signal in our data.



#### 4.1 Weekdays

The date seemed like a useful piece of information to include, as it could capture seasonal effects. Unfortunately, we only had one year of data, so seasonality on an annual scale would be difficult (read impossible) to incorporate. Fortunately, we could try and detect seasonal effects on a micro, with perhaps equally informative results.  We ended up creating a new column of weekdays out of dates, to denote which day of the week the session was held on. This new feature turned out to have some useful predictive power, when added as a variable into our model.

#### 4.2 Data Leakage
The marginal gain from adding a weekday feature, was overshadowed by the concern of data leakage in our training data. In the initial naive models we trained, we got outstanding results. So outstanding that we knew that something must be going on. As it turned out, quite a few features functioned as proxies for the feature we were trying to predict: meaning some of the features we conditioned on to build the model had an almost 1:1 correlation with the target feature. Intuitively, this made sense.

One feature that exhibited this behavior was the number of page views a customer made during a session. By conditioning on page views in a session, we could very reliably predict which customer sessions a purchase would be made in. At first this seems like the golden ticket, we can reliably predict whether or not a purchase is made! The catch: the full page view information can only be collected at the end of the session, by which point we would also have whether or not a transaction was made. Seen from this perspective, collecting page views at the same time as collecting the transaction information would make it pointless to predict the transaction information using the page views information, as we would already have both. One solution was to drop page views as a feature entirely. This would safely stop the data leakage, but we would lose some critically useful information. Another solution, (the one we ended up going with), was to track the page view information of all previous sessions for a given customer, and use it to inform the current session. This way, we could use the page view information, but only the information that we would have before the session even began. So we created a new column called previous_views, and populated it with the total count of all previous page views made by the customer in all previous sessions. We then deleted the page views feature, to stop the data leakage.

Our rationale for this change can be boiled down to the concise heuristic: only use the information that is available to us on the first click of the session. Applying this reasoning, we performed similar data engineering on other features which we found to be proxies for the label feature. We also refined our objective in the process: For a visit to the Google Merchandise store, what is the probability that a customer will make a purchase, and can we calculate this probability the moment the customer arrives? By clarifying the question, we both made the result more powerful/useful, and eliminated the data leakage that threatened to make the predictive power trivial.


### 5. Train-Validation-Test Split
	
To create the datasets for training, testing and validation, we first had to consider what kind of data we were dealing with. The data we had keeps track of all customer sessions with the Google Merchandise store over a year.  AutoML tables does its own training and testing, and delivers a quite nice UI to view the results in. For the training and testing dataset then, we simply used the over sampled, balanced dataset created by the transformations described above. But we first partitioned the dataset to include the first 9 months in one table and the last 3 in another. This allowed us to train and test with an entirely different dataset that what we used to validate.

Moreover, we held off on oversampling for the validation dataset, to not bias the data that we would ultimately use to judge the success of our model.

The decision to divide the sessions along time was made to avoid the model training on future data to predict past data. (This can be avoided with a datetime variable in the dataset and by toggling a button in the UI)

### 6. Update dataset: assign a label column and enable nullable columns

This section is fairly self explanatory in the colab. Simply update the target column to not nullable, and update the assigned label to ‘totalTransactionRevenue’

### 7. Creating a Model, Make a Prediction

These parts are mostly self explanatory. 
Note that we trained on the first 9 months of data and we validate using the last 3.

### 8. Evaluate your Prediction
In this section, we take our validation data prediction results and plot the Precision Recall Curve and the ROC curve of both the false and true predictions.
