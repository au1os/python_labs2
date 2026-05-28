"""
Модуль содержит обновлённый класс ApartmentCollection с поддержкой интерфейсов.
Коллекция теперь работает через интерфейсы IPrintable, IComparable, IRentable, IFilterable.
"""

from typing import List, Iterator, Optional, Callable, Union, Type
from interfaces import IPrintable, IComparable, IRentable, IFilterable
from models import ApartmentBase, StudioApartment, LuxuryApartment


class ApartmentCollection(IFilterable):
    """
    Контейнерный класс для хранения и управления коллекцией квартир.
    Реализует интерфейс IFilterable для поддержки фильтрации.
    """
    
    def __init__(self):
        """Инициализирует пустую коллекцию квартир."""
        self._items: List[ApartmentBase] = []
    
    def add(self, item: ApartmentBase) -> None:
        """
        Добавляет объект ApartmentBase (или его наследника) в коллекцию.
        
        Args:
            item (ApartmentBase): Объект квартиры для добавления
            
        Raises:
            TypeError: Если передан объект неверного типа
            ValueError: Если квартира с таким же адресом и площадью уже существует
        """
        if not isinstance(item, ApartmentBase):
            raise TypeError(f"Можно добавлять только объекты ApartmentBase или их наследников. Получен {type(item).__name__}")
        
        # Проверка на дубликат
        if item in self._items:
            raise ValueError(f"Квартира с адресом '{item.address}' и площадью {item.area} м² уже существует в коллекции")
        
        self._items.append(item)
    
    def remove(self, item: ApartmentBase) -> None:
        """Удаляет объект ApartmentBase из коллекции."""
        if item not in self._items:
            raise ValueError(f"Квартира с адресом '{item.address}' не найдена в коллекции")
        self._items.remove(item)
    
    def remove_at(self, index: int) -> ApartmentBase:
        """Удаляет объект по индексу и возвращает его."""
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} выходит за границы коллекции (размер: {len(self._items)})")
        removed_item = self._items[index]
        del self._items[index]
        return removed_item
    
    def get_all(self) -> List[ApartmentBase]:
        """Возвращает список всех объектов в коллекции (реализация IFilterable)."""
        return self._items.copy()
    
    def filter_by(self, predicate) -> 'ApartmentCollection':
        """
        Фильтрует элементы коллекции по заданному предикату (реализация IFilterable).
        
        Args:
            predicate: Функция, принимающая элемент и возвращающая bool
            
        Returns:
            ApartmentCollection: Новая коллекция с отфильтрованными элементами
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if predicate(item):
                new_collection.add(item)
        return new_collection
    
    def find_by_address(self, address: str) -> Optional[ApartmentBase]:
        """Находит квартиру по адресу."""
        for item in self._items:
            if address.lower() in item.address.lower():
                return item
        return None
    
    def find_by_price_range(self, min_price: float, max_price: float) -> List[ApartmentBase]:
        """Находит квартиры в ценовом диапазоне."""
        return [item for item in self._items if min_price <= item.price <= max_price]
    
    def find_by_area_range(self, min_area: float, max_area: float) -> List[ApartmentBase]:
        """Находит квартиры в диапазоне площади."""
        return [item for item in self._items if min_area <= item.area <= max_area]
    
    # Методы для работы с типами
    def get_only_studios(self) -> 'ApartmentCollection':
        """Возвращает новую коллекцию только с квартирами-студиями."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if isinstance(item, StudioApartment):
                new_collection.add(item)
        return new_collection
    
    def get_only_luxury(self) -> 'ApartmentCollection':
        """Возвращает новую коллекцию только с элитными квартирами."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if isinstance(item, LuxuryApartment):
                new_collection.add(item)
        return new_collection
    
    def get_only_basic(self) -> 'ApartmentCollection':
        """Возвращает новую коллекцию только с базовыми квартирами."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if type(item) is ApartmentBase:
                new_collection.add(item)
        return new_collection
    
    def get_by_type(self, apartment_type: Type[ApartmentBase]) -> 'ApartmentCollection':
        """Возвращает новую коллекцию с квартирами указанного типа."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if isinstance(item, apartment_type):
                new_collection.add(item)
        return new_collection
    
    # Методы для работы с интерфейсами
    def get_printable(self) -> List[IPrintable]:
        """
        Возвращает список объектов, реализующих интерфейс IPrintable.
        
        Returns:
            List[IPrintable]: Список печатаемых объектов
        """
        return [item for item in self._items if isinstance(item, IPrintable)]
    
    def get_comparable(self) -> List[IComparable]:
        """
        Возвращает список объектов, реализующих интерфейс IComparable.
        
        Returns:
            List[IComparable]: Список сравниваемых объектов
        """
        return [item for item in self._items if isinstance(item, IComparable)]
    
    def get_rentable(self) -> List[IRentable]:
        """
        Возвращает список объектов, реализующих интерфейс IRentable.
        
        Returns:
            List[IRentable]: Список арендуемых объектов
        """
        return [item for item in self._items if isinstance(item, IRentable)]
    
    def count_by_type(self) -> dict:
        """Подсчитывает количество квартир каждого типа."""
        counts = {"basic": 0, "studio": 0, "luxury": 0}
        
        for item in self._items:
            if isinstance(item, StudioApartment):
                counts["studio"] += 1
            elif isinstance(item, LuxuryApartment):
                counts["luxury"] += 1
            else:
                counts["basic"] += 1
        
        return counts
    
    # Универсальные функции, работающие через интерфейсы
    def print_all_items(self) -> None:
        """
        Выводит информацию обо всех объектах коллекции.
        Использует интерфейс IPrintable.
        """
        for item in self._items:
            if isinstance(item, IPrintable):
                item.print_info()
                print()
    
    def sort_by_comparison(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию, используя интерфейс IComparable.
        
        Args:
            reverse (bool): Если True, сортировка по убыванию
        """
        self._items.sort(key=lambda x: x, reverse=reverse)
    
    def get_available_rentals(self) -> List[IRentable]:
        """
        Возвращает список доступных для аренды объектов.
        Использует интерфейс IRentable.
        
        Returns:
            List[IRentable]: Список доступных объектов
        """
        return [item for item in self._items if isinstance(item, IRentable) and item.is_available()]
    
    def calculate_total_rental_income(self) -> float:
        """
        Расчёт общего месячного дохода от аренды.
        Использует интерфейс IRentable.
        
        Returns:
            float: Общая сумма месячного дохода
        """
        total = 0.0
        for item in self._items:
            if isinstance(item, IRentable) and item.is_available():
                total += item.get_rental_price()
        return total
    
    def __len__(self) -> int:
        """Возвращает количество объектов в коллекции."""
        return len(self._items)
    
    def __iter__(self) -> Iterator[ApartmentBase]:
        """Возвращает итератор по коллекции."""
        return iter(self._items)
    
    def __getitem__(self, index: int) -> ApartmentBase:
        """Возвращает объект по индексу."""
        return self._items[index]
    
    def sort_by_price(self, reverse: bool = False) -> None:
        """Сортирует коллекцию по цене."""
        self._items.sort(key=lambda x: x.price, reverse=reverse)
    
    def sort_by_area(self, reverse: bool = False) -> None:
        """Сортирует коллекцию по площади."""
        self._items.sort(key=lambda x: x.area, reverse=reverse)
    
    def sort_by_rent_duration(self, reverse: bool = False) -> None:
        """Сортирует коллекцию по сроку аренды."""
        self._items.sort(key=lambda x: x.rent_duration, reverse=reverse)
    
    def sort(self, key: Callable[[ApartmentBase], any], reverse: bool = False) -> None:
        """Универсальная сортировка по заданному ключу."""
        self._items.sort(key=key, reverse=reverse)
    
    def get_available(self) -> 'ApartmentCollection':
        """Возвращает новую коллекцию со свободными квартирами."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if not item.is_rented:
                new_collection.add(item)
        return new_collection
    
    def get_rented(self) -> 'ApartmentCollection':
        """Возвращает новую коллекцию с арендованными квартирами."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if item.is_rented:
                new_collection.add(item)
        return new_collection
    
    def get_expensive(self, threshold: float) -> 'ApartmentCollection':
        """Возвращает новую коллекцию с квартирами дороже заданного порога."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if item.price > threshold:
                new_collection.add(item)
        return new_collection
    
    def get_by_rent_duration(self, duration: int) -> 'ApartmentCollection':
        """Возвращает новую коллекцию с квартирами на заданный срок аренды."""
        new_collection = ApartmentCollection()
        for item in self._items:
            if item.rent_duration == duration:
                new_collection.add(item)
        return new_collection
    
    def __str__(self) -> str:
        """Возвращает строковое представление коллекции."""
        if not self._items:
            return "Коллекция пуста (0 квартир)"
        
        result = f"Коллекция квартир ({len(self._items)} шт.):\n"
        for i, item in enumerate(self._items, 1):
            if isinstance(item, StudioApartment):
                apt_type = "Студия"
            elif isinstance(item, LuxuryApartment):
                apt_type = "Элитная"
            else:
                apt_type = "Базовая"
            
            result += f"{i}. [{apt_type}] {item.address} - {item.area} м², {item.price:,.2f} руб.\n"
        return result.strip()
    
    def __repr__(self) -> str:
        """Возвращает техническое представление коллекции."""
        return f"ApartmentCollection(items={len(self._items)})"