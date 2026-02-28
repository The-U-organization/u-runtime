import sys
from u.tokenizer import tokenize
from u.parser import parse
from u.interpreter import evaulate  

if len(sys.argv) != 2:
    print("Usage: python main.py <source_file>")
    sys.exit(1)

filename = sys.argv[1]
code = open(filename).read()
tokens = tokenize(code)
ast = parse(tokens)
program = parse(tokens)
for stmt in program:
    evaulate(stmt)