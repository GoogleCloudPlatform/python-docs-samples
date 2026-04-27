# Generative AI on Google Cloud: Python Samples

This directory contains the official Python code samples featured in the [Google Cloud Generative AI documentation](https://cloud.google.com/ai/generative-ai?hl=en). These scripts demonstrate how to integrate and build with Vertex AI.

Looking for interactive, step-by-step tutorials? Check out our extensive collection of [Colab notebooks](https://github.com/GoogleCloudPlatform/generative-ai/tree/main).

## Getting Started

> **Note:** An active Google Cloud Project is required.

We recommend running these code samples using Google Cloud Shell Editor or Google Colab to minimize environment setup.

### Feature folders

Browse the folders below to find the Generative AI capabilities you're interested in.

<table>
  <tr>
   <td><strong>Python Samples Folder</strong>
   </td>
   <td><strong>Google Cloud Product</strong>
   </td>
   <td><strong>Short Description (With the help of Gemini 3.1)</strong>
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/embeddings">Embeddings</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings">https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings</a>
   </td>
   <td>Learn how to use Vertex AI's text and multimodal embedding models. These samples show you how to convert your unstructured data into numerical vectors to power semantic search, clustering, and RAG applications.
   </td>
  </tr>


  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/extensions">Extensions</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/extensions/overview">https://cloud.google.com/vertex-ai/generative-ai/docs/extensions/overview</a>
   </td>
   <td>These samples show how to connect Gemini to external APIs and databases so your models can retrieve live data and execute real-world actions. **Note** that as Google Cloud transitions to the Gemini Enterprise Agent Platform, standalone Vertex AI Extensions are evolving into *Tools* managed within the centralized Agent Registry. While these examples teach the core mechanics of model-to-API communication, future production applications should adopt the new Agent Platform architecture..
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/function_calling">Function Calling</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling</a>
   </td>
   <td>Function calling gives Gemini the ability to interact with your codebase. The model predicts which of your local functions needs to be run and returns the formatted arguments, leaving the actual execution up to your application.
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/image_generation">Image Generation</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview">https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview</a>
   </td>
   <td>Learn how to integrate the Imagen model into your applications. These examples cover text-to-image generation, editing, and using advanced parameters to get the exact visual output you need.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/model_garden">Model Garden</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models">https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models</a>
   </td>
   <td>These examples show you how to provision endpoints and serve predictions from first-party, third-party, and open-source foundation models available in the Vertex AI Model Garden.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/model_tuning">Model Tuning</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models">https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models</a>
   </td>
   <td>Tailor Gemini and other foundation models to your specific domain. These examples cover how to format your datasets, kick off tuning jobs on Vertex AI, and deploy your custom-tuned models or adapters to production endpoints.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/rag">RAG</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api">https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api</a>
   </td>
   <td>These examples cover the end-to-end RAG architecture: ingesting data, generating embeddings, querying a vector database, and passing the retrieved context to Gemini to generate informed, accurate answers.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/reasoning_engine">Reasoning Engine</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine">https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine</a>
   </td>
   <td>These examples cover how to use Vertex AI Reasoning Engine to build custom agents.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/text_generation">Text Generation</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini</a>
   </td>
   <td>These samples demonstrate how to use Vertex AI's Gemini models to generate, summarize, and extract information from text.
   </td>
  </tr>
</table>

## Contributing

Contributions welcome! See the [Contributing Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/CONTRIBUTING.md).

## Getting help

Please use the [issues page](https://github.com/GoogleCloudPlatform/python-docs-samples/issues) to provide suggestions, feedback or submit a bug report.

## Disclaimer

This repository itself is not an officially supported Google product. The code in this repository is for demonstrative purposes only.