import sympy as sp
import pandas as pd

def calculate(expression):
    try:
        result = sp.sympify(expression, evaluate=True)
        return str(result.evalf() if result.free_symbols == set() else result) 
    except Exception as e:
        return f"Ошибка вычисления: {e}"

def analyze_data(path, operation="describe", column = None):
    try:
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    except Exception as e:
        return f"Не удалось прочитать файл: {e}"

    if operation == "describe":
        return df.describe(include="all").to_string()
    elif operation == "head":
        return df.head(10).to_string()
    elif operation == "correlation":
        return df.corr(numeric_only=True).to_string()
    elif operation == "groupby" and column:
        return df.groupby(column).mean(numeric_only=True).to_string()
    else:
        return "Неизвестная операция или не хватает параметров."


    