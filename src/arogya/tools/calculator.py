import ast
import operator
from langchain.tools import tool

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    else:
        raise TypeError(type(node))

@tool
def calculator(expression: str) -> str:
    try:
        return str(_eval(ast.parse(expression, mode='eval').body))
    except Exception as e:
        return str(e)
