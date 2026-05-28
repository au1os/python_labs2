"""
Модуль содержит модели квартир, реализующие интерфейсы из lab04.
На основе классов из ЛР-3 добавлена реализация интерфейсов:
- IPrintable
- IComparable
- IRentable
"""

from typing import List, Optional
from interfaces import IPrintable, IComparable, IRentable
import sys
from pathlib import Path

# Добавляем путь к lab01 для импорта базового класса
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment


class ApartmentBase(Apartment, IPrintable, IComparable, IRentable):
    """
    Базовый класс квартиры с реализацией интерфейсов.
    Наследуется от Apartment из ЛР-1 и реализует интерфейсы.
    """
    
    def to_string(self) -> str:
        """
        Реализация интерфейса IPrintable.
        Возвращает строковое представление квартиры.
        """
        return str(self)
    
    def compare_to(self, other: 'ApartmentBase') -> int:
        """
        Реализация интерфейса IComparable.
        Сравнивает квартиры по цене (по возрастанию).
        
        Returns:
            int: отрицательное если self.price < other.price
                 0 если цены равны
                 положительное если self.price > other.price
        """
        if not isinstance(other, ApartmentBase):
            raise TypeError(f"Cannot compare ApartmentBase with {type(other).__name__}")
        
        if self._price < other._price:
            return -1
        elif self._price > other._price:
            return 1
        return 0
    
    def get_rental_price(self) -> float:
        """
        Реализация интерфейса IRentable.
        Возвращает ежемесячный платёж.
        """
        return self.calculate_monthly_payment()
    
    def is_available(self) -> bool:
        """
        Реализация интерфейса IRentable.
        Проверяет доступность квартиры.
        """
        return not self._is_rented
    
    def rent(self) -> None:
        """
        Реализация интерфейса IRentable.
        Сдаёт квартиру в аренду.
        """
        super().rent()
    
    def vacate(self) -> None:
        """
        Реализация интерфейса IRentable.
        Освобождает квартиру.
        """
        super().vacate()


class StudioApartment(ApartmentBase):
    """
    Квартира-студия с реализацией интерфейсов.
    Наследуется от ApartmentBase и добавляет специфичные атрибуты.
    """
    
    STUDIO_TYPES = ["стандарт", "комфорт", "премиум"]
    
    def __init__(self, area: float, price: float, address: str, rent_duration: int,
                 has_kitchenette: bool, studio_type: str):
        super().__init__(area, price, address, rent_duration)
        
        if not isinstance(has_kitchenette, bool):
            raise TypeError("has_kitchenette должен быть булевым значением")
        self._has_kitchenette = has_kitchenette
        
        if studio_type not in self.STUDIO_TYPES:
            raise ValueError(f"Тип студии должен быть одним из: {self.STUDIO_TYPES}")
        self._studio_type = studio_type
    
    @property
    def has_kitchenette(self) -> bool:
        return self._has_kitchenette
    
    @property
    def studio_type(self) -> str:
        return self._studio_type
    
    def to_string(self) -> str:
        """Переопределение to_string() для студий."""
        base_str = super().to_string()
        kitchen_info = "с кухонным уголком" if self._has_kitchenette else "без кухонного уголка"
        return f"{base_str}\n  Тип: Студия ({self._studio_type})\n  Кухонный уголок: {kitchen_info}"
    
    def compare_to(self, other: 'StudioApartment') -> int:
        """
        Переопределение compare_to() для студий.
        Сравнивает по площади.
        """
        if not isinstance(other, StudioApartment):
            raise TypeError(f"Cannot compare StudioApartment with {type(other).__name__}")
        
        if self._area < other._area:
            return -1
        elif self._area > other._area:
            return 1
        return 0
    
    def calculate_monthly_payment(self) -> float:
        """Расчёт с учётом типа студии."""
        base_payment = super().calculate_monthly_payment()
        
        if self._studio_type == "премиум":
            return base_payment * 1.2
        elif self._studio_type == "комфорт":
            return base_payment * 1.1
        return base_payment
    
    def is_suitable_for_students(self) -> bool:
        """Проверка пригодности для студентов."""
        return self._has_kitchenette and self._studio_type in ["стандарт", "комфорт"]
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return (f"StudioApartment(area={self._area}, price={self._price}, "
                f"address='{self._address}', rent_duration={self._rent_duration}, "
                f"has_kitchenette={self._has_kitchenette}, studio_type='{self._studio_type}')")


class LuxuryApartment(ApartmentBase):
    """
    Элитная квартира с реализацией интерфейсов.
    Наследуется от ApartmentBase и добавляет специфичные атрибуты.
    """
    
    FLOOR_LEVELS = ["низкий", "средний", "высокий", "пентхаус"]
    
    def __init__(self, area: float, price: float, address: str, rent_duration: int,
                 has_parking: bool, floor_level: str, luxury_features: Optional[List[str]] = None):
        super().__init__(area, price, address, rent_duration)
        
        if not isinstance(has_parking, bool):
            raise TypeError("has_parking должен быть булевым значением")
        self._has_parking = has_parking
        
        if floor_level not in self.FLOOR_LEVELS:
            raise ValueError(f"Уровень этажа должен быть одним из: {self.FLOOR_LEVELS}")
        self._floor_level = floor_level
        
        self._luxury_features = luxury_features if luxury_features else []
    
    @property
    def has_parking(self) -> bool:
        return self._has_parking
    
    @property
    def floor_level(self) -> str:
        return self._floor_level
    
    @property
    def luxury_features(self) -> List[str]:
        return self._luxury_features.copy()
    
    def add_luxury_feature(self, feature: str) -> None:
        """Добавление элитной особенности."""
        if not isinstance(feature, str) or not feature.strip():
            raise ValueError("Особенность должна быть непустой строкой")
        
        feature = feature.strip()
        if feature not in self._luxury_features:
            self._luxury_features.append(feature)
    
    def to_string(self) -> str:
        """Переопределение to_string() for элитных квартир."""
        base_str = super().to_string()
        parking_info = "с парковкой" if self._has_parking else "без парковки"
        features_str = ", ".join(self._luxury_features) if self._luxury_features else "нет особенностей"
        
        return (f"{base_str}\n"
                f"  Тип: Элитная квартира\n"
                f"  Этаж: {self._floor_level}\n"
                f"  Парковка: {parking_info}\n"
                f"  Особенности: {features_str}")
    
    def compare_to(self, other: 'LuxuryApartment') -> int:
        """
        Переопределение compare_to() для элитных квартир.
        Сравнивает по количеству особенностей.
        """
        if not isinstance(other, LuxuryApartment):
            raise TypeError(f"Cannot compare LuxuryApartment with {type(other).__name__}")
        
        if len(self._luxury_features) < len(other._luxury_features):
            return -1
        elif len(self._luxury_features) > len(other._luxury_features):
            return 1
        return 0
    
    def get_rental_price(self) -> float:
        """Переопределение цены аренды с учётом элитности."""
        return self.calculate_monthly_payment()
    
    def calculate_monthly_payment(self) -> float:
        """Расчёт с учётом элитности."""
        base_payment = super().calculate_monthly_payment()
        
        if self._floor_level == "пентхаус":
            base_payment *= 1.5
        elif self._floor_level == "высокий":
            base_payment *= 1.2
        
        if self._has_parking:
            base_payment *= 1.1
        
        if len(self._luxury_features) > 3:
            base_payment *= 1.15
        
        return base_payment
    
    def is_vip(self) -> bool:
        """Проверка VIP статуса."""
        return self._floor_level == "пентхаус" or len(self._luxury_features) > 3
    
    def is_suitable_for_family(self) -> bool:
        """Проверка пригодности для семей."""
        return self._has_parking and self._area > 60
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return (f"LuxuryApartment(area={self._area}, price={self._price}, "
                f"address='{self._address}', rent_duration={self._rent_duration}, "
                f"has_parking={self._has_parking}, floor_level='{self._floor_level}', "
                f"luxury_features={self._luxury_features})")