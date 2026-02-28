from u.parser import Number, Boolean, BinaryOp, Print, VarDecl, LetDecl, VarAccess, Block, If

environment = {}
scope_stack = []


def _lookup(name):
    for scope in reversed(scope_stack):
        if name in scope:
            return scope[name]
    if name in environment:
        return environment[name]
    raise Exception(f"Undefined variable: {name}")

def evaulate(node):
    if isinstance(node, Number):
        return node.value
    if isinstance(node, Boolean):
        return node.value
    if isinstance(node, BinaryOp):
        left = evaulate(node.left)
        right = evaulate(node.right)
        if node.operator == "+":
            return left + right
        if node.operator == "==":
            return left == right
        if node.operator == "!=":
            return left != right
        if node.operator == "<":
            return left < right
        if node.operator == "<=":
            return left <= right
        if node.operator == ">":
            return left > right
        if node.operator == ">=":
            return left >= right
        raise Exception(f"Unsupported operator: {node.operator}")
    if isinstance(node, Print):
        print(evaulate(node.expr))
    if isinstance(node, VarDecl):
        value = evaulate(node.value)
        environment[node.name] = value
    if isinstance(node, LetDecl):
        if not scope_stack:
            raise Exception("'let' can only be declared inside a block")
        value = evaulate(node.value)
        scope_stack[-1][node.name] = value
    if isinstance(node, VarAccess):
        return _lookup(node.name)
    if isinstance(node, Block):
        scope_stack.append({})
        try:
            for statement in node.statements:
                evaulate(statement)
        finally:
            scope_stack.pop()
    if isinstance(node, If):
        condition_value = evaulate(node.condition)
        if condition_value:
            evaulate(node.then_branch)
        elif node.else_branch is not None:
            evaulate(node.else_branch)
