import re

text = input("Please enter text: ")
# tokens = text.split()

tokens = re.findall(r"\w+|[^\w\s]", text)
print (tokens)