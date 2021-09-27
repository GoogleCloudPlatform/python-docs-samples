# 🌍 People & Planet AI

## 🦏 [Wildlife Insights -- _image-classification_](image-classification)

This model is trained to recognize animal species from
[camera trap](https://en.wikipedia.org/wiki/Camera_trap)
pictures.

* **Creating datasets**: [Apache Beam] in [Dataflow]
* **Training the model**: [AutoML] in [Vertex AI]
* **Getting predictions**: [Vertex AI]

## 🗺 [Global Fishing Watch -- _timeseries-classification_](timeseries-classification)

This model is trained to categorize if a ship is fishing or not every hour from their
[_Maritime Mobile Service Identitiy_ (MMSI)](https://en.wikipedia.org/wiki/Maritime_Mobile_Service_Identity)
location data.

* **Creating datasets**: [Apache Beam] in [Dataflow]
* **Training the model**: [Keras] in [Vertex AI]
* **Getting predictions**: [Keras] in [Cloud Run]

[Apache Beam]: https://beam.apache.org
[AutoML]: https://cloud.google.com/vertex-ai/docs/beginner/beginners-guide
[Cloud Run]: https://cloud.google.com/run
[Dataflow]: https://cloud.google.com/dataflow
[Keras]: https://keras.io
[Vertex AI]: https://cloud.google.com/vertex-ai
