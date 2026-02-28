# u/tokenizer.py

import re

TOKEN_SPEC = [
    ("EQEQ", r"=="),
    ("NEQ", r"!="),
    ("LTE", r"<="),
    ("GTE", r">="),
    ("LT", r"<"),
    ("GT", r">"),
    ("NUMBER", r"\d+"),
    ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("PLUS", r"\+"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SEMICOLON", r";"),
    ("EQUAL", r"="),
    ("SKIP", r"[ \t\r\n]+"),
]
def tokenize(code):
    tokens = []
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind != "SKIP":
            tokens.append((kind, value))
    return tokens
