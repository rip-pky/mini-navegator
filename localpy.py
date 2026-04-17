# localpy.py
# Biblioteca local de utilitários para o Zenith Navigator

import ast
from typing import Union


class CalcError(ValueError):
    pass


def _eval_node(node: ast.AST) -> Union[int, float]:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise CalcError("Valor inválido")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise CalcError("Divisão por zero")
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right
        if isinstance(node.op, ast.Mod):
            return left % right
        raise CalcError("Operador não permitido")

    if isinstance(node, ast.UnaryOp):
        value = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +value
        if isinstance(node.op, ast.USub):
            return -value
        raise CalcError("Operador unário inválido")

    raise CalcError("Expressão inválida")


def calculate_expression(expression: str) -> str:
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _eval_node(parsed.body)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except (SyntaxError, CalcError) as exc:
        raise CalcError("Erro na expressão") from exc
