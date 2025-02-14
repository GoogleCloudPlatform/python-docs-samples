# Generative AI - Template Folder Sample

This directory showcases how to use templates with Generative AI models on Vertex AI using the `google-genai` library.
This allows developers to structure and organize prompts more effectively.

This guide explains how to create new feature folders within the `python-docs-samples/genai` repository,
specifically focusing on the structure established in the template_folder example.
This assumes you're familiar with basic Python development and Git.

## Folder Structure

When adding a new feature, replicate the structure of the template_folder directory.
This standardized structure ensures consistency and maintainability across the projec

**Recommended Folder-File Structure:**

```
genai/
└── <new_feature_folder>/
    ├── noxfile_config.py
    ├── requirements-test.txt
    ├── requirements.txt
    ├── <newfeature>_<(optional)highlights>_with_<input_type>.py
    └── test_<new_feature_name>_examples.py
```

- `<new_feature_folder`>: A descriptive name for your feature (e.g., custom_models).
- `<newfeature_shortname>_with_<input_type>.py`: The file demonstrating your feature.
  Replace \<new_feature_name> with the name of your feature and \<input_type> with the type of input it uses (e.g., txt, pdf, etc.).
  This file should contain well-commented code and demonstrate the core functionality of your feature using a practical example.
- `test_<new_feature_name>_examples.py`: Unit tests for your feature using pytest. Ensure comprehensive test coverage.
- `noxfile_config.py`: Configuration file for running CICD tests.
- `requirements.txt`: Lists the all dependencies for your feature. Include google-genai and any other necessary libraries.
- `requirements-test.txt`: Lists dependencies required for testing your feature. Include packages like pytest.

If the feature name is `Hello World` and it has example that takes username input to greet user, then the structure would look like this:

```
genai/
└── hello_world/
    ├── noxfile_config.py
    ├── requirements-test.txt
    ├── requirements.txt
    ├── helloworld_with_txt.py
    └── test_hello_world_examples.py
```

Notable:

- The folder name and test file use the full feature name as `hello_world`
- The sample file use the feature `helloworld` but in a short condensed form.
  (This is required for internal automation purposes.)

To improve your understanding, refer to the existing folders lik [count_tokens](../count_tokens) and
[text_generation](../text_generation).
