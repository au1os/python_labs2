"""
Модуль содержит класс ApartmentCollection - контейнер для хранения объектов Apartment.
Реализует все требования для оценки 5:
- Хранение множества объектов
- Управление добавлением и удалением
- Доступ к объектам
- Итерация по коллекции
- Поиск по атрибутам
- Ограничения на дубликаты
- Индексация
- Сортировка
- Логические операции (фильтрация)
"""

from typing import List, Iterator, Optional, Callable, Union
from model import Apartment


class ApartmentCollection:
    """
    Контейнерный класс для хранения и управления коллекцией квартир.
    
    Атрибуты:
        _items (List[Apartment]): Внутренний список для хранения объектов Apartment
        
    Требования:
        - Хранит множество объектов Apartment
        - Управляет добавлением и удалением
        - Предоставляет доступ к объектам
        - Позволяет итерироваться по коллекции
        - Проверяет тип добавляемых объектов
        - Не допускает дубликатов (по адресу и площади)
    """
    
    def __init__(self):
        """Инициализирует пустую коллекцию квартир."""
        self._items: List[Apartment] = []
    
    def add(self, item: Apartment) -> None:
        """
        Добавляет объект Apartment в коллекцию.
        
        Args:
            item (Apartment): Объект квартиры для добавления
            
        Raises:
            TypeError: Если передан объект неверного типа
            ValueError: Если квартира с таким же адресом и площадью уже существует
            
        Requirements:
            - Проверяет тип добавляемого объекта
            - Не допускает добавления дубликатов (по критериям __eq__)
        """
        if not isinstance(item, Apartment):
            raise TypeError(f"Можно добавлять только объекты Apartment. Получен {type(item).__name__}")
        
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
            
        Requirements:
            - Корректно удаляет объекты
            - Работает через __eq__ метод Apartment
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
            
        Requirements:
            - Удаляет по индексу
            - Возвращает удалённый объект
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
            
        Requirements:
            - Предоставляет доступ к объектам
            - Возвращает копию списка для безопасности
        """
        return self._items.copy()
    
    def find_by_address(self, address: str) -> Optional[Apartment]:
        """
        Находит квартиру по адресу (полное или частичное совпадение).
        
        Args:
            address (str): Адрес для поиска (полное или частичное совпадение)
            
        Returns:
            Optional[Apartment]: Найденная квартира или None
            
        Requirements:
            - Поиск по одному из атрибутов
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
    
    def __len__(self) -> int:
        """
        Возвращает количество объектов в коллекции.
        
        Returns:
            int: Количество квартир в коллекции
            
        Requirements:
            - Чтобы можно было писать len(collection)
        """
        return len(self._items)
    
    def __iter__(self) -> Iterator[Apartment]:
        """
        Возвращает итератор по коллекции.
        
        Returns:
            Iterator[Apartment]: Итератор по объектам Apartment
            
        Requirements:
            - Чтобы можно было писать for item in collection
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
            
        Requirements:
            - Чтобы можно было писать collection[0], collection[2] и т.д.
        """
        return self._items[index]
    
    def sort_by_price(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по цене.
        
        Args:
            reverse (bool): Если True, сортировка по убыванию (по умолчанию - по возрастанию)
            
        Requirements:
            - Сортировка объектов
        """
        self._items.sort(key=lambda x: x.price, reverse=reverse)
    
    def sort_by_area(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по площади.
        
        Args:
            reverse (bool): Если True, сортировка по убыванию (по умолчанию - по возрастанию)
            
        Requirements:
            - Сортировка объектов
        """
        self._items.sort(key=lambda x: x.area, reverse=reverse)
    
    def sort_by_rent_duration(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по сроку аренды.
        
        Args:
            reverse (bool): Если True, сортировка по убыванию (по умолчанию - по возрастанию)
            
        Requirements:
            - Сортировка объектов
        """
        self._items.sort(key=lambda x: x.rent_duration, reverse=reverse)
    
    def sort(self, key: Callable[[Apartment], any], reverse: bool = False) -> None:
        """
        Универсальная сортировка по заданному ключу.
        
        Args:
            key (Callable[[Apartment], any]): Функция, возвращающая ключ для сортировки
            reverse (bool): Если True, сортировка по убыванию
            
        Requirements:
            - Универсальная сортировка
        """
        self._items.sort(key=key, reverse=reverse)
    
    def get_available(self) -> 'ApartmentCollection':
        """
        Возвращает новую коллекцию со свободными квартирами.
        
        Returns:
            ApartmentCollection: Коллекция свободных квартир
            
        Requirements:
            - Логические операции над коллекцией
            - Возвращает новую коллекцию
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
            
        Requirements:
            - Логические операции над коллекцией
            - Возвращает новую коллекцию
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
            
        Requirements:
            - Логические операции над коллекцией
            - Возвращает новую коллекцию
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
            
        Requirements:
            - Логические операции над коллекцией
            - Возвращает новую коллекцию
        """
        new_collection = ApartmentCollection()
        for item in self._items:
            if item.rent_duration == duration:
                new_collection.add(item)
        return new_collection
    
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
            result += f"{i}. {item.address} - {item.area} м², {item.price:,.2f} руб.\n"
        return result.strip()
    
    def __repr__(self) -> str:
        """
        Возвращает техническое представление коллекции.
        
        Returns:
            str: Техническое представление
        """
        return f"ApartmentCollection(items={len(self._items)})"