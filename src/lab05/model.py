"""
Модуль импортирует класс Apartment из лабораторной работы №1.
Это соответствует требованию использовать тот же вариант предметной области.
"""

import importlib.util
from pathlib import Path
import sys

# Добавляем lab01 в sys.path, чтобы lab01/model.py мог импортировать validate
lab01_path = Path(__file__).parent.parent / "lab01"
if str(lab01_path) not in sys.path:
    sys.path.insert(0, str(lab01_path))

# Загружаем модуль model.py из lab01 напрямую, чтобы избежать конфликта имен
lab01_model_path = lab01_path / "model.py"
spec = importlib.util.spec_from_file_location("lab01_model", lab01_model_path)
lab01_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab01_model)

# Импортируем класс Apartment из загруженного модуля
Apartment = lab01_model.Apartment

__all__ = ["Apartment"]