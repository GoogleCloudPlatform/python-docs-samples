## 🌦 Weather forecasting -- _timeseries regression_

> [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/weather-forecasting/notebooks/1-overview.ipynb)
>
> [Watch the video in YouTube<br> ![thumbnail](http://img.youtube.com/vi/6-UJzEXMvGY/0.jpg)](https://youtu.be/6-UJzEXMvGY)

This model uses satellite data to forecast precipitation for the next 2 and 6 hours. The satellite data comes from [Google Earth Engine.](https://earthengine.google.com/)

* **Model**: 2D Fully Convolutional Network in [PyTorch]
* **Creating datasets**: [Sentinel-2] satellite data and [ESA WorldCover] from [Earth Engine] with [Dataflow]
* **Training the model**: [PyTorch] in [Vertex AI]
* **Getting predictions**: [PyTorch] locally

[Dataflow]: https://cloud.google.com/dataflow
[Earth Engine]: https://earthengine.google.com/
[PyTorch]: https://pytorch.org/
[Vertex AI]: https://cloud.google.com/vertex-ai
