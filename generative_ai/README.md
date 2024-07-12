# Generative AI on Google Cloud

* Product Page: https://cloud.google.com/ai/generative-ai?hl=en
* Code samples: https://cloud.google.com/docs/samples?text=Generative%20AI

## Samples Style Guide

If you are new to this work and interested in samples contributions, use the [Contributing Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/README.md).

For Generative AI samples, these style guide instructions take precedence over [Contributing Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/README.md).

### 1. Use Scripting format

Wrap the imports, sample code and the region tags to be with in one function definition.
This is to keep the region tag section code to be in script format and also allowing you to write regular testcases.

> This change is motivated by the desire to provide code samples in a copy-paste-run
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

### 2. Avoid Hidden Variables

Suggestion to avoid hidden variables in code samples

* Keep the function def as much possible simple.
  * Ex:`def hello() -> str:` is better than `def hello(a=..b=..c=..d=..) -> str:`  
* Defined common variables like PROJECT_ID, LOCATION as global variables.
* Use description variables name
  * Ex: Instead of `user_input` use `text_input`
* Resist the temptation to tell more. 
  * Ex: Don't define unused optional arguments
  * Ex: Use `Read more @ http://` than explaining '..'

Note: Not all the samples are the same. `Avoid Hidden variables` is not same as `Dont/No Hidden Variables`


## Conclusion

To summarize, it's crucial to maintain the simplicity and brevity of your code 
examples.
> The ideal sample is one that appears self-evident and immediately 
comprehensible.



