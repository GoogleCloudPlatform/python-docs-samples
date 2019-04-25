# Custom prediction routines (beta)

Read the AI Platform documentation about custom prediction routines to learn how
to use these samples:

* [Custom prediction routines (with a TensorFlow Keras
  example)](https://cloud.google.com/ml-engine/docs/tensorflow/custom-prediction-routines)
* [Custom prediction routines (with a scikit-learn
  example)](https://cloud.google.com/ml-engine/docs/scikit/custom-prediction-routines)

If you want to package a predictor directly from this directory, make sure to
edit `setup.py`: replace the reference to `predictor.py` with either
`tensorflow-predictor.py` or `scikit-predictor.py`.

## What's next

For a more complete example of how to train and deploy a custom prediction
routine, check out one of the following tutorials:

* [Creating a custom prediction routine with
  Keras](https://cloud.google.com/ml-engine/docs/tensorflow/custom-prediction-routine-keras)
  (also available as [a Jupyter
  notebook](https://colab.research.google.com/github/GoogleCloudPlatform/cloudml-samples/blob/master/notebooks/tensorflow/custom-prediction-routine-keras.ipynb))

* [Creating a custom prediction routine with
  scikit-learn](https://cloud.google.com/ml-engine/docs/scikit/custom-prediction-routine-scikit-learn)
  (also available as [a Jupyter
  notebook](https://colab.research.google.com/github/GoogleCloudPlatform/cloudml-samples/blob/master/notebooks/scikit-learn/custom-prediction-routine-scikit-learn.ipynb))