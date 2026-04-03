def validate_positive_float(value, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} должен быть числом (int или float). Получен {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} должен быть положительным (>0). Получено {value}")
    return float(value)

def validate_positive_int(value, name: str) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} должен быть целым числом (int). Получен {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} должен быть положительным (>0). Получено {value}")
    return value

def validate_nonempty_string(value, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} должен быть строкой (str). Получен {type(value).__name__}")
    if not value.strip():
        raise ValueError(f"{name} не может быть пустой строкой или состоять из пробелов")
    return value.strip()