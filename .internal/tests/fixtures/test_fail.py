# test_fail.py
import sys  # Flake8 Error: 'sys' imported but unused
import os

def calculate_square (number): # Flake8 Error: extra space before opening parenthesis
    
    result=number*number # Flake8 Error: missing whitespace around operator '='
    print('The result is: ' + str(result)) # Black will want to change single quotes to double quotes
    return result 

# Intentional trailing whitespace on the line below to trigger Flake8
