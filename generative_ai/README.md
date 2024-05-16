# Generative AI on Google Cloud

* Product Page: https://cloud.google.com/ai/generative-ai?hl=en
* Code samples: https://cloud.google.com/docs/samples?text=Generative%20AI

## Samples Style Guide

> If you are new and interested in samples contributions, you are welcome! See the [Contributing Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/README.md).


While developing code samples for Generative AI products, scripting style format
is to be used. So wrap your imports, sample code and region tags to be with
in one function definition. This is to keep the region tag section code to be in
script format and also allowing you to write regular testcases.

This change is motivated by the desire to provide code samples in a copy-paste-run
format that is helpful for popular data science community tools like
Google Colab, Jupyter Notebooks, and IPython shell.

Here is an example code.

```python
def create_hello_world_file(filename):
    # <region tag: starts here>
    import os
    
    # TODO(developer): Update and uncomment below code
    # filename = `/tmp/test.txt`
    
    if os.path.isfile(filename):
        print(f'Overriding content in file(name: {filename})!')
    
    with open(filename) as fp:
        fp.write('Hello world!')
    # <region tag: ends here>
```

In Google Cloud documentation, this code sample will be shown as below

```python
import os

# TODO(developer): Update and uncomment below code
# filename = `/tmp/test.txt`

if os.path.isfile(filename):
    print(f'Overriding content in file(name: {filename})!')

with open(filename) as fp:
    fp.write('Hello world!')
```

**Note:** In the above sample, `imports` are include and `TODO's` are provided to variable
that need to update by users.

