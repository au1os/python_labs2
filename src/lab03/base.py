"""
Базовый модуль для лабораторной работы №3.
Импортирует класс Apartment из ЛР-1 и определяет общий интерфейс.
"""

import sys
from pathlib import Path

# Добавляем путь к lab01 для импорта
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment

__all__ = ["Apartment"]