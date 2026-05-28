"""
Модуль содержит обновлённый класс ApartmentCollection с поддержкой
функциональных методов (map, filter, sort с функциями как аргументами).
"""

from typing import List, Iterator, Optional, Callable, Union, Type, Any
import sys
from pathlib import Path

# Добавляем путь к lab01 для импорта базового класса
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment


class ApartmentCollection:
    """
    Контейнерный класс для хранения и управления коллекцией квартир.
    Поддерживает функциональные методы: sort_by(), filter_by(), apply(), map().
    """
    
    def __init__(self, items: Optional[List[Apartment]] = None):
        """
        Инициализирует коллекцию квартир.
        
        Args:
            items: Опциональный начальный список квартир
        """
        self._items: List[Apartment] = []
        if items:
            for item in items:
                self.add(item)
    
    def add(self, item: Apartment) -> None:
        """
        Добавляет объект Apartment в коллекцию.
        
        Args:
            item (Apartment): Объект квартиры для добавления
            
        Raises:
            TypeError: Если передан объект неверного типа
            ValueError: Если квартира с таким же адресом и площадью уже существует
        """
        if not isinstance(item, Apartment):
            raise TypeError(f"Можно добавлять только объекты Apartment. Получен {type(item).__name__}")
        
        # Проверка на дубликат
        if item in self._items:
            raise ValueError(f"Квартира с адресом '{item.address}' и площадью {item.area} м² уже существует в коллекции")
        
        self._items.append(item)
    
    def remove(self, item: Apartment) -> None:
        """Удаляет объект Apartment из коллекции."""
        if item not in self._items:
            raise ValueError(f"Квартира с адресом '{item.address}' не найдена в коллекции")
        self._items.remove(item)
    
    def remove_at(self, index: int) -> Apartment:
        """Удаляет объект по индексу и возвращает его."""
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} выходит за границы коллекции (размер: {len(self._items)})")
        removed_item = self._items[index]
        del self._items[index]
        return removed_item
    
    def get_all(self) -> List[Apartment]:
        """Возвращает список всех объектов в коллекции."""
        return self._items.copy()
    
    # ========================================================================
    # Функциональные методы (требования ЛР-5)
    # ========================================================================
    
    def sort_by(self, key_func: Callable[[Apartment], Any], reverse: bool = False) -> 'ApartmentCollection':
        """
        Сортирует коллекцию по заданному ключу и возвращает новую коллекцию.
        
        Args:
            key_func: Функция, возвращающая ключ для сортировки
            reverse: Если True, сортировка по убыванию
            
        Returns:
            ApartmentCollection: Новая отсортированная коллекция
        """
        sorted_items = sorted(self._items, key=key_func, reverse=reverse)
        return ApartmentCollection(sorted_items)
    
    def filter_by(self, predicate: Callable[[Apartment], bool]) -> 'ApartmentCollection':
        """
        Фильтрует элементы коллекции по заданному предикату.
        
        Args:
            predicate: Функция, принимающая элемент и возвращающая bool
            
        Returns:
            ApartmentCollection: Новая коллекция с отфильтрованными элементами
        """
        filtered_items = list(filter(predicate, self._items))
        return ApartmentCollection(filtered_items)
    
    def apply(self, func: Callable[[Apartment], Any]) -> List[Any]:
        """
        Применяет функцию к каждому элементу коллекции.
        
        Args:
            func: Функция для применения к каждому элементу
            
        Returns:
            List[Any]: Список результатов применения функции
        """
        return [func(item) for item in self._items]
    
    def map(self, func: Callable[[Apartment], Any]) -> List[Any]:
        """
        Преобразует каждый элемент коллекции с помощью функции.
        Алиас для apply().
        
        Args:
            func: Функция для преобразования каждого элемента
            
        Returns:
            List[Any]: Список преобразованных значений
        """
        return list(map(func, self._items))
    
    def find_by(self, predicate: Callable[[Apartment], bool]) -> Optional[Apartment]:
        """
        Находит первый элемент, удовлетворяющий предикату.
        
        Args:
            predicate: Функция-предикат
            
        Returns:
            Optional[Apartment]: Найденный элемент или None
        """
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    # ========================================================================
    # Методы для работы с типами
    # ========================================================================
    
    def count_by_type(self) -> dict:
        """Подсчитывает количество квартир каждого типа."""
        counts = {"Apartment": 0}
        
        for item in self._items:
            type_name = type(item).__name__
            counts[type_name] = counts.get(type_name, 0) + 1
        
        return counts
    
    def __len__(self) -> int:
        """Возвращает количество объектов в коллекции."""
        return len(self._items)
    
    def __iter__(self) -> Iterator[Apartment]:
        """Возвращает итератор по коллекции."""
        return iter(self._items)
    
    def __getitem__(self, index: int) -> Apartment:
        """Возвращает объект по индексу."""
        return self._items[index]
    
    # ========================================================================
    # Методы для совместимости с ЛР-2
    # ========================================================================
    
    def get_available(self) -> 'ApartmentCollection':
        """Возвращает новую коллекцию со свободными квартирами."""
        return self.filter_by(lambda x: not x.is_rented)
    
    def get_rented(self) -> 'ApartmentCollection':
        """Возвращает новую коллекцию с арендованными квартирами."""
        return self.filter_by(lambda x: x.is_rented)
    
    def get_expensive(self, threshold: float) -> 'ApartmentCollection':
        """Возвращает новую коллекцию с квартирами дороже заданного порога."""
        return self.filter_by(lambda x: x.price > threshold)
    
    def __str__(self) -> str:
        """Возвращает строковое представление коллекции."""
        if not self._items:
            return "Коллекция пуста (0 квартир)"
        
        result = f"Коллекция квартир ({len(self._items)} шт.):\n"
        for i, item in enumerate(self._items, 1):
            result += f"{i}. {item.address} - {item.area} м², {item.price:,.2f} руб.\n"
        return result.strip()
    
    def __repr__(self) -> str:
        """Возвращает техническое представление коллекции."""
        return f"ApartmentCollection(items={len(self._items)})"