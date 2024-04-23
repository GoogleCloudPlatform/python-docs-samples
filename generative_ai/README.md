# Generative AI on Google Cloud

Product Page: https://cloud.google.com/ai/generative-ai?hl=en
Code samples: https://cloud.google.com/docs/samples?text=Generative%20AI

## Developer Notes

In developing code samples for Generative AI products, a scripting style format is recommended. It's important to wrap the code samples and region tags to be with in a function definition.

This change is motivated by the desire to provide a code format that can effortlessly integrate with popular data science community tools. These tools include Colab, Jupyter Notebooks, and the IPython shell.

Example:

```python
def create_hello_world_file(filename):
    # [START hello_world_file_creation]
    import os
    
    # TODO(developer): Update and uncomment below code
    # filename = `/tmp/test.txt`
    
    if os.path.isfile(filename):
        print(f'Overriding content in file(name: {filename})!')
    
    with open(filename) as fp:
        fp.write('Hello world!')
    # [END hello_world_file_creation]
```

In Google Cloud documentation page, code sample for region tag `hello_world_file_creation` is shown as below

```python
import os

# TODO(developer): Update and uncomment below code
# filename = `/tmp/test.txt`

if os.path.isfile(filename):
    print(f'Overriding content in file(name: {filename})!')

with open(filename) as fp:
    fp.write('Hello world!')
```






