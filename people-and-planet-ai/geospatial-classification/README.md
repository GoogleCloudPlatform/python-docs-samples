# 🏭 Coal Plant Predictions -- _geospatial-classification_ (retired)

This sample has been retired and is no longer maintained.

It trained a TensorFlow model on Vertex AI to predict, from Sentinel-2 satellite
imagery in Earth Engine, whether a coal plant was operating, and served the
predictions from Cloud Run. It accompanied the video
[Mapping carbon pollution globally with satellites](https://youtu.be/8amFK7T_n30).

## Why it was retired

* The notebook no longer runs: its setup step depends on a file that was removed
  in 2023, and its training and serving code don't work with Keras 3.
* It used the deprecated `COPERNICUS/S2` Earth Engine dataset.
* Its labels end in 2021, and many of the labeled plants have since closed or
  switched to natural gas.

## Last version

You can still read the code as it was before retirement at commit
[`636f2f5`](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/636f2f5fc1b4dc34855b3115b0deba21b524cc51/people-and-planet-ai/geospatial-classification).
It isn't maintained and doesn't run as is.

## Related samples

* [Weather forecasting](../weather-forecasting): forecasting with Earth Engine
  satellite data.
* [Wildlife Insights](../image-classification): classifying camera trap images
  with Gemini.
