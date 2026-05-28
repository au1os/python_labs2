"""
Модуль содержит функции для сохранения и загрузки данных коллекции квартир.
Использует JSON формат для хранения данных.

Функциональность модуля:
1. Сериализация объектов Apartment в JSON (apartment_to_dict)
2. Десериализация из JSON в объекты Apartment (dict_to_apartment)
3. Сохранение коллекции в файл (save)
4. Загрузка коллекции из файла (load)
5. Очистка хранилища (clear)
6. Получение информации о хранилище (get_storage_info)

Структура JSON файла:
[
  {
    "area": 50.0,
    "price": 100000,
    "address": "ул. Примерная, д.1, кв.10",
    "rent_duration": 12,
    "is_rented": false
  },
  ...
]
"""

import json  # Модуль для работы с JSON форматом
import os  # Модуль для работы с операционной системой
from typing import List, Dict, Any  # Аннотации типов
from pathlib import Path  # Модуль для работы с путями файлов
import sys  # Модуль для доступа к системным параметрам

# Добавляем путь к lab01 для импорта базового класса Apartment
# Это необходимо, чтобы использовать класс Apartment из первой лабораторной
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

# Импортируем класс Apartment из первой лабораторной работы
from model import Apartment
# Импортируем исключение для ошибок хранилища
from exceptions import StorageError

# Путь к файлу хранения данных по умолчанию
# Файл будет создан в поддиректории "data" текущей директории
DEFAULT_STORAGE_PATH = Path(__file__).parent / "data" / "apartments.json"


def apartment_to_dict(apartment: Apartment) -> Dict[str, Any]:
    """
    Преобразует объект Apartment в словарь для сериализации в JSON.
    
    Этот метод необходим, потому что объекты Apartment нельзя напрямую
    сохранить в JSON - нужно преобразовать их в словари.
    
    Args:
        apartment: Объект квартиры, который нужно сериализовать
        
    Returns:
        Dict[str, Any]: Словарь, содержащий все необходимые данные о квартире:
            - area: площадь (float)
            - price: цена (float)
            - address: адрес (str)
            - rent_duration: срок аренды (int)
            - is_rented: статус аренды (bool)
    """
    # Создаём словарь с данными квартиры
    # Используем свойства (properties) класса Apartment для получения значений
    return {
        "area": apartment.area,  # Площадь квартиры
        "price": apartment.price,  # Цена аренды
        "address": apartment.address,  # Адрес квартиры
        "rent_duration": apartment.rent_duration,  # Срок аренды в месяцах
        "is_rented": apartment.is_rented  # Флаг: арендована или нет
    }


def dict_to_apartment(data: Dict[str, Any]) -> Apartment:
    """
    Преобразует словарь (из JSON) в объект Apartment.
    
    Этот метод выполняет обратную операцию к apartment_to_dict -
    создаёт объект Apartment из данных, загруженных из JSON файла.
    
    Args:
        data: Словарь с данными квартиры, загруженный из JSON
        
    Returns:
        Apartment: Созданный объект квартиры
        
    Raises:
        StorageError: Если в словаре отсутствуют обязательные поля
                     или данные имеют некорректный тип
    """
    try:
        # Создаём объект Apartment, передавая данные из словаря
        # Преобразуем значения к нужным типам (float, int, str)
        return Apartment(
            area=float(data["area"]),  # Преобразуем площадь к float
            price=float(data["price"]),  # Преобразуем цену к float
            address=str(data["address"]),  # Преобразуем адрес к str
            rent_duration=int(data["rent_duration"])  # Преобразуем срок к int
        )
    except (KeyError, TypeError, ValueError) as e:
        # Если произошло исключение при преобразовании данных,
        # выбрасываем StorageError с подробным сообщением
        raise StorageError("load", f"Некорректные данные квартиры: {e}")


def save(collection: Any, filepath: Path = DEFAULT_STORAGE_PATH) -> None:
    """
    Сохраняет коллекцию квартир в JSON-файл.
    
    Алгоритм работы:
    1. Создаёт директорию для файла, если она не существует
    2. Преобразует каждый объект Apartment в словарь
    3. Записывает список словарей в JSON файл
    
    Args:
        collection: Коллекция квартир (любой итерируемый объект)
        filepath: Путь к файлу для сохранения (по умолчанию DEFAULT_STORAGE_PATH)
        
    Raises:
        StorageError: Если возникла ошибка при создании директории
                     или записи в file
    """
    try:
        # Создаём директорию, если она не существует
        # parents=True - создаёт все промежуточные директории
        # exist_ok=True - не выбрасывает ошибку, если директория уже существует
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Преобразуем коллекцию в список словарей
        # Каждый объект Apartment преобразуется в словарь через apartment_to_dict
        apartments_data = []
        for apartment in collection:
            # Добавляем словарь с данными каждой квартиры в список
            apartments_data.append(apartment_to_dict(apartment))
        
        # Сохраняем список словарей в JSON файл
        # encoding="utf-8" - для поддержки кириллицы
        # ensure_ascii=False - чтобы кириллица сохранялась как есть, а не как \uXXXX
        # indent=2 - для красивого форматирования (отступ 2 пробела)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(apartments_data, f, ensure_ascii=False, indent=2)
            
    except (IOError, OSError) as e:
        # Обрабатываем ошибки ввода-вывода (нет прав, диск заполнен и т.д.)
        raise StorageError("save", f"Не удалось сохранить данные: {e}")
    except Exception as e:
        # Обрабатываем любые другие неожиданные исключения
        raise StorageError("save", f"Неожиданная ошибка: {e}")


def load(filepath: Path = DEFAULT_STORAGE_PATH) -> List[Apartment]:
    """
    Загружает список квартир из JSON-файла.
    
    Алгоритм работы:
    1. Проверяет существование file
    2. Читает JSON данные из file
    3. Преобразует каждый словарь в объект Apartment
    4. Возвращает список объектов
    
    Args:
        filepath: Путь к файлу для загрузения (по умолчанию DEFAULT_STORAGE_PATH)
        
    Returns:
        List[Apartment]: Список загруженных объектов Apartment
                        Пустой список, если файл не существует
        
    Raises:
        StorageError: Если файл повреждён, имеет некорректный формат
                     или данные не могут быть преобразованы
    """
    try:
        # Если файл не существует, возвращаем пустой список
        # Это нормальная ситуация при первом запуске приложения
        if not filepath.exists():
            return []  # Возвращаем пустой список, если файл не существует
        
        # Открываем и читаем JSON файл
        with open(filepath, "r", encoding="utf-8") as f:
            # Загружаем JSON данные
            data = json.load(f)
        
        # Проверяем, что данные являются списком
        # JSON файл должен содержать массив объектов
        if not isinstance(data, list):
            raise StorageError("load", "Ожидался список квартир в JSON")
        
        # Преобразуем каждый словарь в объект Apartment
        apartments = []
        for item in data:
            # Проверяем, что каждый элемент - словарь
            if not isinstance(item, dict):
                raise StorageError("load", "Каждая квартира должна быть объектом JSON")
            # Преобразуем словарь в объект Apartment
            apartments.append(dict_to_apartment(item))
        
        # Возвращаем список объектов Apartment
        return apartments
        
    except json.JSONDecodeError as e:
        # Обрабатываем ошибку некорректного JSON формата
        raise StorageError("load", f"Некорректный JSON формат: {e}")
    except StorageError:
        # Если уже произошло StorageError, просто передаём его дальше
        raise
    except (IOError, OSError) as e:
        # Обрабатываем ошибки ввода-вывода (нет прав, файл повреждён)
        raise StorageError("load", f"Не удалось загрузить данные: {e}")


def clear(filepath: Path = DEFAULT_STORAGE_PATH) -> None:
    """
    Очищает файл хранения (удаляет все data).
    
    Используется для полного сброса хранилища данных.
    
    Args:
        filepath: Путь к файлу, который нужно очистить
        
    Raises:
        StorageError: Если не удалось удалить файл
    """
    try:
        # Если файл существует, удаляем его
        if filepath.exists():
            filepath.unlink()  # unlink() удаляет файл
    except OSError as e:
        # Обрабатываем ошибки операционной системы
        raise StorageError("clear", f"Не удалось очистить файл: {e}")


def get_storage_info(filepath: Path = DEFAULT_STORAGE_PATH) -> Dict[str, Any]:
    """
    Возвращает информацию о хранилище данных.
    
    Используется для отладки и отображения информации о file.
    
    Args:
        filepath: Путь к файлу хранилища
        
    Returns:
        Dict[str, Any]: Словарь с информацией о хранилище:
            - exists: существует ли файл (bool)
            - path: полный путь к файлу (str)
            - size: размер файла в байтах (int)
            - apartments_count: количество квартир в file (int)
    """
    # Создаём словарь с базовой информацией
    info = {
        "exists": filepath.exists(),  # Проверяем существование file
        "path": str(filepath),  # Преобразуем Path в строку
        "size": 0,  # Размер файла (по умолчанию 0)
        "apartments_count": 0  # Количество квартир (по умолчанию 0)
    }
    
    # Если файл существует, получаем дополнительную информацию
    if filepath.exists():
        try:
            # Получаем размер file в байтах
            info["size"] = filepath.stat().st_size
            
            # Пытаемся загрузить данные и посчитать количество квартир
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Если данные являются списком, считаем количество элементов
                if isinstance(data, list):
                    info["apartments_count"] = len(data)
        except (json.JSONDecodeError, OSError):
            # Если произошла ошибка при чтении, оставляем значения по умолчанию
            pass
    
    # Возвращаем словарь с информацией
    return info
