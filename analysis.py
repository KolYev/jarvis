import sympy as sp

def calculate(expression):
    try:
        result = sp.sympify(expression, evaluate=True)
        return str(result.evalf() if result.free_symbols == set() else result) 
    except Exception as e:
        return f"Ошибка вычисления: {e}"