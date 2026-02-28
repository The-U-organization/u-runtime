# U Runtime

Minimal interpreted language implemented in Python.

## Run

```bash
python3 main.py test.u
```

Or run any source file:

```bash
python3 main.py path/to/file.u
```

## Language Overview

`U` currently supports:

- Integer literals (`123`)
- Boolean literals (`true`, `false`)
- Arithmetic: `+`
- Comparisons: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Variable declarations:
  - `var name = expr;` (global scope)
  - `let name = expr;` (block scope only)
- Variable access by identifier
- `print(expr);`
- Blocks: `{ ... }`
- Branching: `if (condition) statement` with optional `else statement`

## Semantics

- `var` writes into a global environment.
- `let` is only valid inside a block and writes into the current block scope.
- Name lookup checks innermost block scope first, then global scope.
- Blocks create a new scope frame; nested blocks can shadow names.
- `if` executes `then` when condition is truthy, otherwise optional `else`.
- Any statement can be used as an `if` branch (single statement or block).

## Formal Syntax (EBNF)

```ebnf
program         = { statement } ;

statement       = block
                | var_decl
                | let_decl
                | if_stmt
                | print_stmt ;

block           = "{" , { statement } , "}" ;

var_decl        = "var" , IDENT , "=" , expression , ";" ;
let_decl        = "let" , IDENT , "=" , expression , ";" ;

if_stmt         = "if" , "(" , expression , ")" , statement ,
                  [ "else" , statement ] ;

print_stmt      = "print" , "(" , expression , ")" , ";" ;

expression      = comparison ;

comparison      = addition ,
                  { ( "==" | "!=" | "<" | "<=" | ">" | ">=" ) , addition } ;

addition        = primary , { "+" , primary } ;

primary         = NUMBER
                | IDENT
                | "true"
                | "false"
                | "(" , expression , ")" ;
```

## Lexical Rules

Tokenizer tokens:

- `EQEQ` (`==`)
- `NEQ` (`!=`)
- `LTE` (`<=`)
- `GTE` (`>=`)
- `LT` (`<`)
- `GT` (`>`)
- `NUMBER` (`\d+`)
- `IDENT` (`[a-zA-Z_][a-zA-Z0-9_]*`)
- `PLUS` (`+`)
- `LBRACE` (`{`)
- `RBRACE` (`}`)
- `LPAREN` (`(`)
- `RPAREN` (`)`)
- `SEMICOLON` (`;`)
- `EQUAL` (`=`)
- `SKIP` (`[ \t\r\n]+`)

## Notes and Current Limits

- Only integer numbers are supported.
- No subtraction/multiplication/division yet.
- No assignment after declaration yet (for example `x = 2;` is not supported).
- `let` at top-level raises: `'let' can only be declared inside a block`.
- `true` and `false` are treated as boolean literals by the parser.

## Example

```u
var x = 10;

if ((x + 2) >= 12) {
  print(true);
  {
    let x = 1;
    print(x + 5);
  }
  print(x);
} else {
  print(false);
}
```

