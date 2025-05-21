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

### [Batch Prediction](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/batch_prediction/)

Demonstrates how to use batch prediction with Generative AI models. This allows efficient processing of large datasets.
See the [Batch Prediction documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-gemini)
for more details.

### [Bounding Box](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/bounding_box/)

Demonstrates how to use Bounding Box with Generative AI models. This allows for object detection and localization within
images and video. see the [Bounding Box documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/bounding-box-detection)
for more details.

### [Content Cache](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/content_cache/)

Illustrates how to create, update, use, and delete content caches. Caches store frequently used content to improve
performance and reduce costs. See the [Content Cache documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)
for more information.

### [Controlled Generation](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/controlled_generation/)

Provides examples of how to control various aspects of the generated content, such as length, format, safety attributes,
and more. This allows for tailoring the output to specific requirements and constraints.
See the [Controlled Generation documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output)
for details.

### [Count Tokens](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/count_tokens/)

Shows how to estimate token usage for inputs and outputs of Generative AI models. Understanding token consumption is
crucial for managing costs and optimizing performance. See the [Token Counting documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/list-token)
for more details.

### [Express Mode](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/express_mode/)

Demonstrates how to use Express Mode for simpler and faster interactions with Generative AI models using an API key.
This mode is ideal for quick prototyping and experimentation. See the [Express Mode documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/start/express-mode/overview)
for details.

### [Image Generation](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/image_generation/)

Demonstrates how to generate image and edit images using Generative AI models. Check [Image Generation with Gemini Flash](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation)
and [Imagen on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview) for details.


### [Live API](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/live_api/)

Provides examples of using the Generative AI [Live API](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal-live-api).
This allows for real-time interactions and dynamic content generation.

### [Model Optimizer](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/model_optimizer/)

Provides examples of using the Generative AI [Model Optimizer](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/vertex-ai-model-optimizer).
Vertex AI Model Optimizer is a dynamic endpoint designed to simplify model selection by automatically applying the 
Gemini model which best meets your needs.

### [Provisioned Throughput](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/live_api/)

Provides examples demonstrating how to use Provisioned Throughput with Generative AI models. This feature provides a
fixed-cost monthly subscription or weekly service that reserves throughput for supported generative AI models on Vertex AI.
See the [Provisioned Throughput](https://cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) for details.

### [Safety](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/safety/)

Provides examples demonstrating how to configure and apply safety settings to Generative AI models. This includes
techniques for content filtering and moderation to ensure responsible AI usage. See the
[Safety documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes)
for details.

### [Text Generation](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/text_generation/)

Provides examples of generating text using various input modalities (text, images, audio, video) and features like
asynchronous generation, chat, and text streaming. See the[Text Generation documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini)
for details.

### [Tools](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/tools/)

Showcases how to use tools like function calling, code execution, and grounding with Google Search to enhance
Generative AI interactions. See the [Tools documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) for more information.

### [Video Generation](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai/video_generation/)

Provides examples of generating videos using text & images input modalities. See the
[Video Generation documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos) for details.

## Contributing

Contributions are welcome! See the [Contributing Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/CONTRIBUTING.md).

## Getting Help

For questions, feedback, or bug reports, please use the [issues page](https://github.com/GoogleCloudPlatform/python-docs-samples/issues).

## Disclaimer

This repository is not an officially supported Google product. The code is provided for demonstrative purposes only.
