# Generative AI Samples on Google Cloud

Welcome to the Python samples folder for Generative AI on Vertex AI! In this folder, you can find the Python samples
used in [Google Cloud Generative AI documentation](https://cloud.google.com/ai/generative-ai?hl=en).

If you are looking for colab notebook, then this [link](https://github.com/GoogleCloudPlatform/generative-ai/tree/main).

## Getting Started

To try and run these Code samples, we have following recommend using Google Cloud IDE or Google Colab.

Note: A Google Cloud Project is a pre-requisite.

### Feature folders

Browse the folders below to find the Generative AI capabilities you're interested in.

<table>
  <tr>
   <td><strong>Python Samples Folder</strong>
   </td>
   <td><strong>Google Cloud Product</strong>
   </td>
   <td><strong>Short Description (With the help of Gemini 1.5)</strong>
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/context_caching">Context Caching</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview">https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview</a>
   </td>
   <td>Code samples demonstrating how to use context caching with Vertex AI's generative models. This allows for more consistent and relevant responses across multiple interactions by storing previous conversation history.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/controlled_generation">Controlled Generation</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output</a>
   </td>
   <td>Examples of how to control the output of generative models, such as specifying length, format, or sentiment.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/count_token">Count Token</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/list-token">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/list-token</a>
   </td>
   <td>Code demonstrating how to count tokens in text, which is crucial for managing costs and understanding model limitations.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/embeddings">Embeddings</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings">https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings</a>
   </td>
   <td>Code showing how to generate and use embeddings from text or images. Embeddings can be used for tasks like semantic search, clustering, and classification.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/extensions">Extensions</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/extensions/overview">https://cloud.google.com/vertex-ai/generative-ai/docs/extensions/overview</a>
   </td>
   <td>Demonstrations of how to use extensions with generative models, enabling them to access and process real-time information, use tools, and interact with external systems.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/function_calling">Function Calling</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling</a>
   </td>
   <td>Examples of how to use function calling to enable generative models to execute specific actions or retrieve information from external APIs.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/grounding">Grounding</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview">https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview</a>
   </td>
   <td>Code illustrating how to ground generative models with specific knowledge bases or data sources to improve the accuracy and relevance of their responses.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/image_generation">Image Generation</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview">https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview</a>
   </td>
   <td>Samples showcasing how to generate images from text prompts using models like Imagen.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/model_garden">Model Garden</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models">https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models</a>
   </td>
   <td>Resources related to exploring and utilizing pre-trained models available in Vertex AI's Model Garden.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/model_tuning">Model Tuning</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models">https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models</a>
   </td>
   <td>Code and guides for fine-tuning pre-trained generative models on specific datasets or for specific tasks.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/rag">RAG</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api">https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api</a>
   </td>
   <td>Information and resources about Retrieval Augmented Generation (RAG), which combines information retrieval with generative models.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/reasoning_engine">Reasoning Engine</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine">https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine</a>
   </td>
   <td>Details about the Reasoning Engine, which enables more complex reasoning and logical deduction in generative models.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/safety">Safety</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes</a>
   </td>
   <td>Examples of how to configure safety attributes and filters to mitigate risks and ensure responsible use of generative models.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/system_instructions">System Instructions</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/system-instructions?hl=en">https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/system-instructions?hl=en</a>
   </td>
   <td>Code demonstrating how to provide system instructions to guide the behavior and responses of generative models.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/text_generation">Text Generation</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini</a>
   </td>
   <td>Samples of how to generate text using Gemini models, including chat-based interactions and creative writing.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/audio">Understand Audio</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/audio-understanding">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/audio-understanding</a>
   </td>
   <td>Examples of how to use generative models for audio understanding tasks, such as transcription and audio classification.
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/video">Understand Video</a>
   </td>
   <td><a href="https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/video-understanding">https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/video-understanding</a>
   </td>
   <td>Samples showcasing how to use generative models for video understanding tasks, such as video summarization and content analysis.
   </td>
  </tr>
</table>

## Contributing

Contributions welcome! See the [Contributing Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/CONTRIBUTING.md).

## Getting help

Please use the [issues page](https://github.com/GoogleCloudPlatform/python-docs-samples/issues) to provide suggestions, feedback or submit a bug report.

## Disclaimer

This repository itself is not an officially supported Google product. The code in this repository is for demonstrative purposes only.