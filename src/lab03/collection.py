"""
Модуль содержит обновлённый класс ApartmentCollection с поддержкой полиморфизма.
Коллекция теперь может хранить разные типы квартир (базовые, студии, элитные)
и предоставляет методы для фильтрации по типам.
"""

from typing import List, Iterator, Optional, Callable, Union, Type
from base import Apartment
from models import StudioApartment, LuxuryApartment


class ApartmentCollection:
    """
    Контейнерный класс для хранения и управления коллекцией квартир.
    Поддерживает полиморфизм - может хранить объекты разных типов,
    наследованных от Apartment.
    
    Атрибуты:
        _items (List[Apartment]): Внутренний список для хранения объектов Apartment
        
    Требования:
        - Хранит множество объектов Apartment (и его наследников)
        - Управляет добавлением и удалением
        - Предоставляет доступ к объектам
        - Позволяет итерироваться по коллекции
        - Проверяет тип добавляемых объектов
        - Не допускает дубликатов (по адресу и площади)
        - Поддерживает фильтрацию по типам квартир
    """
    
    def __init__(self):
        """Инициализирует пустую коллекцию квартир."""
        self._items: List[Apartment] = []
    
    def add(self, item: Apartment) -> None:
        """
        Добавляет объект Apartment (или его наследника) в коллекцию.
        
        Args:
            item (Apartment): Объект квартиры for добавления
            
        Raises:
            TypeError: Если передан объект неверного типа
            ValueError: Если квартира с таким же адресом и площадью уже существует
            
        Requirements:
            - Проверяет тип добавляемого объекта (должен быть Apartment или наследник)
            - Не допускает добавления дубликатов (по критериям __eq__)
        """
        if not isinstance(item, Apartment):
            raise TypeError(f"Можно добавлять только объекты Apartment или их наследников. Получен {type(item).__name__}")
        
        # Проверка на дубликат (используем __eq__ из Apartment)
        if item in self._items:
            raise ValueError(f"Квартира с адресом '{item.address}' и площадью {item.area} м² уже существует в коллекции")
        
        self._items.append(item)
    
    def remove(self, item: Apartment) -> None:
        """
        Удаляет объект Apartment из коллекции.
        
        Args:
            item (Apartment): Объект квартиры для удаления
            
        Raises:
            ValueError: Если объект не найден в коллекции
        """
        if item not in self._items:
            raise ValueError(f"Квартира с адресом '{item.address}' не найдена в коллекции")
        
        self._items.remove(item)
    
    def remove_at(self, index: int) -> Apartment:
        """
        Удаляет объект по индексу и возвращает его.
        
        Args:
            index (int): Индекс удаляемого объекта
            
        Returns:
            Apartment: Удалённый объект
            
        Raises:
            IndexError: Если индекс выходит за границы коллекции
        """
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} выходит за границы коллекции (размер: {len(self._items)})")
        
        removed_item = self._items[index]
        del self._items[index]
        return removed_item
    
    def get_all(self) -> List[Apartment]:
        """
        Возвращает список всех объектов в коллекции.
        
        Returns:
            List[Apartment]: Копия списка всех квартир
        """
        return self._items.copy()
    
    def find_by_address(self, address: str) -> Optional[Apartment]:
        """
        Находит квартиру по адресу (полное или частичное совпадение).
        
        Args:
            address (str): Адрес для поиска
            
        Returns:
            Optional[Apartment]: Найденная квартира или None
        """
        for item in self._items:
            if address.lower() in item.address.lower():
                return item
        return None
    
    def find_by_price_range(self, min_price: float, max_price: float) -> List[Apartment]:
        """
        Находит квартиры в ценовом диапазоне.
        
        Args:
            min_price (float): Минимальная цена
            max_price (float): Максимальная цена
            
        Returns:
            List[Apartment]: Список квартир в заданном ценовом диапазоне
        """
        return [item for item in self._items if min_price <= item.price <= max_price]
    
    def find_by_area_range(self, min_area: float, max_area: float) -> List[Apartment]:
        """
        Находит квартиры в диапазоне площади.
        
        Args:
            min_area (float): Минимальная площадь
            max_area (float): Максимальная площадь
            
        Returns:
            List[Apartment]: Список квартир в заданном диапазоне площади
        """
        return [item for item in self._items if min_area <= item.area <= max_area]
    
    # Методы для работы с типами (полиморфизм)
    def get_only_studios(self) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию только с квартирами-студиями.
        
        Returns:
            ApartmentCollection: Коллекция, содержащая только студии
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if isinstance(item, StudioApartment):
                new_collection.add(item)
        return new_collection
    
    def get_only_luxury(self) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию только с элитными квартирами.
        
        Returns:
            ApartmentCollection: Коллекция, содержащая только элитные квартиры
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if isinstance(item, LuxuryApartment):
                new_collection.add(item)
        return new_collection
    
    def get_only_basic(self) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию только с базовыми квартирами (не студии и не элитные).
        
        Returns:
            ApartmentCollection: Коллекция, содержащая только базовые квартиры
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            # Базовые - это те, которые не являются студиями или элитными
            if type(item) is Apartment:
                new_collection.add(item)
        return new_collection
    
    def get_by_type(self, apartment_type: Type[Apartment]) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию с квартирами указанного типа.
        
        Args:
            apartment_type (Type[Apartment]): Тип квартиры (Apartment, StudioApartment, LuxuryApartment)
            
        Returns:
            ApartmentCollection: Коллекция квартир указанного типа
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if isinstance(item, apartment_type):
                new_collection.add(item)
        return new_collection
    
    def count_by_type(self) -> dict:
        """
        Подсчитывает количество квартир каждого типа.
        
        Returns:
            dict: Словарь с количеством квартир каждого типа
        """
        counts = {
            "basic": 0,
            "studio": 0,
            "luxury": 0
        }
        
        for item in self._items:
            if isinstance(item, StudioApartment):
                counts["studio"] += 1
            elif isinstance(item, LuxuryApartment):
                counts["luxury"] += 1
            else:
                counts["basic"] += 1
        
        return counts
    
    def __len__(self) -> int:
        """
        Возвращает количество объектов в коллекции.
        
        Returns:
            int: Количество квартир в коллекции
        """
        return len(self._items)
    
    def __iter__(self) -> Iterator[Apartment]:
        """
        Возвращает итератор по коллекции.
        
        Returns:
            Iterator[Apartment]: Итератор по объектам Apartment
        """
        return iter(self._items)
    
    def __getitem__(self, index: int) -> Apartment:
        """
        Возвращает объект по индексу (поддержка индексации).
        
        Args:
            index (int): Индекс объекта (поддерживает отрицательные индексы)
            
        Returns:
            Apartment: Объект квартиры по заданному индексу
            
        Raises:
            IndexError: Если индекс выходит за границы коллекции
        """
        return self._items[index]
    
    def sort_by_price(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по цене.
        
        Args:
            reverse (bool): Если True, сортировка по убыванию
        """
        self._items.sort(key=lambda x: x.price, reverse=reverse)
    
    def sort_by_area(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по площади.
        
        Args:
            reverse (bool): Если True, сортировка по убыванию
        """
        self._items.sort(key=lambda x: x.area, reverse=reverse)
    
    def sort_by_rent_duration(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по сроку аренды.
        
        Args:
            reverse (bool): Если True, сортировка по убыванию
        """
        self._items.sort(key=lambda x: x.rent_duration, reverse=reverse)
    
    def sort(self, key: Callable[[Apartment], any], reverse: bool = False) -> None:
        """
        Универсальная сортировка по заданному ключу.
        
        Args:
            key (Callable[[Apartment], any]): Функция, возвращающая ключ для сортировки
            reverse (bool): Если True, сортировка по убыванию
        """
        self._items.sort(key=key, reverse=reverse)
    
    def get_available(self) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию со свободными квартирами.
        
        Returns:
            ApartmentCollection: Коллекция свободных квартир
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if not item.is_rented:
                new_collection.add(item)
        return new_collection
    
    def get_rented(self) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию с арендованными квартирами.
        
        Returns:
            ApartmentCollection: Коллекция арендованных квартир
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if item.is_rented:
                new_collection.add(item)
        return new_collection
    
    def get_expensive(self, threshold: float) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию с квартирами дороже заданного порога.
        
        Args:
            threshold (float): Порог стоимости
            
        Returns:
            ApartmentCollection: Коллекция дорогих квартир
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if item.price > threshold:
                new_collection.add(item)
        return new_collection
    
    def get_by_rent_duration(self, duration: int) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию с квартирами на заданный срок аренды.
        
        Args:
            duration (int): Срок аренды в месяцах
            
        Returns:
            ApartmentCollection: Коллекция квартир с заданным сроком аренды
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if item.rent_duration == duration:
                new_collection.add(item)
        return new_collection
    
    def calculate_total_monthly_income(self) -> float:
        """
        Расчёт общего месячного дохода от всех квартир.
        Использует полиморфный метод calculate_monthly_payment().
        
        Returns:
            float: Общая сумма месячного дохода
        """
        total = 0.0
        for item in self._items:
            if not item.is_rented:  # Считаем только свободные квартиры
                total += item.calculate_monthly_payment()
        return total
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление коллекции.
        
        Returns:
            str: Информация о коллекции (количество и список квартир)
        """
        if not self._items:
            return "Коллекция пуста (0 квартир)"
        
        result = f"Коллекция квартир ({len(self._items)} шт.):\n"
        for i, item in enumerate(self._items, 1):
            # Определяем тип квартиры
            if isinstance(item, StudioApartment):
                apt_type = "Студия"
            elif isinstance(item, LuxuryApartment):
                apt_type = "Элитная"
            else:
                apt_type = "Базовая"
            
            result += f"{i}. [{apt_type}] {item.address} - {item.area} м², {item.price:,.2f} руб.\n"
        return result.strip()
    
    def __repr__(self) -> str:
        """
        Возвращает техническое представление коллекции.
        
        Returns:
            str: Техническое представление
        """
        return f"ApartmentCollection(items={len(self._items)})"