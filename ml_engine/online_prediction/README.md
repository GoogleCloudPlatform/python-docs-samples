# Online Prediction with the Cloud Machine Learning Engine

This sample assumes that you have already run the Cloud ML Engine end to end walkthrough using the UCI Census dataset, including training a wide & deep model and deploying it into production, ready to take prediction requests.

This sample then shows you how to create a client that takes user JSON inputs, and sends those inputs as online prediction requests to a given deployed model.

In order to use this client, first obtain the following information, and store it into the given environment variables:

```
PROJECT=<your project name>
MODEL=<your model name>
VERSION=<version of model you are using>
```

Next, launch this client as follows:

```
python predict.py --project=$PROJECT --model=$MODEL --version=$VERSION
```

After having done that, the client will ask you for ‘Valid JSON’ input as follows:

```
Valid JSON >>>
```

Now you can input a JSON example that corresponds to the schema of the given model. For instance if you are sending prediction requests to the census-based model created in the Cloud ML Engine walkthrough, you can send a JSON example like the following:

```
{"age": 25, "workclass": " Private", "education": " 11th", "education_num": 7, "marital_status": " Never-married", "occupation": " Machine-op-inspct", "relationship": " Own-child", "race": " Black", "gender": " Male", "capital_gain": 0, "capital_loss": 0, "hours_per_week": 40, "native_country": " United-States"}
```
The result should be something along the following lines (depending on how you trained the model/what parameters you used, the results may vary):

```
[{u'probabilities': [0.992774486541748, 0.007225471083074808], u'logits': [-4.922891139984131], u'classes': 0, u'logistic': [0.007225471083074808]}]
```

Now that you have a working client, you can adapt this to your own use cases!
