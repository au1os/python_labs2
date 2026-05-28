"""
Модуль импортирует класс Apartment из лабораторной работы №1.
Это соответствует требованию использовать тот же вариант предметной области.
"""

import sys
from pathlib import Path

# Добавляем путь к lab01 для импорта
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment

__all__ = ["Apartment"]