class Number:
    def __init__(self, value):
        self.value = int(value)

class Boolean:
    def __init__(self, value):
        self.value = value

class BinaryOp:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Print:
    def __init__(self, expr):
        self.expr = expr

class VarDecl:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class LetDecl:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarAccess:
    def __init__(self, name):
        self.name = name

class Block:
    def __init__(self, statements):
        self.statements = statements

class If:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def _peek(self):
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current]

    def _advance(self):
        token = self._peek()
        if token is None:
            raise Exception("Unexpected end of input")
        self.current += 1
        return token

    def _expect(self, token_type=None, token_value=None):
        token = self._advance()
        if token_type is not None and token[0] != token_type:
            raise Exception(f"Expected {token_type}, got {token[0]}")
        if token_value is not None and token[1] != token_value:
            raise Exception(f"Expected '{token_value}', got '{token[1]}'")
        return token

    def parse_program(self):
        statements = []
        while self._peek() is not None:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self._peek()
        if token is None:
            raise Exception("Expected statement, got end of input")

        if token[0] == "LBRACE":
            return self.parse_block()
        if token[1] == "var":
            return self.parse_var_decl()
        if token[1] == "let":
            return self.parse_let_decl()
        if token[1] == "if":
            return self.parse_if()
        if token[1] == "print":
            return self.parse_print()
        raise Exception(f"Unexpected token: {token[1]}")

    def parse_block(self):
        self._expect("LBRACE")
        statements = []
        while self._peek() is not None and self._peek()[0] != "RBRACE":
            statements.append(self.parse_statement())
        self._expect("RBRACE")
        return Block(statements)

    def parse_var_decl(self):
        self._expect(token_value="var")
        name = self._expect("IDENT")[1]
        self._expect("EQUAL")
        value = self.parse_expression()
        self._expect("SEMICOLON")
        return VarDecl(name, value)

    def parse_let_decl(self):
        self._expect(token_value="let")
        name = self._expect("IDENT")[1]
        self._expect("EQUAL")
        value = self.parse_expression()
        self._expect("SEMICOLON")
        return LetDecl(name, value)

    def parse_print(self):
        self._expect(token_value="print")
        self._expect("LPAREN")
        expr = self.parse_expression()
        self._expect("RPAREN")
        self._expect("SEMICOLON")
        return Print(expr)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_if(self):
        self._expect(token_value="if")
        self._expect("LPAREN")
        condition = self.parse_expression()
        self._expect("RPAREN")
        then_branch = self.parse_statement()

        else_branch = None
        if self._peek() is not None and self._peek()[1] == "else":
            self._advance()
            else_branch = self.parse_statement()

        return If(condition, then_branch, else_branch)

    def parse_comparison(self):
        left = self.parse_addition()
        comparison_tokens = {"EQEQ", "NEQ", "LT", "LTE", "GT", "GTE"}
        while self._peek() is not None and self._peek()[0] in comparison_tokens:
            operator = self._advance()[1]
            right = self.parse_addition()
            left = BinaryOp(left, operator, right)
        return left

    def parse_addition(self):
        # Left-associative addition chain: a + b + c
        left = self.parse_primary()
        while self._peek() is not None and self._peek()[0] == "PLUS":
            operator = self._advance()[1]
            right = self.parse_primary()
            left = BinaryOp(left, operator, right)
        return left

    def parse_primary(self):
        token = self._peek()
        if token is None:
            raise Exception("Expected expression, got end of input")

        token_type, token_value = token
        if token_type == "NUMBER":
            self._advance()
            return Number(token_value)
        if token_type == "LPAREN":
            self._advance()
            expr = self.parse_expression()
            self._expect("RPAREN")
            return expr
        if token_type == "IDENT":
            if token_value == "true":
                self._advance()
                return Boolean(True)
            if token_value == "false":
                self._advance()
                return Boolean(False)
            self._advance()
            return VarAccess(token_value)
        raise Exception(f"Expected number or identifier, got: {token_value}")


def parse(tokens):
    return Parser(tokens).parse_program()
