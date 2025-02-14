# Generative AI Samples on Google Cloud

This directory contains Python code samples demonstrating how to use Google Cloud's Generative AI capabilities on Vertex AI. These samples accompany the [Google Cloud Generative AI documentation](https://cloud.google.com/ai/generative-ai) and provide practical examples of various features and use cases.

## Getting Started

To run these samples, we recommend using either Google Cloud Shell, Cloud Code IDE, or Google Colab. You'll need a Google Cloud Project and appropriate credentials.

**Prerequisites:**

- **Google Cloud Project:** Create or select a project in the [Google Cloud Console](https://console.cloud.google.com).
- **Authentication:** Ensure you've authenticated with your Google Cloud account. See the [authentication documentation](https://cloud.google.com/docs/authentication) for details.
- **Enable the Vertex AI API:** Enable the API in your project through the [Cloud Console](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com).

## Sample Categories

The samples are organized into the following categories:

### Batch Prediction (`batch_prediction`)

Demonstrates how to use batch prediction with Generative AI models. This allows efficient processing of large datasets. See the [Batch Prediction documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-gemini) for more details.

### Content Cache (`content_cache`)

Illustrates how to create, update, use, and delete content caches. Caches store frequently used content to improve performance and reduce costs. See the [Content Cache documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview) for more information.

### Controlled Generation (`controlled_generation`)

Provides examples of how to control various aspects of the generated content, such as length, format, safety attributes, and more. This allows for tailoring the output to specific requirements and constraints. See the [Controlled Generation documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output) for details.

### Count Tokens (`count_tokens`)

Shows how to estimate token usage for inputs and outputs of Generative AI models. Understanding token consumption is crucial for managing costs and optimizing performance. See the [Token Counting documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/list-token) for more details.

### Express Mode (`express_mode`)

Demonstrates how to use Express Mode for simpler and faster interactions with Generative AI models using an API key. This mode is ideal for quick prototyping and experimentation. See the [Express Mode documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/start/express-mode/overview) for details.

### Live API (`live_api`)

Provides examples of using the Generative AI [Live API](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal-live-api). This allows for real-time interactions and dynamic content generation.

### Safety (`safety`)

Provides examples demonstrating how to configure and apply safety settings to Generative AI models. This includes techniques for content filtering and moderation to ensure responsible AI usage. See the [Safety documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes) for details.

### Text Generation (`text_generation`)

Provides examples of generating text using various input modalities (text, images, audio, video) and features like asynchronous generation, chat, and text streaming. See the [Text Generation documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini) for details.

### Tools (`tools`)

Showcases how to use tools like function calling, code execution, and grounding with Google Search to enhance Generative AI interactions. See the [Tools documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) for more information.

## Contributing

Contributions are welcome! See the [Contributing Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/CONTRIBUTING.md).

## Getting Help

For questions, feedback, or bug reports, please use the [issues page](https://github.com/GoogleCloudPlatform/python-docs-samples/issues).

## Disclaimer

This repository is not an officially supported Google product. The code is provided for demonstrative purposes only.
