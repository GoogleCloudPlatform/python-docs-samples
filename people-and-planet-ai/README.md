# 🌍 People & Planet AI

## 🦏 [Wildlife Insights -- _image-classification_](image-classification)

> [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/feat/modernize-ppai-image-classification/people-and-planet-ai/image-classification/README.ipynb)
>
> [Watch the video on YouTube ![thumbnail](https://img.youtube.com/vi/hUzODH3uGg0/0.jpg)](https://youtu.be/hUzODH3uGg0)

Classify wildlife species and extract ecological recovery metrics from
[camera trap](https://en.wikipedia.org/wiki/Camera_trap)
pictures in the public [LILA Science](https://lila.science/datasets/wcscameratraps) Cloud Storage bucket (`gs://public-datasets-lila/`).

* **Multimodal classification and ecological extraction**: [Gemini] (`gemini-3.8-flash`) via the [Google Gen AI SDK]
* **Rare-species visual similarity and vector search**: [Gemini Embedding 2] (`gemini-embedding-2`)
* **Class-balanced batch inference pipeline**: [Apache Beam] `RunInference` in [Dataflow]
* **Metadata and structured observation storage**: [BigQuery]

[Apache Beam]: https://beam.apache.org
[BigQuery]: https://cloud.google.com/bigquery
[Dataflow]: https://cloud.google.com/dataflow
[Gemini]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash
[Gemini Embedding 2]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/embedding-2
[Google Gen AI SDK]: https://googleapis.github.io/python-genai/

---

## 🗺 [Global Fishing Watch -- _timeseries-classification_](timeseries-classification)

> [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/timeseries-classification/README.ipynb)
>
> [Watch the video in YouTube<br> ![thumbnail](http://img.youtube.com/vi/LnEhSVEJUuY/0.jpg)](https://youtu.be/LnEhSVEJUuY)

This model is trained to classify if a ship is fishing or not every hour from their
[_Maritime Mobile Service Identity_ (MMSI)](https://en.wikipedia.org/wiki/Maritime_Mobile_Service_Identity)
location data.

* **Model**: 1D Fully Convolutional Network in [Keras]
* **Creating datasets**: [Apache Beam] in [Dataflow]
* **Training the model**: [Keras] in [Vertex AI]
* **Getting predictions**: [Keras] in [Cloud Run]

[Apache Beam]: https://beam.apache.org
[Cloud Run]: https://cloud.google.com/run
[Dataflow]: https://cloud.google.com/dataflow
[Keras]: https://keras.io
[Vertex AI]: https://cloud.google.com/vertex-ai

---

## 🏭 [Coal Plant Predictions -- _geospatial-classification_](geospatial-classification)

> [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/geospatial-classification/README.ipynb)
>
> [Watch the video in YouTube<br> ![thumbnail](http://img.youtube.com/vi/8amFK7T_n30/0.jpg)](https://youtu.be/8amFK7T_n30)

This model uses satellite data to predict if a coal plant is turned on and producing carbon emissions. The satellite data comes from [Google Earth Engine.](https://earthengine.google.com/)

* **Model**: 1D Fully Convolutional Network in [TensorFlow]
* **Creating datasets**: [Sentinel-2] satellite data from [Earth Engine]
* **Training the model**: [TensorFlow] in [Vertex AI]
* **Getting predictions**: [TensorFlow] in [Cloud Run]

[Cloud Run]: https://cloud.google.com/run
[Sentinel-2]: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
[Earth Engine]: https://earthengine.google.com/
[TensorFlow]: https://www.tensorflow.org/
[Vertex AI]: https://cloud.google.com/vertex-ai

---

## 🌍 [Land cover classification -- _image segmentation_](land-cover-classification)

> [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/land-cover-classification/README.ipynb)
>
> [Watch the video in YouTube<br> ![thumbnail](http://img.youtube.com/vi/zImQf91ffFo/0.jpg)](https://youtu.be/zImQf91ffFo)

This model uses satellite data to classify what is on Earth. The satellite data comes from [Google Earth Engine.](https://earthengine.google.com/)

* **Model**: 2D Fully Convolutional Network in [TensorFlow]
* **Creating datasets**: [Sentinel-2] satellite data and [ESA WorldCover] from [Earth Engine] with [Dataflow]
* **Training the model**: [TensorFlow] in [Vertex AI]
* **Getting predictions**: [TensorFlow] in [Cloud Run] (real-time) and [Dataflow] (batch)

[Sentinel-2]: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
[ESA WorldCover]: https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100

[Cloud Run]: https://cloud.google.com/run
[Dataflow]: https://cloud.google.com/dataflow
[Earth Engine]: https://earthengine.google.com/
[TensorFlow]: https://www.tensorflow.org/
[Vertex AI]: https://cloud.google.com/vertex-ai

---

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
