"""
Модуль содержит бизнес-логику приложения - управление коллекцией квартир.
Все операции над коллекцией выполняются через этот модуль.
"""

from typing import List, Optional, Callable, Any
from pathlib import Path
import sys

# Добавляем путь к lab01 для импорта базового класса
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment
from exceptions import (
    ApartmentNotFoundError,
    DuplicateApartmentError,
    InvalidApartmentError,
    ApartmentOperationError,
    StorageError
)
from storage import save, load, DEFAULT_STORAGE_PATH


class ApartmentApp:
    """
    Класс приложения, управляющий коллекцией квартир.
    Содержит всю бизнес-логику приложения.
    
    Attributes:
        _collection (List[Apartment]): Коллекция квартир
        _storage_path (Path): Путь к файлу хранения данных
    """
    
    def __init__(self, storage_path: Path = DEFAULT_STORAGE_PATH):
        """
        Инициализация приложения.
        
        Args:
            storage_path: Путь к файлу хранения данных
        """
        self._collection: List[Apartment] = []
        self._storage_path = storage_path
    
    @property
    def collection(self) -> List[Apartment]:
        """
        Возвращает коллекцию квартир.
        
        Returns:
            List[Apartment]: Список квартир
        """
        return self._collection.copy()
    
    @property
    def count(self) -> int:
        """
        Возвращает количество квартир в коллекции.
        
        Returns:
            int: Количество квартир
        """
        return len(self._collection)
    
    def add_apartment(self, area: float, price: float, address: str, 
                      rent_duration: int) -> Apartment:
        """
        Добавляет новую квартиру в коллекцию.
        
        Args:
            area: Площадь квартиры (м²)
            price: Цена аренды (руб.)
            address: Адрес квартиры
            rent_duration: Срок аренды (мес.)
            
        Returns:
            Apartment: Созданная квартира
            
        Raises:
            DuplicateApartmentError: Если квартира с таким адресом и площадью уже существует
            InvalidApartmentError: Если данные некорректны
        """
        # Валидация данных
        self._validate_apartment_data(area, price, address, rent_duration)
        
        # Создание квартиры
        apartment = Apartment(area, price, address, rent_duration)
        
        # Проверка на дубликат
        for existing in self._collection:
            if existing == apartment:
                raise DuplicateApartmentError(existing.address, existing.area)
        
        self._collection.append(apartment)
        return apartment
    
    def remove_apartment(self, identifier: str) -> Apartment:
        """
        Удаляет квартиру из коллекции по адресу.
        
        Args:
            identifier: Адрес квартиры (полное или частичное совпадение)
            
        Returns:
            Apartment: Удалённая квартира
            
        Raises:
            ApartmentNotFoundError: Если квартира не найдена
        """
        apartment = self.find_by_address(identifier)
        if apartment is None:
            raise ApartmentNotFoundError(identifier, "адресу")
        
        self._collection.remove(apartment)
        return apartment
    
    def remove_by_index(self, index: int) -> Apartment:
        """
        Удаляет квартиру по индексу.
        
        Args:
            index: Индекс квартиры в коллекции
            
        Returns:
            Apartment: Удалённая квартира
            
        Raises:
            ApartmentNotFoundError: Если индекс вне диапазона
        """
        if index < 0 or index >= len(self._collection):
            raise ApartmentNotFoundError(str(index), "индексу")
        
        apartment = self._collection[index]
        del self._collection[index]
        return apartment
    
    def find_by_address(self, address: str) -> Optional[Apartment]:
        """
        Находит квартиру по адресу (полное или частичное совпадение).
        
        Args:
            address: Адрес для поиска
            
        Returns:
            Optional[Apartment]: Найденная квартира или None
        """
        for apartment in self._collection:
            if address.lower() in apartment.address.lower():
                return apartment
        return None
    
    def find_by_index(self, index: int) -> Optional[Apartment]:
        """
        Находит квартиру по индексу.
        
        Args:
            index: Индекс квартиры
            
        Returns:
            Optional[Apartment]: Квартира по индексу или None
        """
        if 0 <= index < len(self._collection):
            return self._collection[index]
        return None
    
    def filter_by_price_range(self, min_price: float, max_price: float) -> List[Apartment]:
        """
        Фильтрует квартиры по диапазону цен.
        
        Args:
            min_price: Минимальная цена
            max_price: Максимальная цена
            
        Returns:
            List[Apartment]: Список квартир в диапазоне
        """
        return [apt for apt in self._collection if min_price <= apt.price <= max_price]
    
    def filter_by_area_range(self, min_area: float, max_area: float) -> List[Apartment]:
        """
        Фильтрует квартиры по диапазону площади.
        
        Args:
            min_area: Минимальная площадь
            max_area: Максимальная площадь
            
        Returns:
            List[Apartment]: Список квартир в диапазоне
        """
        return [apt for apt in self._collection if min_area <= apt.area <= max_area]
    
    def filter_by_rent_duration(self, duration: int) -> List[Apartment]:
        """
        Фильтрует квартиры по сроку аренды.
        
        Args:
            duration: Срок аренды (мес.)
            
        Returns:
            List[Apartment]: Список квартир с заданным сроком
        """
        return [apt for apt in self._collection if apt.rent_duration == duration]
    
    def get_available(self) -> List[Apartment]:
        """
        Возвращает список свободных квартир.
        
        Returns:
            List[Apartment]: Список свободных квартир
        """
        return [apt for apt in self._collection if not apt.is_rented]
    
    def get_rented(self) -> List[Apartment]:
        """
        Возвращает список арендованных квартир.
        
        Returns:
            List[Apartment]: Список арендованных квартир
        """
        return [apt for apt in self._collection if apt.is_rented]
    
    def get_expensive(self, threshold: float) -> List[Apartment]:
        """
        Возвращает квартиры дороже заданного порога.
        
        Args:
            threshold: Порог стоимости
            
        Returns:
            List[Apartment]: Список дорогих квартир
        """
        return [apt for apt in self._collection if apt.price > threshold]
    
    def sort_by_price(self, reverse: bool = False) -> List[Apartment]:
        """
        Сортирует квартиры по цене.
        
        Args:
            reverse: Если True, сортировка по убыванию
            
        Returns:
            List[Apartment]: Отсортированный список
        """
        return sorted(self._collection, key=lambda x: x.price, reverse=reverse)
    
    def sort_by_area(self, reverse: bool = False) -> List[Apartment]:
        """
        Сортирует квартиры по площади.
        
        Args:
            reverse: Если True, сортировка по убыванию
            
        Returns:
            List[Apartment]: Отсортированный список
        """
        return sorted(self._collection, key=lambda x: x.area, reverse=reverse)
    
    def sort_by_rent_duration(self, reverse: bool = False) -> List[Apartment]:
        """
        Сортирует квартиры по сроку аренды.
        
        Args:
            reverse: Если True, сортировка по убыванию
            
        Returns:
            List[Apartment]: Отсортированный список
        """
        return sorted(self._collection, key=lambda x: x.rent_duration, reverse=reverse)
    
    def rent_apartment(self, identifier: str) -> Apartment:
        """
        Сдаёт квартиру в аренду.
        
        Args:
            identifier: Адрес квартиры
            
        Returns:
            Apartment: Сданная квартира
            
        Raises:
            ApartmentNotFoundError: Если квартира не найдена
            ApartmentOperationError: Если квартира уже арендована
        """
        apartment = self.find_by_address(identifier)
        if apartment is None:
            raise ApartmentNotFoundError(identifier, "адресу")
        
        if apartment.is_rented:
            raise ApartmentOperationError("сдать в аренду", "квартира уже арендована")
        
        apartment.rent()
        return apartment
    
    def vacate_apartment(self, identifier: str) -> Apartment:
        """
        Освобождает квартиру (прекращает аренду).
        
        Args:
            identifier: Адрес квартиры
            
        Returns:
            Apartment: Освобождённая квартира
            
        Raises:
            ApartmentNotFoundError: Если квартира не найдена
            ApartmentOperationError: Если квартира не арендована
        """
        apartment = self.find_by_address(identifier)
        if apartment is None:
            raise ApartmentNotFoundError(identifier, "адресу")
        
        if not apartment.is_rented:
            raise ApartmentOperationError("освободить", "квартира не арендована")
        
        apartment.vacate()
        return apartment
    
    def update_apartment(self, identifier: str, **kwargs) -> Apartment:
        """
        Обновляет данные квартиры.
        
        Args:
            identifier: Адрес квартиры
            **kwargs: Поля для обновления (area, price, address, rent_duration)
            
        Returns:
            Apartment: Обновлённая квартира
            
        Raises:
            ApartmentNotFoundError: Если квартира не найдена
            ApartmentOperationError: Если квартира арендована
            InvalidApartmentError: Если данные некорректны
        """
        apartment = self.find_by_address(identifier)
        if apartment is None:
            raise ApartmentNotFoundError(identifier, "адресу")
        
        if apartment.is_rented:
            raise ApartmentOperationError("изменить", "нельзя изменять арендованную квартиру")
        
        # Обновление полей
        if "area" in kwargs:
            apartment.area = kwargs["area"]
        if "price" in kwargs:
            apartment.price = kwargs["price"]
        if "address" in kwargs:
            apartment.address = kwargs["address"]
        if "rent_duration" in kwargs:
            apartment.rent_duration = kwargs["rent_duration"]
        
        return apartment
    
    def save_data(self) -> None:
        """
        Сохраняет данные коллекции в файл.
        
        Raises:
            StorageError: Если возникла ошибка при сохранении
        """
        save(self._collection, self._storage_path)
    
    def load_data(self) -> int:
        """
        Загружает данные коллекции из файла.
        
        Returns:
            int: Количество загруженных квартир
            
        Raises:
            StorageError: Если возникла ошибка при загрузке
        """
        self._collection = load(self._storage_path)
        return len(self._collection)
    
    def clear_collection(self) -> None:
        """
        Очищает коллекцию.
        """
        self._collection.clear()
    
    def _validate_apartment_data(self, area: float, price: float, 
                                  address: str, rent_duration: int) -> None:
        """
        Валидация данных квартиры.
        
        Args:
            area: Площадь
            price: Цена
            address: Адрес
            rent_duration: Срок аренды
            
        Raises:
            InvalidApartmentError: Если данные некорректны
        """
        # Проверка типа и значения площади
        if not isinstance(area, (int, float)):
            raise InvalidApartmentError("площадь", str(area), "должно быть числом")
        if area <= 0:
            raise InvalidApartmentError("площадь", str(area), "должна быть положительной")
        
        # Проверка типа и значения цены
        if not isinstance(price, (int, float)):
            raise InvalidApartmentError("цена", str(price), "должна быть числом")
        if price <= 0:
            raise InvalidApartmentError("цена", str(price), "должна быть положительной")
        
        # Проверка адреса
        if not isinstance(address, str) or not address.strip():
            raise InvalidApartmentError("адрес", str(address), "не может быть пустым")
        
        # Проверка срока аренды
        if not isinstance(rent_duration, int):
            raise InvalidApartmentError("срок аренды", str(rent_duration), "должно быть целым числом")
        if rent_duration <= 0:
            raise InvalidApartmentError("срок аренды", str(rent_duration), "должен быть положительным")
    
    def get_statistics(self) -> dict:
        """
        Возвращает статистику по коллекции.
        
        Returns:
            dict: Статистика
        """
        if not self._collection:
            return {
                "total": 0,
                "available": 0,
                "rented": 0,
                "avg_price": 0,
                "avg_area": 0,
                "min_price": 0,
                "max_price": 0
            }
        
        total = len(self._collection)
        available = len(self.get_available())
        rented = len(self.get_rented())
        
        prices = [apt.price for apt in self._collection]
        areas = [apt.area for apt in self._collection]
        
        return {
            "total": total,
            "available": available,
            "rented": rented,
            "avg_price": sum(prices) / total,
            "avg_area": sum(areas) / total,
            "min_price": min(prices),
            "max_price": max(prices)
        }