# 🦏 Wildlife Insights -- _image-classification_

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/image-classification/README.ipynb)

> [Watch the video on YouTube ![thumbnail](https://img.youtube.com/vi/hUzODH3uGg0/0.jpg)](https://youtu.be/hUzODH3uGg0)

Classify wildlife species and extract ecological recovery metrics from
[camera trap](https://en.wikipedia.org/wiki/Camera_trap)
pictures in the public [LILA Science](https://lila.science/datasets/wcscameratraps) Cloud Storage bucket (`gs://public-datasets-lila/`).

* **Multimodal classification and ecological extraction**: [Gemini] (`gemini-3.8-flash`) via the [Google Gen AI SDK]
* **Rare-species visual similarity and vector search**: [Gemini Embedding 2] (`gemini-embedding-2`)
* **Class-balanced batch inference pipeline**: [Apache Beam] `RunInference` in [Dataflow]
* **Metadata and structured observation storage**: [BigQuery]

## Snippet files

* [`create_images_metadata_table.py`](create_images_metadata_table.py) (`dataflow_wildlife_ingest_metadata`): Ingests and cleans LILA WCS camera trap annotations into BigQuery.
* [`classify_wildlife_image.py`](classify_wildlife_image.py) (`genai_wildlife_classify_image`): Classifies a camera trap image into structured ecological metadata (`species_scientific_name`, `taxon_family`, `common_name`, `animal_count`, `juvenile_present`, `is_empty_or_misfire`, `confidence`) with optional habitat geo-fencing (`habitat_region`).
* [`embed_wildlife_image.py`](embed_wildlife_image.py) (`genai_wildlife_embed_image`): Generates a 768-dimensional multimodal vector embedding for a camera trap image using `gemini-embedding-2`.
* [`run_wildlife_inference.py`](run_wildlife_inference.py) (`dataflow_wildlife_run_inference`): Runs class-balanced sampling (`Sample.FixedSizePerKey`) and batch Gemini inference (`RunInference`) directly against `gs://public-datasets-lila/wcs-unzipped/` and writes results to BigQuery.

[Apache Beam]: https://beam.apache.org
[BigQuery]: https://cloud.google.com/bigquery
[Dataflow]: https://cloud.google.com/dataflow
[Gemini]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash
[Gemini Embedding 2]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/embedding-2
[Google Gen AI SDK]: https://googleapis.github.io/python-genai/

> 📜 For more information about the background of this solution, see [Recovering global wildlife populations using ML](https://cloud.google.com/blog/topics/developers-practitioners/recovering-global-wildlife-populations-using-ml).
