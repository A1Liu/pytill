from re import *

#Splits a string based on a regular expression
def splitRegex(expression, regex):
    # if type(expression) != str:
    #     raise TypeError("First argument must be string")
    # if type(regex) != str:
    #     raise TypeError("Second argument must be string")
    # if len(regex) == 0 or len(expression) == 0:
    #     raise ValueError("splitRegex() requires a non-empty pattern match")
    return compile(regex).split(expression)
    #END splitRegex
